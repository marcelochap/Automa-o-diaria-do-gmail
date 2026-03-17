# Triage SOP (Standard Operating Procedure)

## Goal
To efficiently triage the morning inbox and ensure all actionable items are tracked as tasks.

## Protocol

### 1. Data Retrieval
- Execute `gws gmail +triage`.
- Capture the output, focusing on `Sender`, `Subject`, and `Snippet`.

### 2. Classification Logic
- **Actionable**: Emails from clients, teammates, or urgent system alerts.
- **Informational**: Internal updates, non-urgent reports (Review, then ignore).
- **Ignore**: Newsletters, receipts, marketing.

### 3. Execution
- For each **Actionable** item:
    - Run `gws workflow +email-to-task`.
    - Provide the context from the email.
- Log completion of the triage.

## Error Handling
- If the GWS tool fails, notify the user immediately.
- If no unread emails are found, report a clean inbox.
