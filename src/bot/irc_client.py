import itertools
import more_itertools
import logging
import sys
from datetime import datetime

from irc.bot import SingleServerIRCBot, ServerSpec, ReconnectStrategy


class IrcClient(SingleServerIRCBot):
    """Module responsible for the Twitch (IRC) chat.

    Listen to all pub messages and forward to the command processor if a command is detected.
    Provide methods to send message to the current channel or a private message to a user.

    Attributes:
        bot: Bot owning this client
        stop_signal: Flag for process termination.
    """

    SEVER_URI = 'irc.chat.twitch.tv'
    SERVER_PORT = 6667

    def __init__(self, bot):
        self.bot = bot

        nickname = self.bot.settings.irc_nickname
        password = self.bot.settings.irc_token
        SingleServerIRCBot.__init__(self, [(IrcClient.SEVER_URI, IrcClient.SERVER_PORT, password)], nickname, nickname,
                                    recon=NoopReconnect())

        self.last_ping = datetime.utcnow()
        self.last_claimed_reward = None
        self.stop_signal = False

    def update_credentials(self):
        server_list = [(IrcClient.SEVER_URI, IrcClient.SERVER_PORT, self.bot.settings.irc_token)]
        specs = map(ServerSpec.ensure, server_list)
        self.servers = more_itertools.peekable(itertools.cycle(specs))

    def stop(self) -> None:
        """Set the stop flag and disconnect all open sockets."""
        self.stop_signal = True
        self.disconnect()

    def on_disconnect(self, connection, e) -> None:
        """When the IRC bot is disconnected, end the thread only if the stop flag is set."""
        self.bot.qt.window.connection_changed.emit("Off")
        if self.stop_signal:
            sys.exit(0)

    def on_welcome(self, connection, e):
        """Called when the bot is connected to the IRC server. Setup config."""
        connection.join(f"#{self.bot.settings.irc_channel}")
        connection.set_rate_limit(0.5)
        connection.send_raw('CAP REQ :twitch.tv/commands')
        connection.send_raw('CAP REQ :twitch.tv/membership')
        connection.send_raw('CAP REQ :twitch.tv/tags')
        connection.add_global_handler("join", self.on_join)
        connection.add_global_handler("part", self.on_part)
        self.bot.qt.window.connection_changed.emit("On")

    def on_join(self, connection, e):
        self.bot.qt.window.chatter_join.emit(e.source.split("!")[0])

    def on_part(self, connection, e):
        self.bot.qt.window.chatter_left.emit(e.source.split("!")[0])

    def on_ping(self, connection, e):
        """Save last ping for sanitizer check."""
        self.last_ping = datetime.utcnow()
        self.bot.qt.window.heartbeat_received.emit()

    def on_pubmsg(self, connection, e):
        """Called for every public message. Detect if a command is called."""
        message = e.arguments[0]
        sender = e.source.nick
        tags = {key_value["key"]: key_value["value"] for key_value in e.tags}
        is_admin = False
        is_sub = False
        reward_id = None
        command = None

        if ("badges" in tags and tags["badges"] is not None and
                ("moderator" in tags["badges"] or "broadcaster" in tags["badges"])):
            is_admin = True
        if "badges" in tags and tags["badges"] and ("subscriber" in tags["badges"]):
            is_sub = True
        if "custom-reward-id" in tags and tags["custom-reward-id"] is not None:
            reward_id = tags["custom-reward-id"]
        if len(message) > 2 and message[0] == '!' and message[1] != ' ':
            command = message[1:].split(' ', maxsplit=1)[0]

        strategy = self.bot.strategy

        if reward_id is not None:
            self.last_claimed_reward = reward_id
            strategy.on_reward(sender, is_admin, is_sub, reward_id, message)
        elif command is not None:
            strategy.on_command(sender, is_admin, is_sub, command, message[min(len(command)+2, len(message)):])
        else:
            strategy.on_message(sender, is_admin, is_sub, message)
        self.bot.qt.window.chatter_join.emit(sender)

    def send_msg(self, line):
        """Send a message to the IRC channel.

        Do nothing if there is an exception (like disconnected)

        Args:
            line: The line to print.
        """
        try:
            self.connection.privmsg(self.bot.settings.irc_channel, line)
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


class NoopReconnect(ReconnectStrategy):

    def __init__(self, **attrs):
        pass

    def run(self, bot):
        pass
