---
title: Evidence-to-brief review process
type: process
status: draft
id: proc-evidence-to-brief
domain: process
project: knowledge-pilot
version: 0.1.0
supporting:
- notes/curated/transcript-2026-01-12-knowledge-pilot-CURATED.md
---

# Evidence-to-brief review

Fictional process definition. It describes the expected workflow, not a claim
that every stage has happened.

## Overview

Create a decision brief from permitted source material with reviewable evidence.

## Stages

### 1. Curate the permitted source

- ID: curate
- Role: author
- Trigger: a permitted source has been normalized
- Tools: Markdown editor and curation skill
- Output: a mirrored curated note with its origin

### 2. Verify coverage

- ID: verify
- Role: reviewer
- Trigger: curated draft available
- Tools: source, curated note and comparison checklist
- Gate: qualifications, unresolved questions and ownership boundaries are retained

### 3. Compose and review

- ID: compose
- Role: author and designated approver
- Trigger: reviewed source bundle available
- Tools: composition skill and work-product template
- Gate: factual support, audience and sharing permission are reviewed separately

## Invariants

A source link does not prove that a claim is supported. A finished document does
not establish permission to share it.

## Exception paths

Missing permission stops capture. Unclear attribution stays uncertain. Missing
approval keeps the output in draft. Record an observed deviation as a process
run; do not rewrite the process definition merely to match an unfinished run.
