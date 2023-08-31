import os
import sys
import time


class SoundProcessor:
    """Listen to the chat rewards claims. When the custom sound reward is claimed, check for the sound in database and
    push it to the display.

    Attributes:
        bot: master bot
        sound_dictionary: dict of all key-files associations
    """

    def __init__(self, bot, strategy):
        self.bot = bot

        # Load sounds
        self.MAX_RELOAD_FREQUENCY = 60
        self.sound_dictionary = {}
        self.last_sound_load = time.time() - 2*self.MAX_RELOAD_FREQUENCY
        if getattr(sys, 'frozen', False):
            self.sound_path = os.path.join(os.path.dirname(sys.executable), "sounds")
        elif __file__:
            self.sound_path = os.path.join(os.path.dirname(__file__), "..", "data", "sounds")
        self.reload_sound_map()

        # Add handler
        strategy.reward_handlers.append(self.on_reward)
        
    def reload_sound_map(self):
        if time.time() > self.last_sound_load + self.MAX_RELOAD_FREQUENCY:
            self.last_sound_load = time.time()
            self.sound_dictionary = {}
            for dir_path, _, filenames in os.walk(self.sound_path):
                for sound_file in [f for f in filenames if f.endswith(".opus")]:
                    self.sound_dictionary[sound_file[:-5]] = os.path.join(dir_path, sound_file)

    def on_reward(self, sender, is_admin, is_sub, reward_id, message):
        if reward_id != self.bot.settings.sound_reward_id:
            return

        lower_message = message.lower()
        lower_message = lower_message.replace("’", "'")
        lower_message = lower_message.replace(" ", "_")
        lower_message = lower_message.replace("à", "a")
        lower_message = lower_message.replace("è", "e")
        lower_message = lower_message.replace("é", "e")
        lower_message = lower_message.replace("ö", "o")
        if lower_message in self.sound_dictionary:
            self.bot.qt.window.queue_sound(self.sound_dictionary[lower_message])
        else:
            self.reload_sound_map()
            if lower_message in self.sound_dictionary:
                self.bot.qt.window.queue_sound(self.sound_dictionary[lower_message])
