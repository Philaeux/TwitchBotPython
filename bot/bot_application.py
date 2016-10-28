import logging
import os
import threading
from configparser import ConfigParser
from datetime import datetime
from sys import exit

from apiclient import discovery

from bot.grenouille_irc_bot import GrenouilleIrcBot
from bot.grenouille_calendar import Event

# Logs
logging.basicConfig(format='[%(asctime)s] %(levelname)s (%(threadName)-8s) %(name)s: %(message)s', level=logging.DEBUG)


class GrenouilleBot:
    """The Master class for the GrenouilleBot

    Attributes
        config - Application configuration
        grenouille_irc_bot - IrcGrenouilleBot

        service - Calendar service
        event_list - List of upcoming events, updated every hour
        calendar_timer - Timer to update event list
    """

    def __init__(self):
        # Config
        self.config = ConfigParser()
        try:
            self.config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
        except Exception:
            print('Impossible to load settings.ini config. Check configuration format.')
            exit(1)

        # Calendar
        self.service = discovery.build('calendar', 'v3',
                                       developerKey=self.config['DEFAULT']['calendar_key'],
                                       cache_discovery=False)
        self.event_list = []
        self.calendar_timer = None

        # Irc
        self.grenouille_irc_bot = GrenouilleIrcBot(self)

    def start(self):
        """Start the GrenouilleBot by initializing the IrcClient

        :return:
        """
        self.update_events_from_calendar()
        self.grenouille_irc_bot.start()

    def stop(self):
        """Stop the running GrenouilleBot by stopping all actors

        :return:
        """
        self.calendar_timer.cancel()

    def update_events_from_calendar(self):
        """Read google calendar to update the list of event, every hour.
        """
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId='qnv4k3c3upl94sj41pui158k3c@group.calendar.google.com',
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        del self.event_list[:]
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = datetime.strptime(''.join(start.rsplit(':', 1)), "%Y-%m-%dT%H:%M:%S%z")
            end = event['end'].get('dateTime', event['end'].get('date'))
            end = datetime.strptime(''.join(end.rsplit(':', 1)), "%Y-%m-%dT%H:%M:%S%z")
            summary = event['summary']
            self.event_list.append(Event(start, end, summary))

            self.calendar_timer = threading.Timer(60*60, self.update_events_from_calendar).start()

# Start if main script
if __name__ == '__main__':
    GrenouilleBot().start()
