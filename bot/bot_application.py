import logging
import os
from datetime import datetime
import threading
from sys import exit
from configparser import ConfigParser

from apiclient import discovery

from bot.grenouille_bot import GrenouilleBot

# Config
config = ConfigParser()
try:
    config.read(os.path.join(os.path.dirname(__file__), '..', 'common', 'settings.ini'))
except Exception:
    print('Impossible to load settings.ini config. Check configuration format')
    exit(1)

# Log
logging.basicConfig(format='[%(asctime)s] %(levelname)s (%(threadName)-8s) %(name)s: %(message)s', level=logging.INFO)

# Calendar refresh
service = discovery.build('calendar', 'v3', developerKey=config['DEFAULT']['calendar_key'], cache_discovery=False)
event_list = []


class Event:
    def __init__(self, start, end, summary):
        self.start = start
        self.end = end
        self.summary = summary

    def __str__(self):
        return '{0} - {1} {2}'.format(self.start.strftime("%H:%M"), self.end.strftime("%H:%M"), self.summary)


def update_events_from_calendar():
    global service
    global event_list

    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='qnv4k3c3upl94sj41pui158k3c@group.calendar.google.com', timeMin=now, maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    del event_list[:]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.strptime(''.join(start.rsplit(':', 1)), "%Y-%m-%dT%H:%M:%S%z")
        end = event['end'].get('dateTime', event['end'].get('date'))
        end = datetime.strptime(''.join(end.rsplit(':', 1)), "%Y-%m-%dT%H:%M:%S%z")
        summary = event['summary']
        event_list.append(Event(start, end, summary))

    threading.Timer(60*60, update_events_from_calendar).start()
update_events_from_calendar()

# Start Irc Bot
grenouille = GrenouilleBot(config, event_list)
grenouille.start()

