---
name: workflow-diagram
version: 1.1.3
description: Create or revise a Mermaid workflow diagram from code, configuration, or a process description. Use when a user wants to understand who does each step, distinguish manual and automated work, or improve a confusing workflow diagram. Ask a few focused questions and revise the diagram through conversation.
---

# Workflow Diagram

## Purpose in plain English

This skill helps you explain a workflow with a diagram showing who does each step and what happens next.

## How to explain the result

For a client-facing explanation, use ordinary words and the requested format. Explain unfamiliar abbreviations. Name what each number counts and explain its practical meaning. Keep internal identifiers out of the explanation. Keep necessary technical details in the working steps and technical references.

## Following the process

Use the process below. Preserve its conditions, commands, checks, and approval rules. Use information the user already supplied. Follow the existing questions or stopping rules when required information is missing.


Create a diagram that explains how the user's workflow works. Use the user's current source and answers. Keep the task focused on the diagram.

## Ask a few questions

Read the current conversation before asking anything. Keep answers and corrections the user has already given.

Ask one question at a time. Ask only questions whose answers would change the diagram. Use the host's question control when available. Otherwise, ask in the conversation and wait for the answer.

After each answer, use the new fact to choose the next needed question. Create the diagram when the required facts are known. If the user changes an earlier answer, update that fact and continue from the current question.

Use up to three opening questions. Skip any question the user has already answered.

1. Ask, "Which workflow should I diagram?" Request code, configuration, or a description when the source is missing.
2. Ask, "Who needs to understand this diagram?" Offer staff, a developer, or both when choices would help.
3. Ask, "How much detail should I show?" Offer the full flow with alternate routes or the main route first. Recommend the full flow when errors or retries affect the outcome.

Accept a combined answer. If the user asks you to choose, use a plain-language full flow for a reader who has not seen the code.

Ask a follow-up only when a required fact remains unknown. Name the missing fact. Keep the question specific, such as "Does a staff member select Send, or does a schedule start this workflow?"

If the user wants a draft despite missing facts, show those facts as unknown. Do not invent an actor, trigger, decision, or retry.

## Read the workflow

Read the supplied source. Inspect a referenced local file when it is available. Read a live configuration only when the user has requested or authorized access to that system. If access fails, identify the missing source.

Trace these facts:

- Identify the event that starts the workflow.
- Identify each input and its source.
- Name the person or system that performs each action.
- Record what each action reads, checks, creates, changes, sends, or returns.
- Record each condition and its possible results.
- Identify manual work, automated work, and steps whose type is unknown.
- Include successful routes, early stops, failure routes, unclear outcomes, and retries when the source contains them.
- Identify the final result and its destination.

Keep a private working list that connects each step to its source or a confirmed user answer. Do not turn a plan into a claim about a live system. A checked identifier format does not prove that a record exists. A returned identifier does not prove that a payment or delivery occurred.

When the source contains only one component, describe the known boundary. Ask for an upstream or downstream component only when the user's requested scope needs it. Do not add a guessed staff action to an automated component.

## Write the diagram

Read [diagram rules](references/diagram-rules.md) before the first diagram. Follow the user's preferred layout when it is known.

Use a Mermaid flowchart. Mermaid is text that a compatible viewer displays as a diagram.

A node represents one action or decision in the diagram.

Every action node needs a subject, a verb, and an object. Name the actual actor. Write "The worker checks the Payout record ID format." Avoid "Check ID," "Validation," "It checks," and "The system" when the source names a specific system.

Keep one action in each node. Split actions when different actors perform them. Use a diamond for a decision. Write the actor's check in the diamond. Label each outgoing arrow with the condition that selects that route.

Use these defaults unless the user requests another readable palette:

- Color manual nodes orange with fill `#F59E0B`, text `#111111`, and stroke `#783F00`.
- Color automated nodes dark blue with fill `#174EA6`, text `#FFFFFF`, and stroke `#0B2D64`.
- Color unknown nodes light gray with fill `#E5E7EB`, text `#111111`, and stroke `#4B5563`.
- Put "Manual," "Automated," or "Unknown" in every node.
- Use rounded nodes for manual actions. Use rectangles for automated actions. Use diamonds for decisions.
- Add a short legend. Apply the colors to the nodes themselves.

Use line breaks to keep labels readable. Use ordinary quoted Mermaid labels. Keep identifiers separate from visible labels. Avoid clickable links or executable callbacks in diagram source.

For a dense flow, split the diagram into named stages. Keep the links between stages visible. If the user chooses a main-route view, label it "Main route" and state which known routes that view omits.

The optional [Mermaid helper](scripts/build_mermaid.py) accepts a structured workflow and produces a flowchart. It checks required actors, actions, objects, branches, references, and reachability. It also applies the default palette. Use it when a local Python runner is available and saving diagram source serves the request. Use the [fictional example](references/example-workflow.json) to understand its input format. The helper does not infer the process from code.

## Check and return the result

Compare every node and arrow with the source. Confirm that all decision results reach an action or stopping point. Keep an unclear result separate from a confirmed failure. Show a retry only when the source or user confirms who starts it.

Check the color contrast. Pair colors with visible labels. Check Mermaid syntax with a local renderer or parser when one is available. Report a render limitation briefly when it affects the result. Do not upload private source to a public diagram service.

Return a short legend followed by one fenced `mermaid` block. Add a short note only for a material unknown, a source limitation, or an intentionally omitted route. Save a file when the user asks for one or the task already requires a saved artifact.

## Respond to feedback

Use the current diagram and confirmed answers. Apply the requested change before asking another question. Return the complete updated diagram.

- When a user asks who performs a check, name the actor in the affected node. Check the remaining nodes for the same issue.
- When a user cannot distinguish the colors, increase the contrast. Keep the manual and automated labels visible.
- When a user says the diagram is too dense, split the flow into stages or shorten repeated wording. Preserve the conditions and outcomes in the chosen view.
- When a user changes a workflow fact, update the affected actions and routes. Preserve unrelated confirmed facts.
- When a user asks for Mermaid, return Mermaid directly.

Ask one focused question only when the correction leaves a required fact unresolved. Finish after the updated result. Do not add a generic offer to continue.

## Use plain language everywhere

Apply these rules to questions, node labels, arrow labels, explanations, saved documents, and delivery messages:

- Use common words and complete sentences.
- Keep one idea in each sentence.
- Name the actor before the action.
- Preserve exact product, field, table, status, and command names.
- Explain a required technical term at first use.
- Avoid analogies, metaphors, em dashes, filler, and repeated summaries.
- Write "needs to be fixed" when that wording is needed.

Keep documentation within the requested scope. A diagram request explains the workflow. It does not authorize running that workflow or changing its business rules.

If the user requests a how-it-works guide, read [guide format](references/how-it-works-format.md). Use exactly Trigger, Inputs, What happens, and Outputs. Save the guide to the selected project location when requested. Update existing documents only when they directly describe the workflow and need a correction. Report a missing running-updates file instead of inventing its location.
