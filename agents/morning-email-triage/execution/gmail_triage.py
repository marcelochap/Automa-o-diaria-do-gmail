import subprocess
import json
import os
import sys
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

GWS_CMD = 'gws.cmd' if sys.platform == 'win32' else 'gws'

def mark_as_read(msg_id, env):
    """Removes the UNREAD label from a message."""
    modify_args = [
        GWS_CMD, 'gmail', 'users', 'messages', 'modify',
        '--params', json.dumps({"userId": "me", "id": msg_id}),
        '--json', json.dumps({"removeLabelIds": ["UNREAD"]})
    ]
    try:
        subprocess.run(modify_args, capture_output=True, text=True, check=True, env=env)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error marking message {msg_id} as read: {e.stderr}")
        return False

def list_unread_messages():
    env = os.environ.copy()
    
    # 500 results is usually enough for a daily routine
    list_args = [
        GWS_CMD, 'gmail', 'users', 'messages', 'list',
        '--params', json.dumps({"userId": "me", "labelIds": ["UNREAD"], "maxResults": 500})
    ]
    
    triage_data = {
        "stats": {"Total": 0, "Importante": 0, "Promoção": 0, "Newsletter": 0, "Outros": 0},
        "critical_emails": [],
        "normal_emails": [],
        "the_news_briefing": "",
        "full_list": [],
        "processed_log": [],      # For UI log
        "to_archive_ids": []      # IDs that SHOULD be archived (non-critical)
    }
    
    try:
        print("Fetching unread messages...")
        result = subprocess.run(list_args, capture_output=True, text=True, check=True, env=env, encoding='utf-8')
        data = json.loads(result.stdout)
        messages = data.get('messages', [])
        
        if not messages:
            print("No unread messages found.")
            return triage_data

        triage_data["stats"]["Total"] = len(messages)

        print(f"\n--- Processing {len(messages)} Messages ---")
        for msg in messages:
            msg_id = msg['id']
            get_args = [
                GWS_CMD, 'gmail', 'users', 'messages', 'get',
                '--params', json.dumps({"userId": "me", "id": msg_id})
            ]
            
            try:
                get_result = subprocess.run(get_args, capture_output=True, text=True, check=True, env=env, encoding='utf-8')
                msg_data = json.loads(get_result.stdout)
            except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
                print(f"Error fetching message {msg_id}: {e}")
                continue
            
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            snippet = msg_data.get('snippet', '')
            
            triage_data["processed_log"].append({"id": msg_id, "subject": subject})
            triage_data["full_list"].append({"from": sender, "subject": subject})
            
            # Categorization Logic
            category = "Outros"
            is_critical = False
            
            sender_lower = sender.lower()
            subject_lower = subject.lower()
            
            # IMPORTANT: Authorization emails are NOT critical
            if "alçada" in subject_lower:
                category = "Outros"
                is_critical = False
            elif any(k in sender_lower for k in ["nubank", "prefeitura", "banco", "diretoria"]) or \
                 any(k in subject_lower for k in ["boleto", "vencimento", "fatura", "pagar", "atraso", "urgente"]):
                category = "Importante"
                is_critical = True
                triage_data["stats"]["Importante"] += 1
            
            elif "news" in sender_lower or "newsletter" in sender_lower or "briefing" in subject_lower or "morning" in subject_lower:
                category = "Newsletter"
                triage_data["stats"]["Newsletter"] += 1
                if "the news" in sender_lower:
                    triage_data["the_news_briefing"] = snippet
            
            elif any(k in sender_lower for k in ["shein", "aliexpress", "shopee", "amazon", "magalu", "mercado"]) or \
                 any(k in subject_lower for k in ["promo", "oferta", "desconto", "cupom", "sale"]):
                 category = "Promoção"
                 triage_data["stats"]["Promoção"] += 1
            
            else:
                category = "Outros"
                triage_data["stats"]["Outros"] += 1

            email_info = {"from": sender, "subject": subject, "snippet": snippet, "category": category}
            
            if is_critical:
                triage_data["critical_emails"].append(email_info)
                # DO NOT mark as read, DO NOT add to to_archive_ids
                print(f"KEEPING INBOX: {subject[:30]}... ({category})")
            else:
                triage_data["normal_emails"].append({"category": category, "from": sender, "subject": subject})
                triage_data["to_archive_ids"].append(msg_id)
                # Mark as read for non-critical
                mark_as_read(msg_id, env)
                print(f"Processed: {subject[:30]}... ({category})")

    except subprocess.CalledProcessError as e:
        print(f"Error executing gws: {e.stderr}")
    except json.JSONDecodeError:
        print("Error parsing GWS output as JSON.")
    
    return triage_data

if __name__ == "__main__":
    result = list_unread_messages()
    print(json.dumps(result, indent=2))
