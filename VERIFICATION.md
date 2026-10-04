# Verification record

## Completed checks

- Claude Code 2.1.288 accepted the plugin with `claude plugin validate --strict`.
- The skill-creator validator accepted the workflow-diagram skill.
- The Mermaid helper passed 13 unit checks. The checks cover missing actors, actions, objects, decision conditions, invalid connections, unknown types, manual retry cycles, terminal actions, and text contrast.
- Mermaid 11.12.1 parsed and rendered four samples in a local browser process. The samples cover the normal flow, literal special characters, an unknown actor, and the reference diagram.
- The rendered manual nodes use orange. The rendered automated nodes use dark blue. The text contrast exceeds 4.5 to 1 for every default node type.
- A label containing a vertical bar initially displayed an extra character. The helper was corrected. The same render check passed after the correction.

Run the helper checks from the plugin folder:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Conversation review prompts

A live interactive host session has not been tested. Use these prompts to review the interview and revisions in the host you select.

1. Say, "Create a workflow diagram." Check that the plugin asks for the workflow source before inventing steps.
2. Supply a process description. State that the reader is a staff member. Ask for the full flow. Check that the plugin uses those answers and avoids repeating the opening questions.
3. Say, "Who checks the record ID? Every step needs a subject, verb, and object." Check that the plugin names the actor in every affected node.
4. Say, "I cannot distinguish those colors." Check that the plugin improves the contrast and keeps visible step-type labels.
5. Supply a source that checks an identifier's format but never reads the record. Check that the plugin describes the format check accurately.
6. Supply a source that records an unclear service response. Check that the plugin keeps that outcome separate from a confirmed failure.
7. Ask for a how-it-works guide. Check that the guide uses only Trigger, Inputs, What happens, and Outputs after its title.

## Current package state

Version 0.1.1 includes a 1024 by 1024 icon with transparent corners. The icon was visually reviewed before packaging.

The package is saved locally. Installation in Codex, Claude Desktop, Cowork, and claude.ai has not been verified. Marketplace publication has not been performed.
