---
description: This flow coordinates the user's start of the day, extracting data from Google Workspace and generating an actionable briefing.
---

# Workflow: Morning Routine

**Trigger:** User requests "start the day", "morning routine", or "run my morning routine".

## Execution Phases

### Phase 1: Data Extraction (DevWorkflow Agent)
The DevWorkflow Agent takes control and uses GWS MCP tools to extract current context:
1. Execute email triage using the native triage command (or custom REST script) to find important unread messages.
2. **Mark analyzed emails as read** to maintain inbox hygiene and prevent duplication.
3. Execute calendar search for today's events.

### Phase 2: Analysis and Planning (PM Agent / Reader)
Once raw data is collected in Phase 1, the PM Agent (Reader) enters the workflow:
1. Analyze provided emails and calendar data.
2. Use the `daily-standup-generator` skill to structure a report of meetings and pending tasks.
3. For the first meeting of the day, extract agenda, participants, and linked documents.
4. Identify emails requiring immediate action and prepare task conversion suggestions.

### Phase 3: UI Formatting (Frontend Agent)
The PM Agent hands the structured analysis to the Frontend Agent (`morning-briefing-ui`):
1. Receive the analysis of emails, calendar, and news.
2. Convert the content into a premium, Gmail-safe HTML template using inline CSS.
3. Ensure the layout includes a motivational greeting and highlighted sections for critical alerts.

### Phase 4: Synthesis and Sending (Orchestrator Agent)
The Orchestrator Agent resumes control to finalize the flow:
1. Present the final HTML preview to the user.
2. Send the briefing to the user's Gmail using `gws gmail +send`.
3. Actively ask: "Would you like me to transform any of these emails into Google Tasks or prepare a response?"
4. If confirmed, trigger the task conversion skill (`+email-to-task`).

