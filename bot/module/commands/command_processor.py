import logging

from bot.module.commands.calendar.calendar_processor import CalendarProcessor
from bot.module.commands.info.info_processor import InfoProcessor
from bot.module.commands.crs.crs_processor import CrsProcessor
from bot.module.commands.wiki.wiki_processor import WikiProcessor


class CommandProcessor(InfoProcessor, CalendarProcessor, CrsProcessor, WikiProcessor):
    """Class processing all commands sent into the chat.

    Attributes:
        grenouille_bot: master class with all modules.
        commands: list of all commands managed by the command processor.

    """
    def __init__(self, grenouille_bot):
        """Define all commands the bot will process.

        Args:
            grenouille_bot: master class with all modules.
        """
        InfoProcessor.__init__(self)
        CalendarProcessor.__init__(self)
        CrsProcessor.__init__(self)
        WikiProcessor.__init__(self)

        self.grenouille_bot = grenouille_bot
        self.commands = [{
            'aliases': ['grenouille', 'help', 'aide'],
            'command': self.help
        }, {
            'aliases': ['motd', 'mdj'],
            'command': self.motd
        }, {
            'aliases': ['who', 'qui'],
            'command': self.who
        }, {
            'aliases': ['youtube', 'y'],
            'command': self.youtube
        }, {
            'aliases': ['instagram', 'i'],
            'command': self.instagram
        }, {
            'aliases': ['twitter', 't'],
            'command': self.twitter
        }, {
            'aliases': ['now'],
            'command': self.now
        }, {
            'aliases': ['next'],
            'command': self.next
        }, {
            'aliases': ['update', 'u'],
            'command': self.update
        }, {
            'aliases': ['crs'],
            'command': self.crs
        }, {
            'aliases': ['crs_open', 'crsopen', 'crso'],
            'command': self.crs_open
        }, {
            'aliases': ['crs_vote', 'crsvote', 'crsv'],
            'command': self.crs_vote
        }, {
            'aliases': ['crs_close', 'crsclose', 'crsc'],
            'command': self.crs_close
        }, {
            'aliases': ['wiki'],
            'command': self.wiki
        }]

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
