import logging

from bot.module.commands.calendar.calendar_processor import CalendarProcessor
from bot.module.commands.info.info_processor import InfoProcessor
from bot.module.commands.vote.vote_processor import VoteProcessor
from bot.module.commands.wiki.wiki_processor import WikiProcessor
from bot.module.commands.bet.bet_processor import BetProcessor
from bot.module.commands.ads.ads_processor import AdsProcessor


class CommandProcessor(InfoProcessor, CalendarProcessor, VoteProcessor, WikiProcessor, BetProcessor, AdsProcessor):
    """Class processing all commands sent into the chat.

    Attributes:
        bot: master class with all modules.
        commands: list of all commands managed by the command processor.

    """
    def __init__(self, bot):
        """Define all commands the bot will process.

        Args:
            bot: master class with all modules.
        """

        self.bot = bot
        self.commands = []

        InfoProcessor.__init__(self)
        CalendarProcessor.__init__(self)
        BetProcessor.__init__(self)
        AdsProcessor.__init__(self)

    def process(self, command_line, sender, is_admin):
        """Process a command.

        Args:
            command_line: Full command line without the ! stating a command.
            sender: String sender of the command.
            is_admin: Boolean representing user rights.
        """
        command_split = command_line.split(' ', maxsplit=1)

        command = self.find_command(command_split[0])
        if command is None:
            return

        if len(command_split) == 1 or command_split[1] == '':
            param_line = None
        else:
            param_line = command_split[1]

        # Call the command
        command(param_line=param_line, sender=sender, is_admin=is_admin)

    def find_command(self, name):
        """Find if asked command exists and returns it.

        Args:
            name: Name of the command object to find.
        Returns:
            The command method responsible to process the command, or None if
            no object is able to process it.
        """
        for command in self.commands:
            if name in command['aliases']:
                return command['command']

        return None
