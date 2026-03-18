---
name: morning-email-triage
description: Analyzes the Gmail inbox for important unread emails, categorizes them based on priority, and ignores spam and newsletters.
category: productivity
risk: safe
source: local
tags: [gmail, automation, triage, productivity]
date_added: "2026-03-16"
---

# morning-email-triage

## Purpose
This skill identifies crucial unread emails to start the day efficiently. It categorizes emails according to a standard protocol, filters out irrelevant content (like spam, marketing, and newsletters), focuses on items requiring immediate action, and prepares a structured summary for the daily briefing.

## Trigger Phrases
- "triage my emails"
- "check my morning emails"
- "find important unread emails"
- "start morning email triage"

## Core Capabilities
1. **Gmail Triaging**: Uses the GWS Gmail tool to list and analyze unread messages.
2. **Contact Verification**: Uses the GWS `people` service via MCP to cross-reference unknown senders with the user's Google Contacts list.
3. **SOP Enforcement**: Reads and strictly follows the categorization rules defined in the external SOP document.
4. **Sender & Subject Evaluation**: Distinguishes between critical communications and noise.
5. **Task Automation**: Converts actionable emails into tasks using the `email-to-task` workflow.

## Instructions
### Objective: Obtain crucial emails, categorize them, and prepare the morning summary.

### Steps:
1. **Read Guidelines**: Before processing any data, read the categorization rules and protocol located in `directives/triage_sop.md`.
2. **Fetch Unread Emails**: Use the GWS Gmail MCP tool with the `+triage` suffix to pull the latest unread messages.
3. **Verify Senders**: For senders that are not obviously system alerts or newsletters, use the GWS `people` service via MCP to check if their email address exists in the user's contacts. 
4. **Categorize**: Evaluate the sender, subject line, and contact verification result. Distribute every message strictly into the 4 categories defined in the SOP: *Actionable*, *Informational*, *Newsletters*, and *Promotions*.
5. **Convert to Tasks**: For every email classified as **Actionable**, trigger the `gws workflow +email-to-task` command to ensure follow-up.
6. **Generate Summary**: Structure the final output for the briefing. Highlight the "Actionable" emails first (explaining briefly why they need attention). Group the other categories concisely.

## Constraints
- **Strict Categorization**: Do not invent new categories. Only use the 4 categories defined in the SOP.
- **Do Not Delete**: Never delete or archive emails. Only read, summarize, and create tasks.
- **Focus on Action**: Only create tasks for emails classified as *Actionable*.

## Files
- Directory: `agents/morning-email-triage/`
- SOP: `directives/triage_sop.md`
- Script: `execution/gmail_triage.py`