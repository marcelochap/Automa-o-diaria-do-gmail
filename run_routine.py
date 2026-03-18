import os
import sys
import json
import subprocess
from datetime import datetime

# Add paths for imports
BASE_DIR = r'c:\Projetos Antigravity\Projetos Python\Projeto Automação de Email'
sys.path.append(os.path.join(BASE_DIR, 'agents', 'morning-email-triage', 'execution'))
sys.path.append(os.path.join(BASE_DIR, 'agents', 'daily-standup-generator', 'execution'))
sys.path.append(os.path.join(BASE_DIR, 'agents', 'morning-briefing-ui', 'execution'))

from gmail_triage import list_unread_messages
from calendar_standup import generate_standup
from format_briefing import format_briefing

GWS_CMD = 'gws.cmd' if sys.platform == 'win32' else 'gws'

def ensure_label(label_name):
    """Checks if a label exists, if not, creates it."""
    try:
        # List labels
        list_args = [GWS_CMD, 'gmail', 'users', 'labels', 'list', '--params', '{"userId": "me"}', '--format', 'json']
        result = subprocess.run(list_args, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f">>> GWS Erro listar etiquetas: {result.stdout.strip()}")
            return None
            
        labels = json.loads(result.stdout).get('labels', [])
        
        for lb in labels:
            if lb['name'] == label_name:
                return lb['id']
        
        # Create label
        print(f"Criando etiqueta: {label_name}...")
        create_args = [
            GWS_CMD, 'gmail', 'users', 'labels', 'create',
            '--params', '{"userId": "me"}',
            '--json', json.dumps({"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"})
        ]
        create_result = subprocess.run(create_args, capture_output=True, text=True, encoding='utf-8')
        if create_result.returncode != 0:
            print(f">>> GWS Erro criar etiqueta {label_name}: {create_result.stdout.strip()}")
            return None
            
        return json.loads(create_result.stdout)['id']
    except Exception as e:
        print(f"Erro python ao gerenciar etiqueta {label_name}: {e}")
        return None

def archive_and_label(msg_ids, label_id):
    """Labels and archives (removes INBOX) a list of messages."""
    if not msg_ids or not label_id:
        return
    
    print(f"Arquivando {len(msg_ids)} emails com a etiqueta {label_id}...")
    for msg_id in msg_ids:
        modify_args = [
            GWS_CMD, 'gmail', 'users', 'messages', 'modify',
            '--params', json.dumps({"userId": "me", "id": msg_id}),
            '--json', json.dumps({
                "addLabelIds": [label_id],
                "removeLabelIds": ["INBOX"]
            })
        ]
        try:
            res = subprocess.run(modify_args, capture_output=True, text=True)
            if res.returncode != 0:
                print(f">>> GWS Erro ao arquivar mensagem {msg_id}: {res.stdout.strip()}")
        except Exception as e:
            print(f">>> Erro python ao arquivar {msg_id}: {e}")

def main():
    print("--- Iniciando Rotina Matinal (SEM LIMITES + ARQUIVAMENTO CONDICIONAL) ---")
    
    # 1. Triage Emails
    print("\n1. Triagem de E-mails...")
    triage_results = list_unread_messages()
    
    # 2. Extract Calendars
    print("\n2. Extração de Calendários...")
    agenda_results = generate_standup()
    
    # 3. Format Briefing
    print("\n3. Gerando Briefing HTML...")
    full_data = {
        "agenda": agenda_results,
        "critical_emails": triage_results["critical_emails"],
        "normal_emails": triage_results["normal_emails"],
        "stats": triage_results["stats"],
        "the_news_briefing": triage_results["the_news_briefing"],
        "full_list": triage_results["full_list"],
        "processed_log": triage_results["processed_log"]
    }
    
    html_content = format_briefing(full_data)
    
    # Save local copy
    report_path = os.path.join(BASE_DIR, 'morning_briefing.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Relatório salvo em: {report_path}")
    
    # 4. Enviar E-mail via GWS CLI (Upload)
    print("\n4. Enviando E-mail via GWS CLI (Upload)...")
    subject = f"Briefing Matinal - {datetime.now().strftime('%d/%m/%Y')}"
    
    rfc_path = os.path.join(BASE_DIR, 'final_message.rfc822')
    with open(rfc_path, 'w', encoding='utf-8') as f:
        f.write(f"To: marcelo.leite.engcivil@gmail.com\n")
        f.write(f"Subject: {subject}\n")
        f.write("Content-Type: text/html; charset=utf-8\n")
        f.write("\n")
        f.write(html_content)

    send_args = [
        GWS_CMD, 'gmail', 'users', 'messages', 'send',
        '--params', '{"userId": "me"}',
        '--upload', rfc_path,
        '--upload-content-type', 'message/rfc822'
    ]
    
    try:
        result = subprocess.run(send_args, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("E-mail enviado com sucesso via API!")
            
            # 5. Label and Archive (ONLY for identified non-critical IDs)
            target_label = "Processado/Rotina Matinal"
            label_id = ensure_label(target_label)
            
            archive_ids = triage_results.get("to_archive_ids", [])
            if archive_ids:
                archive_and_label(archive_ids, label_id)
            else:
                print("Nenhum e-mail para arquivar (apenas importantes ou nenhum processo).")
            
        else:
            print(f"Erro ao enviar e-mail: {result.stderr}")
    except Exception as e:
        print(f"Falha no processo de envio: {e}")
    finally:
        if os.path.exists(rfc_path):
            os.remove(rfc_path)

if __name__ == "__main__":
    main()
