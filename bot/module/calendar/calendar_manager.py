import threading, logging
from datetime import datetime, timezone
from apiclient import discovery


class Event:
    """A calendar event.

    Attributes:
        start: starting datetime of the event.
        end: ending datetime of the event.
        summary: simple description of the event.
    """

    def __init__(self, start, end, summary):
        """Init an Event with all attributes."""
        self.start = start
        self.end = end
        self.summary = summary

    def __str__(self):
        """How the event will be displayed in chat.

        Returns:
            A string representing the calendar event.
        """
        now = datetime.now(timezone.utc)
        days = self.start - now
        result = ''
        if days.days > 0:
            result = 'J+{0} '.format(days.days)
        return '{0}{1} - {2} {3}'.format(result, self.start.strftime("%H:%M"),
                                         self.end.strftime("%H:%M"),
                                         self.summary)


class CalendarManager:
    """The module of the bot responsible for the calendar reading.

    Attributes:
        enabled: Is the calendar module enabled.
        g_cal_key: Key to the Google calendar API.
        g_cal_id: Id of the Google calendar to read.
        g_cal_freq: int minutes between updates.

        calendar_timer: Timer periodically calling a update of the event_list.
        event_list: List of upcoming events, updated from Google Calendar.
    """

    def __init__(self, grenouille_bot):
        """Create the calendar modules from config parameters.

        Args:
            grenouille_bot: master class.
        """
        config = grenouille_bot.config['CALENDAR']

        self.enabled = config.getboolean('enabled', False)
        if not self.enabled:
            return

        self.g_cal_key = config['google_api_key']
        self.g_cal_id = config['google_calendar_id']
        self.g_cal_freq = int(config['refresh_frequency'])
        self.calendar_timer = None

        self.event_list = []

    def start(self):
        """Start the GrenouilleCalendar module periodic update process."""
        if not self.enabled:
            return

        self.calendar_timer = threading.Timer(10, self.update_events_from_calendar)
        self.calendar_timer.start()

    def stop(self):
        """Stop the GrenouilleCalendar module by canceling any process."""
        if not self.enabled:
            return

        self.calendar_timer.cancel()

    def update_events_from_calendar(self, start_timer=True):
        """Read google calendar to update the list of events.

        Args:
            start_timer: Boolean to indicate if a timer must be start to
            refresh at the end of the execution.
        """
        new_calendar = []

        try:
            service = discovery.build('calendar', 'v3',
                                      developerKey=self.g_cal_key,
                                      cache_discovery=False)
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId=self.g_cal_id,
                                                  timeMin=now, maxResults=5,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            for event in events:
                try:
                    summary = event['summary']
                    start = event['start'].get('dateTime',
                                               event['start'].get('date'))
                    start = datetime.strptime(''.join(start.rsplit(':', 1)),
                                              "%Y-%m-%dT%H:%M:%S%z")
                    end = event['end'].get('dateTime',
                                           event['end'].get('date'))
                    end = datetime.strptime(''.join(end.rsplit(':', 1)),
                                            "%Y-%m-%dT%H:%M:%S%z")
                    new_calendar.append(Event(start, end, summary))
                except Exception:
                    logging.exception('Error getting one event, skipping')

                self.event_list = new_calendar
        except Exception:
            logging.exception('Error while requesting calendar data, the calendar is not updated.')

        if start_timer:
            self.calendar_timer = threading.Timer(60 * self.g_cal_freq,
                                                  self.update_events_from_calendar)
            self.calendar_timer.start()

    def get_next_event(self):
        """Access to the next Event in the calendar.

        Returns:
            The Event object corresponding to the next event in the calendar
            or None if there is no event.
        """
        now = datetime.now(timezone.utc)
        while self.event_list and self.event_list[0].end < now:
            self.event_list.pop(0)

        if len(self.event_list) == 0:
            return None
        elif self.event_list[0].start > now:
            return self.event_list[0]
        elif len(self.event_list) == 1:
            return None
        else:
            return self.event_list[1]

    def get_now_event(self):
        """Access to the current Event in the calendar.

        Returns:
            The Event object corresponding to the current event in the calendar
            or None if there is no event.
        """
        now = datetime.now(timezone.utc)
        while self.event_list and self.event_list[0].end < now:
            self.event_list.pop(0)

        if len(self.event_list) == 0:
            return None
        elif self.event_list[0].start < now < self.event_list[0].end:
            return self.event_list[0]
        else:
            return None
