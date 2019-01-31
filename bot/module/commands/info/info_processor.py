import os
import json
import random

from bot.module.commands.processor import Processor


class InfoProcessor(Processor):
    """Processor for all information that a viewer may request.

    Attributes:
        motd_data: message of the day.
        who_data: information about the current streamer.
        twitter_accounts: list of twitter accounts loaded from file
    """

    def __init__(self):
        self.motd_data = 'Aucun message.'
        self.who_data = 'Aucune info sur le streamer actuel.'

        with open(os.path.join(os.path.dirname(__file__),
                               'twitters.json')) as json_data:
            self.twitter_accounts = json.load(json_data)

        self.commands.extend([{
                'aliases': ['help', 'aide', 'h'],
                'command': self.help
            }, {
                'aliases': ['who', 'qui'],
                'command': self.who
            }])
        if self.bot.config['TWITTER'].getboolean('enabled', False):
            self.commands.append({
                'aliases': ['twitter', 't'],
                'command': self.twitter
            })
        if self.bot.config['MOTD'].getboolean('enabled', False):
            self.commands.append({
                'aliases': ['motd', 'mdj'],
                'command': self.motd
            })
        if self.bot.config['YOUTUBE'].getboolean('enabled', False):
            self.commands.append({
                'aliases': ['youtube', 'y'],
                'command': self.youtube
            })

    def help(self, param_line, sender, is_admin):
        """Returns all the commands the bot is listening to."""
        command_names = []

        for command in self.get_commands().commands:
            command_names.append(command['aliases'][0])

        line = "Les commandes sont: {0}.".format(', '.join(sorted(command_names)))

        self.get_irc().send_msg(line)

    def motd(self, param_line, sender, is_admin):
        """Display an informative message for the viewers.

        Only admins are able to change the message.
        """
        if is_admin and param_line is not None:
            self.motd_data = 'Message du jour: {0}'.format(param_line)
        self.get_irc().send_msg(self.motd_data)

    def who(self, param_line, sender, is_admin):
        """Display current streamers.

        Only admins are able to change the message.
        """
        if is_admin and param_line is not None:
            self.who_data = 'Streamers actuels: {0}'.format(param_line)
        self.get_irc().send_msg(self.who_data)

    def youtube(self, param_line, sender, is_admin):
        """Print the youtube official channel of the FroggedTV"""
        self.get_irc().send_msg('Le YouTube de la chaîne est: ' +
                                self.get_bot().config['YOUTUBE']['youtube_url'])

    def twitter(self, param_line, sender, is_admin):
        """Display the Twitter acco unt of the asked streamer."""
        if param_line is not None:
            twitter = self.find_twitter(param_line.lower())
        else:
            twitter = self.find_twitter('froggedtv')

        if twitter is not None:
            line = '{0}: {1}'.format(twitter['pretty_name'], twitter['link'])
            self.get_irc().send_msg(line)

    def find_twitter(self, name):
        """Find the twitter account linked to a streamer name.

        Args:
            name: name of the twitter account requested.
        Returns:
            The twitter account information with name as one of it aliases,
            or None if no account is found.
        """
        for twitter_account in self.twitter_accounts:
            if name in twitter_account['aliases']:
                return twitter_account

        return None
