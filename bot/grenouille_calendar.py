class Event:
    """A calendar event.

    Attributes
        start - starting TimeDate of the event
        end - ending TimeDate of the event
        summary - simple description of the event
    """

    def __init__(self, start, end, summary):
        self.start = start
        self.end = end
        self.summary = summary

    def __str__(self):
        """How the event will be displayed in chat.
        """
        return '{0} - {1} {2}'.format(self.start.strftime("%H:%M"), self.end.strftime("%H:%M"), self.summary)
