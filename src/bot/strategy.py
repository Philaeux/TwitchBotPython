from bot.processors.sound_processor import SoundProcessor


class Strategy:
    """Class processing all events."""

    def __init__(self, bot):
        self.bot = bot

        self.message_handlers = []
        self.command_handlers = {}
        self.reward_handlers = []

        self.sound_processor = SoundProcessor(self.bot, self)

    def on_message(self, sender, is_admin, is_sub, message):
        print("message s:{} a:{} s:{} m:{}".format(sender, is_admin, is_sub, message))
        for handler in self.message_handlers:
            handler(sender, is_admin, is_sub, message)

    def on_command(self, sender, is_admin, is_sub, command, arguments):
        print("command s:{} a:{} s:{} c:{} a:{}".format(sender, is_admin, is_sub, command, arguments))
        handler = self.command_handlers.get(command, None)
        if handler is None:
            return
        else:
            handler(sender, is_admin, is_sub, command, arguments)

    def on_reward(self, sender, is_admin, is_sub, reward_id, message):
        print("reward s:{} a:{} s:{} r:{} m:{}".format(sender, is_admin, is_sub, reward_id, message))
        for handler in self.reward_handlers:
            handler(sender, is_admin, is_sub, reward_id, message)
