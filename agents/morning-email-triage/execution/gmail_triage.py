import subprocess
import json
import os
import sys
import re
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
        res = subprocess.run(modify_args, capture_output=True, text=True, env=env, encoding='utf-8')
        if res.returncode != 0:
            print(f">>> GWS Erro ao marcar como lido {msg_id}: {res.stdout.strip()}")
            return False
        return True
    except Exception as e:
        print(f">>> Erro python ao marcar {msg_id} como lido: {e}")
        return False

def fetch_all_contacts(env):
    """Fetches all known contact email addresses from Google People API."""
    print("Fetching contacts via People API...")
    args = [
        GWS_CMD, 'people:v1', 'people', 'connections', 'list',
        '--params', json.dumps({"resourceName": "people/me", "personFields": "emailAddresses", "pageSize": 1000}),
        '--format', 'json'
    ]
    try:
        res = subprocess.run(args, capture_output=True, text=True, env=env, encoding='utf-8')
        if res.returncode != 0:
            print(f">>> GWS Erro ao acessar contatos: {res.stdout.strip()}")
            return set()
            
        data = json.loads(res.stdout)
        connections = data.get('connections', [])
        
        emails = set()
        for person in connections:
            for email_obj in person.get('emailAddresses', []):
                val = email_obj.get('value')
                if val:
                    emails.add(val.lower().strip())
        print(f"Loaded {len(emails)} contacts.")
        return emails
    except Exception as e:
        print(f">>> Erro python ao acessar contatos: {e}")
        return set()

def extract_email(sender_header):
    match = re.search(r'<([^>]+)>', sender_header)
    if match:
        return match.group(1).lower().strip()
    return sender_header.lower().strip()

def check_if_user_replied(thread_id, env):
    """Verifies if the user sent any message in the given thread."""
    args = [
        GWS_CMD, 'gmail', 'users', 'threads', 'get',
        '--params', json.dumps({"userId": "me", "id": thread_id})
    ]
    try:
        res = subprocess.run(args, capture_output=True, text=True, env=env, encoding='utf-8')
        if res.returncode == 0:
            data = json.loads(res.stdout)
            for m in data.get('messages', []):
                if "SENT" in m.get('labelIds', []):
                    return True
    except Exception:
        pass
    return False

def list_unread_messages():
    env = os.environ.copy()
    
class TriageResult:
    """Class to store triage results with explicit types to satisfy linters."""
    def __init__(self):
        self.stats = {"Total": 0, "Importante": 0, "Promoção": 0, "Newsletter": 0, "Outros": 0}
        self.critical_emails = []
        self.normal_emails = []
        self.normal_emails_summary = ""
        self.the_news_briefing = ""
        self.top_news = []
        self.full_list = []
        self.processed_log = []
        self.to_archive_ids = []
        self.flight_deals = []
        self.shopping_deals = []

    def to_dict(self):
        return {
            "stats": self.stats,
            "critical_emails": self.critical_emails,
            "normal_emails": self.normal_emails,
            "normal_emails_summary": self.normal_emails_summary,
            "the_news_briefing": self.the_news_briefing,
            "top_news": self.top_news,
            "full_list": self.full_list,
            "processed_log": self.processed_log,
            "to_archive_ids": self.to_archive_ids,
            "flight_deals": self.flight_deals,
            "shopping_deals": self.shopping_deals
        }

