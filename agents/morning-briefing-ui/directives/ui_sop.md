# SOP: Morning Briefing UI Formatting

## Overview
This directive defines the visual standards for the morning briefing email. The goal is "Premium Minimalism v2", adapting UI/UX Pro Max principles to inline CSS limitations.

## Strict Order Requirements

Follow this exact structure when generating or reviewing the briefing:

1.  **GREETING & MOTIVATION**
    * Display "Bom dia," followed by an inspiring motivational quote in italics.

2.  **AGENDA DE HOJE**
    * Section header: `📅 Agenda de Hoje`
    * Display an unordered list of the user's appointments (`HH:MM - Título`). Provide a fallback message if empty.

3.  **RESUMO DA CAIXA DE ENTRADA**
    * Section header: `📊 Resumo da Caixa de Entrada`
    * Display a summary table/grid with counts for: Importantes, Outros (Infos), Newsletters, and Promoções.

4.  **EMAILS IMPORTANTES**
    * Section header: `🚨 Emails Importantes (Ação Imediata)`
    * Render each critical email alerting the user to priority actions. Provide a fallback message if empty.

5.  **TOP 5 NOTÍCIAS**
    * Section header: `📰 Top 5 Notícias do Dia`
    * Provide an ordered list (`<ol>`) of the top 5 relevant news items.

6.  **RADAR DE PROMOÇÕES E VIAGENS**
    * Section header: `🏷️ Radar de Promoções e Viagens`
    * Display highlighted promotions and a clean interface for monitored flight prices.

7.  **RESUMO DOS EMAILS VALIDADOS**
    * Section header: `✉️ Resumo dos Emails Validados`
    * Render a **single generated text paragraph** summarizing the non-critical emails (what was read, important themes, etc). **Do not use bullet lists for normal emails.** Provide a fallback message if empty.

8.  **LOG DE EMAILS PROCESSADOS**
    * Section header: `🛠️ Log de Emails Processados`
    * Present a raw monospace log of all processed email subjects (do not show IDs).

## Visual Directives
- Apply UI/UX Pro Max elements via safe inline CSS.
- Ensure appropriate spacing (`margin`, `padding`), soft borders, readable fonts without external web fonts.
- Use explicit visual hierarchy (titles > lists > metadata).
