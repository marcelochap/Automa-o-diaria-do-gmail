---
name: morning-email-triage
description: Analyzes the Gmail inbox for important unread emails, ignoring spam and newsletters.
category: productivity
risk: safe
source: local
tags: [gmail, automation, triage, productivity]
date_added: "2026-03-16"
---

# morning-email-triage

## Purpose
This skill identifies crucial unread emails to start the day efficiently. It filters out irrelevant content like spam and newsletters, focusing on items that require immediate attention or action.

## Trigger Phrases
- "triage my emails"
- "check my morning emails"
- "find important unread emails"
- "start morning email triage"

## Core Capabilities
1. **Gmail Triaging**: Uses the GWS Gmail tool to list and analyze unread messages.
2. **Sender & Subject Evaluation**: Distinguishes between critical communications and noise (newsletters/spam).
3. **Task Automation**: Converts actionable emails into tasks using the `email-to-task` workflow.

## Instructions

### Objective: Obtain crucial emails to start the day.

### Steps:
1. **Fetch Unread Emails**: Use the GWS Gmail MCP tool with the `+triage` suffix to pull the latest unread messages.
2. **Analyze Content**: Evaluate the sender and subject line of each email.
3. **Filter Noise**: Disregard any emails identified as spam, automated newsletters, or promotional material.
4. **Convert to Tasks**: For every email that requires action, trigger the `gws workflow +email-to-task` command to ensure follow-up.

## Constraints
- **Do Not Delete**: Never delete or archive emails. Only read and create tasks.
- **Focus on Action**: Only create tasks for emails requiring specific follow-up from the user.

## Files
- Directory: `agents/morning-email-triage/`
- SOP: `directives/triage_sop.md`
- Script: `execution/gmail_triage.py`
