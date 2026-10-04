# Workflow Diagram Builder

## Trigger

- The user asks the assistant to create or revise a workflow diagram.
- The workflow-diagram skill must be available in the current host.

## Inputs

- The assistant reads the code, configuration, or process description selected by the user.
- The assistant reads confirmed answers and corrections from the current conversation.
- The assistant uses the intended reader to choose the wording.
- The assistant uses the requested level of detail to choose the diagram's scope.
- The assistant uses the user's layout and color preferences when those preferences are known.
- The assistant uses a selected file location when the task requires a saved diagram or guide.
- The optional Mermaid helper reads a structured list of nodes and connections. Each node names an actor, action, object, and step type.

## What happens

1. The assistant checks which facts the user has already supplied. Each new answer determines the next needed question. If the user changes an earlier answer, the assistant updates that fact in the current flow.
2. If the source is missing, the assistant asks, "Which workflow should I diagram?" The assistant waits for the source or a request to proceed with unknown facts.
3. If the reader is unknown, the assistant asks, "Who needs to understand this diagram?" The assistant offers staff, a developer, or both when choices would help. The assistant waits for the answer before asking the next question.
4. If the level of detail is unknown, the assistant asks, "How much detail should I show?" The assistant offers the full flow or the main route first. The user can answer several questions together. If the user asks the assistant to choose, the assistant uses a plain-language full flow.
5. The assistant traces the trigger, inputs, actors, actions, conditions, and outcomes in the selected source.
6. If a required fact is missing, the assistant asks one focused question. If the user requests a draft, the assistant labels that fact as unknown.
7. The assistant writes each action as a sentence with a subject, verb, and object. The assistant gives each decision a named actor and labeled routes.
8. The assistant colors manual nodes orange. The assistant colors automated nodes dark blue. The assistant adds visible type labels. Unknown step types use gray.
9. If the diagram is dense, the assistant divides the flow into named stages. If the user chooses a main-route view, the assistant names the omitted routes.
10. If saving diagram source serves the request, the assistant can run the Mermaid helper. If a required label or connection is invalid, the helper stops with a specific error. The assistant corrects the structured workflow before trying again.
11. The assistant compares every node and arrow with the source. The assistant checks syntax with an available local Mermaid tool. If rendering is unavailable, the assistant states that limitation when it affects the result.
12. The assistant returns the legend and Mermaid diagram in the conversation. If the task requires saved files, the assistant saves them to the selected location.
13. If the user gives feedback, the assistant updates the affected labels, colors, detail, or routes. The assistant preserves previous answers. The assistant returns the complete revised diagram.
14. If the user requests a guide, the assistant writes Trigger, Inputs, What happens, and Outputs. The assistant updates an existing project document only when it directly describes the selected workflow and needs a correction.

## Outputs

- The user receives a Mermaid workflow diagram in the current conversation.
- The user receives a legend that identifies manual, automated, and unknown step types when present.
- The user receives a short note for a material unknown or source limitation when needed.
- When saving is requested, the user receives diagram source or a how-it-works guide in the selected project folder.
- When feedback is supplied, the user receives the complete updated diagram in the same conversation.
