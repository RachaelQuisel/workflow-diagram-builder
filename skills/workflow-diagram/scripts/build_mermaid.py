#!/usr/bin/env python3
"""Create Mermaid source from a workflow with named actors and actions."""

import argparse
import html
import json
import re
import sys
from pathlib import Path

STYLES = {
    "manual": "fill:#F59E0B,stroke:#783F00,color:#111111,stroke-width:2px",
    "automated": "fill:#174EA6,stroke:#0B2D64,color:#FFFFFF,stroke-width:2px",
    "unknown": "fill:#E5E7EB,stroke:#4B5563,color:#111111,stroke-width:2px,stroke-dasharray:5 3",
}
IDENTIFIER = re.compile(r"[A-Z][A-Z0-9_]*\Z")


def required_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} needs text.")
    return " ".join(value.split())


def label(value):
    return html.escape(value, quote=True).replace("|", "#124;")


def build_mermaid(workflow, direction="TD"):
    if not isinstance(workflow, dict):
        raise ValueError("The workflow needs an object.")
    if direction not in {"TD", "LR"}:
        raise ValueError("The direction must be TD or LR.")
    nodes = workflow.get("nodes")
    edges = workflow.get("edges")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("The workflow needs at least one node.")
    if not isinstance(edges, list):
        raise ValueError("The workflow needs an edges list.")
    indexed = {}
    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("Each node needs an object.")
        identifier = node.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            raise ValueError("A node ID must start with an uppercase letter and use letters, numbers, or underscores.")
        if identifier in indexed:
            raise ValueError(f"Node {identifier} repeats an ID.")
        for field in ("actor", "action", "object"):
            required_text(node.get(field), f"Node {identifier} {field}")
        if not isinstance(node.get("mode"), str) or node["mode"] not in STYLES:
            raise ValueError(f"Node {identifier} needs manual, automated, or unknown mode.")
        if not isinstance(node.get("kind", "action"), str) or node.get("kind", "action") not in {"action", "decision"}:
            raise ValueError(f"Node {identifier} needs action or decision kind.")
        indexed[identifier] = node
    start = workflow.get("start")
    if not isinstance(start, str) or start not in indexed:
        raise ValueError("The start must name a node ID.")
    outgoing = {identifier: [] for identifier in indexed}
    seen_edges = set()
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("Each edge needs an object.")
        origin, destination = edge.get("from"), edge.get("to")
        if not isinstance(origin, str) or not isinstance(destination, str) or origin not in indexed or destination not in indexed:
            raise ValueError("Each edge must connect two existing node IDs.")
        condition = edge.get("condition")
        if condition is not None:
            required_text(condition, "An edge condition")
        key = (origin, destination, condition)
        if key in seen_edges:
            raise ValueError("An edge repeats the same route.")
        seen_edges.add(key)
        outgoing[origin].append(edge)
    for identifier, node in indexed.items():
        if node.get("kind") == "decision":
            branches = outgoing[identifier]
            if len(branches) < 2 or any(not edge.get("condition") for edge in branches):
                raise ValueError(f"Decision {identifier} needs at least two labeled routes.")
            conditions = [required_text(edge["condition"], "A decision condition") for edge in branches]
            if len(set(conditions)) != len(conditions):
                raise ValueError(f"Decision {identifier} repeats a route condition.")
    reached, pending = set(), [start]
    while pending:
        identifier = pending.pop()
        if identifier in reached:
            continue
        reached.add(identifier)
        pending.extend(edge["to"] for edge in outgoing[identifier])
    if reached != set(indexed):
        missing = ", ".join(sorted(set(indexed) - reached))
        raise ValueError(f"These nodes cannot be reached from the start: {missing}.")
    lines = [f"flowchart {direction}"]
    classes = {mode: [] for mode in STYLES}
    for identifier, node in indexed.items():
        sentence = " ".join(required_text(node[field], field) for field in ("actor", "action", "object"))
        if sentence[-1] not in ".?!":
            sentence += "."
        text = label(node["mode"].capitalize()) + "<br/>" + label(sentence)
        if node.get("kind") == "decision":
            wrapped = '{"' + text + '"}'
        elif node["mode"] == "manual":
            wrapped = '(["' + text + '"])'
        else:
            wrapped = '["' + text + '"]'
        lines.append(f"    {identifier}{wrapped}")
        classes[node["mode"]].append(identifier)
    for edge in edges:
        condition = edge.get("condition")
        connector = '-->|"' + label(required_text(condition, "condition")) + '"|' if condition else "-->"
        lines.append(f"    {edge['from']} {connector} {edge['to']}")
    for mode, style in STYLES.items():
        lines.append(f"    classDef {mode} {style};")
        if classes[mode]:
            lines.append(f"    class {','.join(classes[mode])} {mode};")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path, help="Read the workflow from this JSON file.")
    parser.add_argument("--output", type=Path, help="Save the Mermaid source to this file.")
    parser.add_argument("--direction", choices=("TD", "LR"), default="TD")
    args = parser.parse_args()
    try:
        result = build_mermaid(json.loads(args.workflow.read_text(encoding="utf-8")), args.direction)
        if args.output:
            args.output.write_text(result, encoding="utf-8")
        else:
            sys.stdout.write(result)
    except (OSError, ValueError) as error:
        print(f"The diagram could not be created: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
