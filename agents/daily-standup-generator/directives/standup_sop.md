# Standup SOP (Standard Operating Procedure)

## Goal
To generate a comprehensive morning briefing that prepares the user for their day's responsibilities.

## Protocol

### 1. Data Collection
- Run `gws workflow +standup-report`.
- Identify the earliest meeting in the returned list.

### 2. Deep Dive (First Meeting)
- For the earliest meeting, run `gws workflow +meeting-prep`.
- Capture:
    - Meeting Title & Time
    - Agenda items
    - Participant list
    - Linked Google Drive documents

### 3. Synthesis
- Combine the general standup report with the deep prep for the first meeting.
- Add a "Action Items" section for any tasks listed in the standup report.

### 4. Communication
- Present the report in the current chat.
- (Optional) Prompt or auto-trigger `gws chat +send` with the formatted content.

## Error Handling
- If no meetings are found, note that the day is clear but still list tasks.
- If `meeting-prep` fails, provide the basic meeting info from the `standup-report`.
