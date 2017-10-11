import logging, traceback
from time import sleep
from datetime import datetime, timedelta
import threading

from irc.bot import SingleServerIRCBot


class IrcBot(SingleServerIRCBot):
    """The module of the bot responsible for the Twitch (IRC) chat.

    Listen to all pub messages and forward to the command processor if a
    command is detected. Provide methods to send message to the current
    channel or a private message to a user.

    Attributes:
        grenouille_bot: master class.
        sanitizer: thread checking every 3 minutes to check if the bot is
            still alive.
        last_ping: last time of the ping-pong.
    """

    def __init__(self, grenouille_bot):
        self.grenouille_bot = grenouille_bot
        config = grenouille_bot.config['DEFAULT']

        nickname = config['nickname']
        server = 'irc.chat.twitch.tv'
        password = config['token']
        port = 6667
        SingleServerIRCBot.__init__(self, [(server, port, password)],
                                    nickname, nickname)

        self.channel = config['channel']
        self.sanitizer = threading.Timer(60, self.sanitize).start()
        self.last_ping = datetime.utcnow()

    def stop(self):
        pass
        # TODO - Safely shutdown the thread

    def on_welcome(self, connection, e):
        """Called when the bot is connected to the IRC server. Setup config."""
        connection.join(self.channel)
        connection.set_rate_limit(0.5)
        connection.send_raw('CAP REQ :twitch.tv/commands')
        connection.send_raw('CAP REQ :twitch.tv/tags')
        logging.info('Connected to channel.')

    def sanitize(self):
        """Reconnect if the Twitch IRC server kicked the bot."""
        if datetime.utcnow() - self.last_ping > timedelta(minutes=7):
            self.last_ping = datetime.utcnow()
            logging.warning('Sanitizer detected lost connection. Reconnecting.')
            self.connection.disconnect()
            sleep(10)
            self.connection.reconnect()
        self.sanitizer = threading.Timer(60, self.sanitize).start()

    def on_ping(self, connection, e):
        """Save last ping for sanitizer check."""
        self.last_ping = datetime.utcnow()

    def on_pubmsg(self, connection, e):
        """Called for every public message. Detect if a command is called."""
        message = e.arguments[0]
        sender = e.source.nick
        tags = {key_value["key"]: key_value["value"] for key_value in e.tags}
        is_admin = False
        if 'user-type' in tags:
            is_admin = bool(tags['user-type'])

        # Check we have a message starting with ! from a user
        if (len(message) <= 1
            or message[0] != '!'
            or message[1] == ' ' ):
            return

        processor = self.grenouille_bot.command_processor
        try:
            processor.process(command_line=message[1:],
                              sender=sender,
                              is_admin=is_admin)
        except Exception as e:
            logging.exception('Impossible to execute command.')

    def send_msg(self, line):
        """Send a message to the IRC channel.

        Do nothing if there is an exception (like disconnected)

        Args:
            line: The line to print.
        """
        try :
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
