import os


class SoundProcessor:
    """Listen to the chat rewards claims. When the custom sound reward is claimed, check for the sound in database and
    push it to the display.

    Attributes:
        bot: master bot
        sound_reward_id: reward id linked to sound playing
        sound_dictionary: dict of all key-files associations
    """

    def __init__(self, bot):
        self.bot = bot
        if not self.bot.config['STRATEGY_SOUND'].get("enabled", False):
            return

        self.sound_reward_id = self.bot.config['STRATEGY_SOUND'].get("reward_id", "000")

        # Load sounds
        self.sound_dictionary = {}
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "sounds.txt"), "r") as file:
            lines = file.readlines()
            for line in lines:
                if "=" not in line:
                    continue
                split_line = line.split("=")
                key = split_line[0].strip()
                value = split_line[1].strip()
                self.sound_dictionary[key] = value

        # Add handlers
        reward_id_list = self.bot.strategy.reward_handlers.get(self.sound_reward_id, None)
        if reward_id_list is not None:
            reward_id_list.append(self.on_sound_request)
        else:
            reward_id_list = [self.on_sound_request]
            self.bot.strategy.reward_handlers[self.sound_reward_id] = reward_id_list

    def on_sound_request(self, sender, is_admin, is_sub, reward_id, message):
        lower_message = message.lower()
        lower_message = lower_message.replace("’", "'")
        lower_message = lower_message.replace("à", "a")
        lower_message = lower_message.replace("è", "e")
        lower_message = lower_message.replace("é", "e")
        lower_message = lower_message.replace("ö", "o")
        if lower_message in self.sound_dictionary:
            self.bot.gui.widget.play_sound(self.sound_dictionary[lower_message])
