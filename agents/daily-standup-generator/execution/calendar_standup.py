import subprocess
import json
import os
import sys
from datetime import datetime, time
import pytz
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

GWS_CMD = 'gws.cmd' if sys.platform == 'win32' else 'gws'

CALENDARS = {
    "Principal": "marcelo.leite.engcivil@gmail.com",
    "Harumi": "yukawa.harumi@gmail.com",
    "Diretoria": "diretoria@premoldadobrasil.com.br",
    "Manutenção": "0i23vfndiou4g3rogceqaqlf1o@group.calendar.google.com"
}

def get_events_for_calendar(calendar_id):
    # Today's boundaries in America/Sao_Paulo
    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(tz)
    
    start_of_day = tz.localize(datetime.combine(now.date(), time.min)).isoformat()
    end_of_day = tz.localize(datetime.combine(now.date(), time.max)).isoformat()
    
    args = [
        GWS_CMD, 'calendar', 'events', 'list',
        '--params', json.dumps({
            "calendarId": calendar_id,
            "timeMin": start_of_day,
            "timeMax": end_of_day,
            "singleEvents": True,
            "timeZone": "America/Sao_Paulo",
            "orderBy": "startTime"
        }),
        '--format', 'json'
    ]
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True, encoding='utf-8')
        data = json.loads(result.stdout)
        return data.get('items', [])
    except Exception as e:
        # Silently fail for individual calendars to not break the whole flow
        return []

def generate_standup():
    all_events = []
    for name, cal_id in CALENDARS.items():
        events = get_events_for_calendar(cal_id)
        for event in events:
            summary = event.get('summary', 'Sem Título')
            start_data = event.get('start', {})
            
            # Extract time or date
            if 'dateTime' in start_data:
                # 2026-03-17T09:00:00-03:00 -> 09:00
                dt = datetime.fromisoformat(start_data['dateTime'])
                tz = pytz.timezone('America/Sao_Paulo')
                time_str = dt.astimezone(tz).strftime('%H:%M')
            else:
                time_str = "Dia todo"
                
            all_events.append({
                "calendar": name,
                "time": time_str,
                "title": summary
            })
    
    # Sort by time
    def sort_key(e):
        return e['time'] if e['time'] != "Dia todo" else "00:00"
    
    all_events.sort(key=sort_key)
    return all_events

if __name__ == "__main__":
    report = generate_standup()
    print(json.dumps(report, indent=2))
