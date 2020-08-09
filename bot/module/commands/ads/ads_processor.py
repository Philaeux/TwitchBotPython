from bot.module.commands.processor import Processor


class AdsProcessor(Processor):
    """Processor for all ADS commands."""

    def __init__(self):
        if self.bot.config["ADS"].getboolean("enabled", False):
            self.commands.extend([{
                'aliases': ["ads"],
                'command': self.ads
            }])
            self.ads_default_duration = self.bot.config["ADS"].getint("default_duration", 300)

    def ads(self, param_line, sender, is_admin):
        """Send an ad to be played on twitch"""
        if not is_admin:
            return

        if param_line is not None and param_line.isdigit():
            duration = int(param_line)
        else:
            duration = self.ads_default_duration

        self.get_irc().send_msg("/commercial {0}".format(duration))
        self.get_irc().send_msg("{0} seconds ad sent Kreygasm".format(duration))
