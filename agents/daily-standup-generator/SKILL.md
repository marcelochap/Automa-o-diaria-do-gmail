---
name: daily-standup-generator
description: Extracts the daily meetings and open tasks to create a morning briefing.
category: productivity
risk: safe
source: local
tags: [calendar, standup, briefing, productivity]
date_added: "2026-03-16"
---

# daily-standup-generator

## Purpose
This skill prepares the user for their day by aggregating all meetings and open tasks into a concise, friendly briefing. It also provides specific preparation details for the first meeting of the day.

## Trigger Phrases
- "generate my daily standup"
- "create morning briefing"
- "what's on my schedule today?"
- "run daily standup generator"

## Core Capabilities
1. **Report Generation**: Uses `gws workflow +standup-report` to pull today's meetings and tasks.
2. **Meeting Preparation**: Uses `gws workflow +meeting-prep` for the day's first meeting to list agenda, participants, and linked docs.
3. **Automated Delivery**: Optionally sends the final summary via `gws chat +send`.

## Instructions

### Objective: Prepare the user for daily meetings and tasks.

### Steps:
1. **Pull Data**: Execute the `gws workflow +standup-report` command to gather the list of meetings and tasks for the current day.
2. **Analyze First Meeting**: For the first scheduled meeting of the day, run `gws workflow +meeting-prep` to extract the agenda, attendee list, and any associated documents.
3. **Format Briefing**: Structure the gathered information into a friendly and readable morning report.
4. **Deliver (Optional)**: If requested or configured, use `gws chat +send` to deliver the summary directly to the user's Google Chat space or DM.

## Constraints
- **Friendly Tone**: Ensure the final output is friendly and professional.
- **Accurate Extraction**: Ensure all linked documents and participants from the first meeting are clearly listed.

## Files
- Directory: `agents/daily-standup-generator/`
- SOP: `directives/standup_sop.md`
