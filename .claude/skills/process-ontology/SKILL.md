---
name: process-ontology
description: Maintain process definitions, vocabulary and evidence of observed process runs.
---

# Process Ontology

Selected adaptation of the knowledge-work method for this public template.

Inspect the relevant curated record and existing `reference/processes/` definitions.

Classify the change: a new or changed workflow, an observed run, a glossary change, a verification gate, or no ontology change. A single exception does not automatically redefine the expected process.

A process definition describes stages, roles, triggers, tools, invariants and exception paths when known. Use real process IDs only for mapped processes. Leave unmapped dependencies in prose rather than inventing identifiers. Update the version when the definition changes.

A process run records what happened, evidence and outcome. Keep partial, blocked and completed states distinct. A completed activity is not proof that its goal was achieved. Link terms and architecture patterns when they clarify the process.

The read-only adapter can list these records and traverse explicit links. It does not implement the broader system's stage parser or gap-report tool. Validate local references with `knowledge-demo --validate` and review the meaning yourself.
