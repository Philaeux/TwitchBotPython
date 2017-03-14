from bot.module.commands.processor import Processor


class CalendarProcessor(Processor):
    """Processor for all calendar commands."""

    def __init__(self):
        pass

    def next(self, param_line, sender, is_admin):
        """Display the next event from the calendar."""
        event = self.get_calendar().get_next_event()

        line = 'Aucun événement planifié dans le calendrier.'
        if event is not None:
            line = str(event)

        self.get_irc().send_msg(line)

    def now(self, param_line, sender, is_admin):
        """Display the current event from the calendar."""
        event = self.get_calendar().get_now_event()

        line = "Aucune information dans le calendrier pour l'événement actuel."
        if event is not None:
            line = str(event)

        self.get_irc().send_msg(line)

    def update(self, param_line, sender, is_admin):
        """Force a update from the calendar"""
        if not is_admin:
            return

        self.get_calendar().update_events_from_calendar(start_timer=False)
        self.get_irc().send_msg("Calendrier mis à jour avec succès.")
