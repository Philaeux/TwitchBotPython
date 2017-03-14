from abc import ABC


class Processor(ABC):
    """Abstract class with a getters to access modules."""

    def get_grenouille(self):
        """Getter for the master class containing the processor."""
        return self.grenouille_bot

    def get_irc(self):
        """Getter for the irc bot of the processor."""
        return self.grenouille_bot.irc_bot

    def get_calendar(self):
        """Getter for the calendar manager of the processor."""
        return self.grenouille_bot.calendar_manager

    def get_commands(self):
        """Getter for the command processor of the bot."""
        return self.grenouille_bot.command_processor
