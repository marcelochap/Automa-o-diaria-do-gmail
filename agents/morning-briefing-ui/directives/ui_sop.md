# SOP: Morning Briefing UI Formatting

## Overview
This directive defines the visual standards for the morning briefing email. The goal is "Premium Minimalism".

## Structure Requirements (Strict Order)

Follow this structure exactly:

1.  ### GREETING & MOTIVATION
    * **Syntax:** Start with `### Bom dia,` on a new line.
    * **Content:** Immediately below, add a *short, inspiring motivational quote* of your own choice in Portuguese, enclosed in italics.
    * **Separator:** End this section with a horizontal rule (`---`).

2.  ### AGENDA DE HOJE
    * **Syntax:** Start with `### 📅 Agenda de Hoje` on a new line.
    * **Content:** Present a bulleted list of appointments in `**HH:MM** – Appointment Title` format. Use placeholders if no events exist.
    * **Separator:** End with a horizontal rule (`---`).

3.  ### EMAILS IMPORTANTES
    * **Syntax:** Start with `### 🚨 Emails Importantes (Ação Imediata)` on a new line.
    * **Content:** Present critical emails using Markdown blockquotes (`>`). Each blockquote must include: `**Remetente:** [Sender Name] | **Assunto:** [Subject Summary]`. If empty, note that no critical emails exist.
    * **Separator:** End with a horizontal rule (`---`).

4.  ### RESUMO DE NOTÍCIAS
    * **Syntax:** Start with `### 📰 Resumo de Notícias & Newsletters` on a new line.
    * **Content:** Group newsletters by theme. Present as a bulleted list: `* **[Theme Name]:** Concise main theme summary.`
    * **Separator:** End with a horizontal rule (`---`).

5.  ### RESUMO DOS EMAILS
    * **Syntax:** Start with `### ✉️ Resumo dos Emails (Geral)` on a new line.
    * **Content:** Present a bulleted list of concise summaries of non-critical, processed emails. Format: `* **[General Topic]:** Quick summary of action/information.`

6.  ### LISTA DE EMAILS PROCESSADOS
    * **Syntax:** Start with `### 🛠️ Lista de Emails Processados (Log)` on a new line.
    * **Content:** Provide a simple, raw log of all processed email IDs and brief descriptions using monospace text: ``* `id_[ID]` | [Subject Snippet]``.

## Style Guidelines

* **Tone:** Professional, organized, and encouraging.
* **Conciseness:** Crucial. Summaries must be extremely brief.
* **Scanning:** Use bold text (`**`) and emojis to guide the user’s eye quickly.
* **No placeholders:** Ensure real content is generated or clearly marked as "Nenhum compromisso/email hoje" if empty.



## HTML Structure
1.  **Greeting**: `<h1>Bom dia,</h1>`
2.  **Motivation**: `<p style="font-style: italic; color: #555;">[Motivational Phrase]</p>`
3.  **Sections**: Use `<h2>` for section headers with a bottom border or spacing.
4.  **Agenda**: Table or list with bold times.
5.  **Summaries**: Unordered lists for normal emails and news.
6.  **Important**: A `div` with a light red or yellow background (`#fff4f4` or `#fffde7`) and a border to highlight critical items.

## CSS Standards (Inline Only)
- **Font**: Sans-serif (Arial, Helvetica, sans-serif).
- **Body**: Max-width 600px, centered, padding 20px.
- **Colors**:
  - Headers: `#1a1a1a`
  - Text: `#333333`
  - Links: `#0066cc`
- **Spacing**: Margin-bottom 15px for paragraphs and 25px for headers.

## Verification
- Ensure all tags are closed.
- Ensure no external CSS or `<style>` blocks.
- Check mobile responsiveness (simple 1-column layout).