def list_unread_messages():
    env = os.environ.copy()
    
    # 500 results is usually enough for a daily routine
    list_args = [
        GWS_CMD, 'gmail', 'users', 'messages', 'list',
        '--params', json.dumps({"userId": "me", "labelIds": ["UNREAD"], "maxResults": 500})
    ]
    
    result_obj = TriageResult()
    
    try:
        print("Fetching unread messages...")
        res = subprocess.run(list_args, capture_output=True, text=True, check=True, env=env, encoding='utf-8')
        data = json.loads(res.stdout)
        messages = data.get('messages', [])
        
        if not messages:
            print("No unread messages found.")
            return result_obj.to_dict()

        result_obj.stats["Total"] = len(messages)
        
        user_contacts = fetch_all_contacts(env)

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
            
            result_obj.processed_log.append({"id": msg_id, "subject": subject})
            result_obj.full_list.append({"from": sender, "subject": subject})
            
            # Categorization Logic
            category = "Outros"
            is_critical = False
            
            sender_lower = sender.lower()
            subject_lower = subject.lower()
            sender_email = extract_email(sender)
            
            # 1. Authorizations/Alçadas are NOT critical per user request
            if "alçada" in subject_lower:
                category = "Outros"
                is_critical = False
            # 2. Hardcoded Critical
            elif any(k in sender_lower for k in ["nubank", "prefeitura", "banco", "diretoria"]) or \
                 any(k in subject_lower for k in ["boleto", "vencimento", "fatura", "pagar", "atraso", "urgente"]):
                category = "Importante"
                is_critical = True
                result_obj.stats["Importante"] += 1
            # 3. User Reply Check
            elif check_if_user_replied(msg_data.get("threadId"), env):
                category = "Importante"
                is_critical = True
                result_obj.stats["Importante"] += 1
                print(f"Reply detected for thread: {subject[:30]}")
            # 4. Known Contact check
            elif sender_email in user_contacts:
                category = "Importante"
                is_critical = True
                result_obj.stats["Importante"] += 1
            # 5. Newsletters
            elif "news" in sender_lower or "newsletter" in sender_lower or "briefing" in subject_lower or "morning" in subject_lower or "g1" in sender_lower or "cnn" in sender_lower:
                category = "Newsletter"
                result_obj.stats["Newsletter"] += 1
                if "the news" in sender_lower:
                    result_obj.the_news_briefing = snippet
                
                if any(x in sender_lower for x in ["the news", "g1", "cnn"]) or "newsletter" in sender_lower:
                    if len(result_obj.top_news) < 5:
                        source = "The News" if "the news" in sender_lower else "G1" if "g1" in sender_lower else "CNN" if "cnn" in sender_lower else "Newsletter"
                        clean_snippet = snippet[:120].strip() + "..." if len(snippet) > 120 else snippet.strip()
                        result_obj.top_news.append({
                            "source": source,
                            "title": subject,
                            "snippet": clean_snippet,
                            "id": msg_id
                        })
            # 6. Promotions
            elif any(k in sender_lower for k in ["shein", "aliexpress", "shopee", "amazon", "magalu", "mercado", "latam", "gol", "azul", "decolar", "123milhas", "maxmilhas", "skyscanner", "kayak"]) or \
                 any(k in subject_lower for k in ["promo", "oferta", "desconto", "cupom", "sale", "passagem", "voo", "aérea"]):
                 category = "Promoção"
                 result_obj.stats["Promoção"] += 1
                 
                 price_match = re.search(r'R\$\s*[\d\.,]+', subject + " " + snippet)
                 price_str = price_match.group(0) if price_match else "Preço no email"
                 
                 source_name = sender.split('<')[0].strip() if '<' in sender else sender
                 
                 if any(k in sender_lower for k in ["latam", "gol", "azul", "decolar", "skyscanner", "kayak", "123milhas", "maxmilhas"]) or \
                    any(k in subject_lower for k in ["passagem", "voo", "aérea"]):
                     result_obj.flight_deals.append({
                         "source": source_name,
                         "description": subject,
                         "price": price_str
                     })
                 else:
                     result_obj.shopping_deals.append({
                         "source": source_name,
                         "description": subject,
                         "price": price_str
                     })
            # 7. Others
            else:
                category = "Outros"
                result_obj.stats["Outros"] += 1

            email_info = {"from": sender, "subject": subject, "snippet": snippet, "category": category}
            
            if is_critical:
                result_obj.critical_emails.append(email_info)
                print(f"KEEPING INBOX: {subject[:30]}... ({category})")
            else:
                result_obj.normal_emails.append({"category": category, "from": sender, "subject": subject})
                result_obj.to_archive_ids.append(msg_id)
                mark_as_read(msg_id, env)
                print(f"Processed: {subject[:30]}... ({category})")

    except subprocess.CalledProcessError as e:
        print(f"Error executing gws: {e.stderr}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Data error: {e}")
    
    # Narrative Summary Generation
    if result_obj.normal_emails:
        subjects_for_summary = []
        for e in result_obj.normal_emails[:2]:
            subj = e.get("subject", "Sem Assunto")
            truncated = f"'{subj[:40]}...'" if len(subj) > 40 else f"'{subj}'"
            subjects_for_summary.append(truncated)
            
        subj_str = " e ".join(subjects_for_summary) if subjects_for_summary else "emails diversos"
        
        result_obj.normal_emails_summary = (
            f"Nas últimas 24 horas, recebemos {result_obj.stats['Outros']} notificações gerais e {result_obj.stats['Newsletter']} newsletters. "
            f"Destacam-se informes como {subj_str}, que compõem as leituras do dia. "
            "Todos os emails não críticos já constam como lidos e foram devidamente arquivados conforme sua triagem."
        )
    else:
        result_obj.normal_emails_summary = "Não houve e-mails de rotina, automações ou informes gerais para revisar na sua triagem de hoje."
    
    return result_obj.to_dict()

if __name__ == "__main__":
    routine_result = list_unread_messages()
    print(json.dumps(routine_result, indent=2))
