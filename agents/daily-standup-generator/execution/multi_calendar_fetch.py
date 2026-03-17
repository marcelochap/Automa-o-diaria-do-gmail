import subprocess
import json
import os
import sys
from datetime import datetime, time

GWS_CMD = 'gws.cmd' if sys.platform == 'win32' else 'gws'

CALENDARS = [
    "marcelo.leite.engcivil@gmail.com",
    "yukawa.harumi@gmail.com",
    "diretoria@premoldadobrasil.com.br",
    "0i23vfndiou4g3rogceqaqlf1o@group.calendar.google.com"
]

def get_events_for_calendar(calendar_id):
    # Today's boundaries
    now = datetime.now()
    start_of_day = datetime.combine(now.date(), time.min).isoformat() + "Z"
    end_of_day = datetime.combine(now.date(), time.max).isoformat() + "Z"
    
    args = [
        GWS_CMD, 'calendar', 'events', 'list',
        '--params', json.dumps({
            "calendarId": calendar_id,
            "timeMin": start_of_day,
            "timeMax": end_of_day,
            "singleEvents": True,
            "orderBy": "startTime"
        }),
        '--format', 'json'
    ]
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True, encoding='utf-8')
        data = json.loads(result.stdout)
        return data.get('items', [])
    except Exception as e:
        print(f"Error fetching calendar {calendar_id}: {e}")
        return []

def main():
    all_events = []
    for cal_id in CALENDARS:
        print(f"Fetching events for {cal_id}...")
        events = get_events_for_calendar(cal_id)
        for event in events:
            summary = event.get('summary', 'Sem Título')
            start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
            all_events.append({
                "calendar": cal_id,
                "title": summary,
                "time": start
            })
    
    print(json.dumps(all_events, indent=2))

if __name__ == "__main__":
    main()
