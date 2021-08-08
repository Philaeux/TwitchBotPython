import logging
from datetime import datetime

from irc.bot import SingleServerIRCBot


class IrcClient(SingleServerIRCBot):
    """The module of the bot responsible for the Twitch (IRC) chat.

    Listen to all pub messages and forward to the command processor if a
    command is detected. Provide methods to send message to the current
    channel or a private message to a user.
    """

    def __init__(self, bot):
        self.bot = bot
        config = self.bot.config['IRC']

        self.enabled = config.getboolean('enabled', False)
        if not self.enabled:
            return

        nickname = config['nickname']
        server = 'irc.chat.twitch.tv'
        password = config['token']
        port = 6667
        SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)

        self.channel = config['channel']
        self.last_ping = datetime.utcnow()

    def stop(self):
        self.die()

    def on_welcome(self, connection, e):
        """Called when the bot is connected to the IRC server. Setup config."""
        connection.join(self.channel)
        connection.set_rate_limit(0.5)
        connection.send_raw('CAP REQ :twitch.tv/commands')
        connection.send_raw('CAP REQ :twitch.tv/tags')
        logging.info('Connected to channel.')

    def on_ping(self, connection, e):
        """Save last ping for sanitizer check."""
        self.last_ping = datetime.utcnow()

    def on_pubmsg(self, connection, e):
        """Called for every public message. Detect if a command is called."""
        message = e.arguments[0]
        sender = e.source.nick
        tags = {key_value["key"]: key_value["value"] for key_value in e.tags}
        is_admin = False
        is_sub = False
        reward_id = None
        command = None

        if "badges" in tags and tags["badges"] is not None and ("moderator" in tags["badges"] or "broadcaster" in tags["badges"]):
            is_admin = True
        if "badges" in tags and tags["badges"] and ("subscriber" in tags["badges"]):
            is_sub = True
        if "custom-reward-id" in tags and tags["custom-reward-id"] is not None:
            reward_id = tags["custom-reward-id"]
        if len(message) > 2 and message[0] == '!' and message[1] != ' ' :
            command = message[1:].split(' ', maxsplit=1)[0]

        strategy = self.bot.strategy
        if reward_id is not None:
            strategy.on_reward(sender, is_admin, is_sub, reward_id, message)
        elif command is not None:
            strategy.on_command(sender, is_admin, is_sub, command, message[min(len(command)+2, len(message)):])
        else:
            strategy.on_message(sender, is_admin, is_sub, message)

    def send_msg(self, line):
        """Send a message to the IRC channel.

        Do nothing if there is an exception (like disconnected)

        Args:
            line: The line to print.
        """
        try:
            self.connection.privmsg(self.channel, line)
        except Exception:
            # TODO: Queue the message to resend later.
            logging.exception('Impossible to send the message.')

    def send_private_msg(self, user, line):
        """Send a private message to a IRC user in the channel.

        Args:
            user: user to send the message to.
            line: message to send.
        """
        self.send_msg('/w {} {}'.format(user, line))
