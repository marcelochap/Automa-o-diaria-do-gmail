import random
import json
import os

def load_motivations():
    """Loads motivations from assets/motivations.json with a safe fallback."""
    try:
        # Resolve path relative to this script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # go up to project root then assets
        root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
        json_path = os.path.join(root_dir, "assets", "motivations.json")
        
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load motivations.json: {e}")
    
    # Fallback if file is missing or error occurs
    return ["Que hoje seja um dia de grandes conquistas e foco total no que importa."]

def format_briefing(data):
    """
    Converts structured briefing data into an elegant "Premium Minimalism v2" HTML template.
    Refinements: Improved spacing, softer colors, higher readability, no email IDs in log.
    """
    
    # 1. GREETING & MOTIVATION
    motivations = load_motivations()
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

            <!-- 3. RESUMO DA CAIXA DE ENTRADA -->
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

            <!-- 4. EMAILS IMPORTANTES -->
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

            <!-- 5. TOP 5 NOTICIAS -->
            <h3 style="{h3_style}">📰 Top Notícias do Dia</h3>
    """
    
    top_news = data.get('top_news', [])
    if not top_news:
        html += f"""
            <div style="background-color: #f8fafc; border: 1px solid {border_color}; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <p style="margin: 0; color: {text_secondary}; font-style: italic; font-size: 14px;">Nenhuma newsletter de notícias processada hoje.</p>
            </div>
        """
    else:
        html += f"""
            <div style="background-color: #f8fafc; border: 1px solid {border_color}; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <ul style="margin: 0; padding-left: 10px; list-style-type: none; color: #334155; font-size: 14px; line-height: 1.5;">
        """
        for count, news in enumerate(top_news):
            source = news.get("source", "Newsletter")
            title = news.get("title", "Sem título")
            snippet = news.get("snippet", "")
            
            # Remover a borda inferior do ultimo item para o design ficar perfeito
            li_style = "margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 15px;" if count < len(top_news)-1 else "margin-bottom: 0;"
            
            html += f"""
                    <li style="{li_style}">
                        <span style="font-weight: 700; color: {accent_blue}; text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px;">{source}</span><br>
                        <strong style="color: {text_primary}; font-size: 15px;">{title}</strong><br>
                        <span style="color: {text_secondary}; display: block; margin-top: 6px;">{snippet}</span>
                    </li>
            """
        html += """
                </ul>
            </div>
        """
        
    html += f"""
            <div style="{hr_style}"></div>

            <!-- 6. RADAR DE PROMOCOES E VIAGENS -->
            <h3 style="{h3_style}">🏷️ Radar de Promoções e Viagens</h3>
            
            <div style="background-color: #f8fafc; border: 1px solid {border_color}; border-left: 4px solid {accent_blue}; padding: 15px 20px; border-radius: 8px; margin-bottom: 15px;">
                <div style="font-size: 12px; text-transform: uppercase; color: {accent_blue}; font-weight: 700; margin-bottom: 8px;">✈️ Passagens Monitoradas</div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid {border_color}; padding-bottom: 10px; margin-bottom: 10px;">
                    <div>
                        <div style="font-weight: 700; color: {text_primary}; font-size: 15px;">Brasília (BSB) ➔ São Paulo (GRU)</div>
                        <div style="color: {text_secondary}; font-size: 13px;">Latam - 15 Abr a 18 Abr</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background-color: #dcfce7; color: #166534; font-weight: 700; padding: 4px 8px; border-radius: 6px; font-size: 14px;">R$ 485 📉</span>
                    </div>
                </div>
            </div>

            <div style="background-color: #ffffff; border: 1px solid {border_color}; border-left: 4px solid #10b981; padding: 15px 20px; border-radius: 8px;">
                <div style="font-size: 12px; text-transform: uppercase; color: #10b981; font-weight: 700; margin-bottom: 8px;">🛍️ Ofertas em Destaque</div>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    <li style="font-size: 14px; color: #334155;"><strong>Ofertas de hoje:</strong> Não deixe de conferir seus e-mails promocionais.</li>
                </ul>
            </div>
            <div style="{hr_style}"></div>

            <!-- 7. RESUMO DOS EMAILS (PARAGRAFO) -->
            <h3 style="{h3_style}">✉️ Resumo dos Emails Validados</h3>
    """
    
    summary_paragraph = data.get('normal_emails_summary', "Não houve resumo gerado para os e-mails normais hoje.")
    html += f"""
            <div style="background-color: #f1f5f9; padding: 20px; border-radius: 8px; font-size: 15px; color: #334155; line-height: 1.6; border-left: 4px solid {text_secondary};">
                <strong>Resumo:</strong> {summary_paragraph}
            </div>
            <div style="{hr_style}"></div>

            <!-- 8. LOG DE EMAILS PROCESSADOS -->
            <h3 style="{h3_style}">🛠️ Log de Emails Processados</h3>
            <div style="font-family: 'Courier New', monospace; font-size: 12px; color: {text_secondary}; background-color: #f1f5f9; padding: 20px; border-radius: 8px;">
    """
    
    for log in data.get('processed_log', []):
        subj = log.get('subject', '---')
        html += f'• {subj}<br>'
        
    html += f"""
            </div>
            
            <p style="text-align: center; color: {text_secondary}; font-size: 12px; margin-top: 60px;">
                Monitor Matinal por AG-Orchestrator<br>
                <span style="font-weight: 700; color: {accent_blue};">DESIGN PREMIUM v2.0 UI/UX PRO MAX</span>
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
        "top_news": [
            {"source": "The News", "title": "As manchetes de hoje diretamente da nova Faria Lima", "snippet": "A bolsa operou em alta hoje com as decisões econômicas reveladas após..."},
            {"source": "G1", "title": "G1 em 1 minuto", "snippet": "As principais atualizações da manhã e o clima pelo país nesta terça-feira chuvosa..."}
        ],
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
