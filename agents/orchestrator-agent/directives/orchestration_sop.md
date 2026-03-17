# Orchestration SOP (Standard Operating Procedure)

## Goal
To manage the multi-agent workflow for the morning routine, ensuring data flows correctly between extraction and analysis layers.

## Protocol

### 1. Initialization
- Notify the user: "Starting your morning routine. Orchestrating DevWorkflow and PM agents..."

### 2. Stage 1: Extraction (DevWorkflow)
- Communicate with `DevWorkflow`: "Please perform GWS triage and agenda extraction."
- Wait for output: `raw_gmail_data`, `raw_calendar_data`.

### 3. Stage 2: Analysis (PM Agent)
- Communicate with `PM Agent`: "Analyze this data: [raw_data]. Create a prioritized standup report."
- Wait for output: `final_report`.

### 4. Stage 3: Delivery
- Present `final_report` to User.
- Ask: "Would you like me to take any immediate actions based on this report?"

## Error Handling
- If `DevWorkflow` fails: Ask user if they want to manually trigger the GWS tools.
- If `PM Agent` fails: Attempt to present the raw data in a structured format as a fallback.
