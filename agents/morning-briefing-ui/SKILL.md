---
name: morning-briefing-ui
description: Formata os dados do briefing matinal em um template HTML limpo e responsivo para ser enviado e lido diretamente no Gmail. Ativado pelo Frontend Agent.
category: UI/UX
risk: safe
tags: [html, email, formatting, briefing]
date_added: "2026-03-16"
---

# morning-briefing-ui

## Purpose
Convert structured data analysis (emails, schedule, news) into a premium, minimalist HTML email template optimized for Gmail reading.

## Trigger Phrases
- "format my morning briefing"
- "generate briefing HTML"
- "prepare morning routine email"

## Core Capabilities
- **HTML Generation**: Creates Gmail-safe HTML using inline CSS.
- **Sectioning**: Organizes Agenda, Email Summaries, News, and Critical Alerts.
- **Micro-copy**: Generates short, motivational phrases.

## Instructions
1.  **Input**: Receive structured JSON or text from the PM Agent containing:
    - Calendar events (Agenda)
    - Normal email summaries
    - News/Newsletter summaries
    - Critical email alerts (Important)
2.  **Formatting**: Follow `directives/ui_sop.md` for strict layout and style rules.
3.  **Output**: Deliver a single string containing the full HTML code.

## Constraints
- Use **only inline CSS**.
- No `<script>` or advanced CSS features not supported by Gmail.
- Do not invent data; strictly use provided analysis.
