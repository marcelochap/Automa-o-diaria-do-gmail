import random

def format_briefing(data):
    """
    Converts structured briefing data into an elegant "Premium Minimalism v2" HTML template.
    Refinements: Improved spacing, softer colors, higher readability, no email IDs in log.
    """
    
    # 1. GREETING & MOTIVATION
    motivations = [
        "A persistência é o caminho do êxito.",
        "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
        "Não espere por oportunidades, crie-as.",
        "Sua única limitação é aquela que você impõe em sua própria mente.",
        "Que hoje seja um dia de grandes conquistas e foco total no que importa."
    ]
    motivation = random.choice(motivations)
    
    # Design Tokens
    bg_body = "#f8fafc"
    bg_card = "#ffffff"
    text_primary = "#1e293b"
    text_secondary = "#64748b"
    accent_blue = "#3b82f6"
    accent_red = "#ef4444"
    bg_critical = "#fef2f2"
    border_color = "#e2e8f0"
    
    # Base CSS Wrapper
    container_style = f"""
        background-color: {bg_body};
        font-family: 'Segoe UI', Arial, sans-serif;
        color: {text_primary};
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
        padding: 40px 20px;
    """
    
    card_style = f"""
        background-color: {bg_card};
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {border_color};
    """
    
    h3_style = f"""
        font-size: 18px;
        font-weight: 700;
        color: {text_primary};
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid {border_color};
    """
    
    hr_style = f"border: 0; border-top: 1px solid {border_color}; margin: 40px 0;"
    
    html = f"""
    <div style="{container_style}">
        <div style="{card_style}">
            <!-- 1. GREETING & MOTIVATION -->
            <h3 style="margin-top: 0; font-size: 24px;">Bom dia,</h3>
            <p style="font-style: italic; color: {text_secondary}; font-size: 16px; margin-bottom: 0;">"{motivation}"</p>
            <div style="{hr_style}"></div>

            <!-- 2. AGENDA DE HOJE -->
            <h3 style="{h3_style}">📅 Agenda de Hoje</h3>
    """
    
    if not data.get('agenda'):
        html += f'<p style="color: {text_secondary};">Nenhum compromisso agendado para hoje.</p>'
    else:
        html += '<ul style="list-style: none; padding: 0; margin: 0;">'
        for event in data['agenda']:
            time = event.get('time', '00:00')
            title = event.get('title', 'Sem Título')
            html += f"""
                <li style="margin-bottom: 12px; font-size: 15px;">
                    <span style="font-weight: 700; color: {accent_blue}; width: 60px; display: inline-block;">{time}</span>
                    <span style="color: {text_primary};"> – {title}</span>
                </li>
            """
        html += '</ul>'
    
    html += f"""
            <div style="{hr_style}"></div>

            <!-- RESUMO DAS CATEGORIAS (SOP) -->
            <h3 style="{h3_style}">📊 Resumo da Caixa de Entrada</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
    """
    
    stats = data.get('stats', {"Importante": 0, "Promoção": 0, "Newsletter": 0, "Outros": 0})
    
    categories_info = [
        ("🚨 Importantes", stats.get("Importante", 0), accent_red, bg_critical, "Ação imediata. Clientes, equipe, alertas críticos ou aprovações."),
        ("ℹ️ Outros (Infos)", stats.get("Outros", 0), text_secondary, "#f1f5f9", "Sem ação. Informes internos, alertas do sistema ou recibos."),
        ("📰 Newsletters", stats.get("Newsletter", 0), "#854d0e", "#fefce8", "Leitura passiva. Boletins e informativos."),
        ("🏷️ Promoções", stats.get("Promoção", 0), "#16a34a", "#f0fdf4", "Ignorados. Ofertas, descontos, vendas.")
    ]
    
    for title, count, color, bg, desc in categories_info:
        html += f"""
                <div style="background-color: {bg}; padding: 15px; border-radius: 8px; border-left: 4px solid {color};">
                    <div style="font-weight: bold; color: {color}; font-size: 14px; margin-bottom: 2px;">
                        {title}: <span style="font-size: 16px;">{count}</span>
                    </div>
                    <div style="font-size: 11px; color: {text_secondary}; line-height: 1.4;">
                        {desc}
                    </div>
                </div>
        """
        
    html += "</div>"
    
    html += f"""
            <div style="{hr_style}"></div>

            <!-- 3. EMAILS IMPORTANTES -->
            <h3 style="{h3_style}">🚨 Emails Importantes (Ação Imediata)</h3>
    """
    
    critical = data.get('critical_emails', [])
    if not critical:
        html += f'<p style="color: {text_secondary}; font-style: italic;">Nenhum email crítico encontrado hoje.</p>'
    else:
        for email in critical:
            sender = email.get('from', 'Desconhecido').split('<')[0].strip()
            subject = email.get('subject', 'Sem Assunto')
            html += f"""
            <div style="border-left: 4px solid {accent_red}; background-color: {bg_critical}; padding: 15px 20px; border-radius: 4px; margin-bottom: 15px;">
                <div style="font-size: 12px; text-transform: uppercase; color: {accent_red}; font-weight: 700; margin-bottom: 5px;">Prioridade Alta</div>
                <div style="font-weight: 700; color: {text_primary};">{sender}</div>
                <div style="color: #444; font-size: 14px;">{subject}</div>
            </div>
            """
            
    html += f"""
            <div style="{hr_style}"></div>

            <!-- 4. RESUMO DE NOTÍCIAS -->
            <h3 style="{h3_style}">📰 Resumo de Notícias & Newsletters</h3>
    """
    
    news = data.get('the_news_briefing', '')
    if not news:
        html += f'<p style="color: {text_secondary};">Nenhuma newsletter processada nas últimas 24h.</p>'
    else:
        html += f"""
            <div style="background-color: #fefce8; border: 1px solid #fef08a; padding: 15px; border-radius: 8px;">
                <div style="font-weight: 700; color: #854d0e; margin-bottom: 5px;">☕ The News & Briefing</div>
                <div style="font-size: 14px; color: #713f12;">{news}</div>
            </div>
        """
        
    html += f"""
            <div style="{hr_style}"></div>

            <!-- 5. RESUMO DOS EMAILS (GERAL) -->
            <h3 style="{h3_style}">✉️ Resumo dos Emails (Geral)</h3>
    """
    
    normal = data.get('normal_emails', [])
    if not normal:
        html += f'<p style="color: {text_secondary};">Nenhum outro e-mail processado.</p>'
    else:
        html += '<ul style="padding-left: 0; list-style: none; margin: 0;">'
        for item in normal[:10]:
            cat = item.get('category', 'Outros')
            subj = item.get('subject', 'Sem Assunto')
            html += f"""
                <li style="margin-bottom: 10px; font-size: 14px; padding-left: 15px; border-left: 2px solid {border_color};">
                    <span style="font-weight: 700; font-size: 11px; text-transform: uppercase; color: {text_secondary}; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; margin-right: 8px;">{cat}</span>
                    <span style="color: {text_primary};">{subj}</span>
                </li>
            """
        html += '</ul>'

    html += f"""
            <div style="{hr_style}"></div>

            <!-- 6. LISTA DE EMAILS PROCESSADOS (LOG) -->
            <h3 style="{h3_style}">🛠️ Lista de Emails Processados (Log)</h3>
            <div style="font-family: 'Courier New', monospace; font-size: 12px; color: {text_secondary}; background-color: #f1f5f9; padding: 20px; border-radius: 8px;">
    """
    
    for log in data.get('processed_log', []):
        subj = log.get('subject', '---')
        # Usuário solicitou remover o ID (id_...)
        html += f'• {subj}<br>'
        
    html += f"""
            </div>
            
            <p style="text-align: center; color: {text_secondary}; font-size: 12px; margin-top: 60px;">
                Monitor Matinal por AG-Orchestrator<br>
                <span style="font-weight: 700; color: {accent_blue};">DESIGN PREMIUM v2.0</span>
            </p>
        </div>
    </div>
    """
    
    return html

if __name__ == "__main__":
    test_data = {
        "agenda": [
            {"time": "09:00", "title": "Reunião de Alinhamento"},
            {"time": "14:30", "title": "Foco em Desenvolvimento"}
        ],
        "critical_emails": [
            {"from": "Banco Inter", "subject": "Boleto Vencendo Hoje"},
            {"from": "Diretoria", "subject": "Atualização do Projeto Alpha"}
        ],
        "normal_emails": [
            {"category": "Newsletter", "subject": "Tendências de IA em 2026"},
            {"category": "Promoção", "subject": "Ofertas Exclusivas de Verão"}
        ],
        "the_news_briefing": "O mercado de tecnologia mantém crescimento estável, com destaque para novos semicondutores.",
        "processed_log": [
            {"subject": "Confirmação de Reserva"},
            {"subject": "Newsletter Diária"}
        ],
        "stats": {
            "Total": 6,
            "Importante": 2,
            "Promoção": 1,
            "Newsletter": 1,
            "Outros": 2
        }
    }
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(format_briefing(test_data))
