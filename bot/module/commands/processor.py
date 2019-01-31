from abc import ABC


class Processor(ABC):
    """Abstract class with a getters to access modules."""

    def get_bot(self):
        """Getter for the master class containing the processor."""
        return self.bot

    def get_irc(self):
        """Getter for the irc bot of the processor."""
        return self.bot.irc_bot

    def get_calendar(self):
        """Getter for the calendar manager of the processor."""
        return self.bot.calendar_manager

    def get_wiki(self):
        """Getter for the wiki manager of the processor."""
        return self.bot.wiki_manager

    def get_commands(self):
        """Getter for the command processor of the bot."""
        return self.bot.command_processor
