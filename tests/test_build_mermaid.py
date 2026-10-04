"""Check the Mermaid helper with valid and incomplete workflows."""

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "workflow-diagram"
SPEC = importlib.util.spec_from_file_location("build_mermaid", SKILL / "scripts" / "build_mermaid.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WorkflowChecks(unittest.TestCase):
    def setUp(self):
        self.workflow = json.loads((SKILL / "references" / "example-workflow.json").read_text())

    def test_valid_manual_retry_and_both_decision_routes(self):
        result = MODULE.build_mermaid(self.workflow)
        self.assertIn("Staff selects Process.", result)
        self.assertIn('The request is complete.', result)
        self.assertIn('The request is incomplete.', result)
        self.assertIn("R --> M", result)
        self.assertIn("class M,R manual;", result)

    def test_missing_actor_stops_the_output(self):
        self.workflow["nodes"][0]["actor"] = " "
        with self.assertRaisesRegex(ValueError, "actor needs text"):
            MODULE.build_mermaid(self.workflow)

    def test_missing_action_or_object_stops_the_output(self):
        for field in ("action", "object"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.workflow)
                del changed["nodes"][0][field]
                with self.assertRaisesRegex(ValueError, field + " needs text"):
                    MODULE.build_mermaid(changed)

    def test_unknown_type_is_visible(self):
        self.workflow["nodes"][0]["mode"] = "unknown"
        self.workflow["nodes"][0]["actor"] = "Unknown actor"
        result = MODULE.build_mermaid(self.workflow)
        self.assertIn("Unknown<br/>Unknown actor selects Process.", result)
        self.assertIn("class M unknown;", result)

    def test_decision_without_a_named_route_stops(self):
        self.workflow["edges"][2].pop("condition")
        with self.assertRaisesRegex(ValueError, "two labeled routes"):
            MODULE.build_mermaid(self.workflow)

    def test_decision_with_only_one_route_stops(self):
        self.workflow["edges"] = [edge for edge in self.workflow["edges"] if edge.get("to") != "F"]
        with self.assertRaisesRegex(ValueError, "two labeled routes"):
            MODULE.build_mermaid(self.workflow)

    def test_two_routes_with_the_same_condition_stop(self):
        self.workflow["edges"][3]["condition"] = self.workflow["edges"][2]["condition"]
        with self.assertRaisesRegex(ValueError, "repeats a route condition"):
            MODULE.build_mermaid(self.workflow)

    def test_an_edge_to_a_missing_node_stops(self):
        self.workflow["edges"][0]["to"] = "MISSING"
        with self.assertRaisesRegex(ValueError, "two existing node IDs"):
            MODULE.build_mermaid(self.workflow)

    def test_a_disconnected_step_stops(self):
        self.workflow["nodes"].append({"id": "Z", "actor": "Staff", "action": "reads", "object": "the result", "mode": "manual"})
        with self.assertRaisesRegex(ValueError, "cannot be reached"):
            MODULE.build_mermaid(self.workflow)

    def test_labels_preserve_literal_characters(self):
        self.workflow["nodes"][0]["object"] = '"Process" <draft> & Review | Confirm'
        result = MODULE.build_mermaid(self.workflow)
        self.assertIn('&quot;Process&quot; &lt;draft&gt; &amp; Review #124; Confirm.', result)
        self.assertNotIn('<draft>', result)

    def test_malformed_types_return_useful_errors(self):
        for field in ("mode", "kind"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.workflow)
                changed["nodes"][0][field] = []
                with self.assertRaises(ValueError):
                    MODULE.build_mermaid(changed)

    def test_a_single_terminal_action_is_valid(self):
        workflow = {"start": "A", "nodes": [{"id": "A", "actor": "The worker", "action": "returns", "object": "the result", "mode": "automated"}], "edges": []}
        result = MODULE.build_mermaid(workflow, "LR")
        self.assertTrue(result.startswith("flowchart LR"))
        self.assertIn("The worker returns the result.", result)

    def test_node_text_meets_normal_text_contrast(self):
        def luminance(hex_value):
            rgb = [int(hex_value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in rgb]
            return sum(value * weight for value, weight in zip(linear, (0.2126, 0.7152, 0.0722)))
        for mode, style in MODULE.STYLES.items():
            with self.subTest(mode=mode):
                values = dict(item.split(":", 1) for item in style.split(","))
                high, low = sorted((luminance(values["fill"]), luminance(values["color"])), reverse=True)
                self.assertGreaterEqual((high + 0.05) / (low + 0.05), 4.5)


if __name__ == "__main__":
    unittest.main()
