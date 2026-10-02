# Sharing, privacy and trust boundaries

The capture principle has a limit: do not capture material you are not allowed
to retain or do not want retained. Consent, purpose, retention and deletion rules
come before the convenience of searchable memory. A rule to preserve source
meaning must not override a legitimate deletion requirement.

## Separate workspaces and explicit transfer

Personal projects, businesses and client work can have different sharing rules.
The broader design uses separate vaults and explicit transfer with provenance.
Credentials, model access and tool scope need corresponding boundaries; a folder
name or a `share_with` field does not enforce them on its own.

The design challenge spans original files, derived chunks, embeddings, graph
expansion, rerankers, caches and generated outputs. Authorization must apply
before material reaches an external service or another workspace, not only when
final search results are displayed.

## Private memory and public outputs serve different audiences

A work product is not automatically publishable. The intended sharing path is:

1. Choose the audience and purpose.
2. Select permitted evidence and draft an output.
3. Review factual support and sensitive details.
4. Record the approved selection in a manifest.
5. Export the selected artifact and keep its provenance.
6. Let outward-facing consumers read that approved surface, not the private vault.

The public repository documents these boundaries and leaves the published areas
empty. It does not claim to provide a comprehensive redaction engine, enforce
multi-client isolation or automatically approve an output.

## Tools, guardrails and review

The public MCP server reads this checkout and has no external mutation tools.
It is still important to treat retrieved text as data, not instructions. A client
can send returned content to its chosen model provider. If adapting this template
for private use, configure the client and provider accordingly.

In a larger system, tool gateways, restricted credentials, hooks, audit records,
logs and human review protect different parts of the workflow. A declared
read-only hint is not an authorization system. Inspect what the tool actually
can do and calibrate verification to the consequence of a failure.
