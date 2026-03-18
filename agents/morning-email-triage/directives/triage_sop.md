# Email Triage Guidelines (SOP)

## 1. Goal
To efficiently analyze the morning inbox, categorize messages for the daily briefing, and ensure that all items requiring action (Actionable) are tracked as tasks.

## 2. Data Retrieval
- Execute the `gws gmail +triage` command.
- Capture and analyze the output, focusing strictly on `Sender`, `Subject`, and `Snippet`.

## 3. Classification Logic
Strictly classify each read email into one of the 4 categories below:

### A. Important Emails (Actionable)
*Definition:* Emails from clients, teammates, critical system alerts, or direct approval requests.
*Verification Rule 1:* If you are unsure whether a sender is important, use the GWS `people` service via MCP to search the user's contacts for the sender's email address. If a match is found, the email is automatically Actionable.
*Verification Rule 2:* If the email is a reply within a conversation/thread where the user has previously sent a message, it is automatically Actionable.
*Handling:* Require careful reading and immediate action. These are the top priority of the day.

### B. Informational Emails (Others)
*Definition:* Internal company updates, non-urgent reports, system notifications, or automated receipts.
*Handling:* Review the general content, then ignore. They do not require direct action.

### C. Newsletters and News
*Definition:* Periodic informational content (bulletins, weekly blog summaries) focused on passive reading.
*Handling:* Ignore for task creation purposes.

### D. Promotions (Marketing)
*Definition:* Emails with sales intent, discounts, service offers, or cold outreach.
*Handling:* Completely ignore for task creation purposes.

## 4. Execution & Summarization
- **For Actionable (Important) items:**
    - Clearly identify them in the summary.
    - Run the `gws workflow +email-to-task` command for each one, providing the context from the email when creating the task.
- **For the Summary (Briefing):**
    - List the "Important Emails" by name, explaining in one line why they need attention.
    - Group the other three categories (Informational, Newsletters, Promotions) in a purely quantitative and concise manner (e.g., *"You also received 3 newsletters, 2 informational reports, and 5 promotions"*).
- Log the completion of the triage.

## 5. Error Handling
- If the GWS tool fails or returns an error, notify the user immediately so the execution is halted.
- If no unread emails are found, report a "Clean inbox" and skip the categorization and task creation steps.