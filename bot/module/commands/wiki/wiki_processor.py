from bot.module.commands.processor import Processor

class WikiProcessor(Processor):
    """Processor for the Dota 2 Gamepedia wiki.
    """

    def wiki(self, param_line, sender, is_admin):
        if param_line is None:
            return

        page = self.get_wiki().get_page(param_line)

        if page is None:
            return

        url = self.get_wiki().generate_page_url(page)

        line = "{0}: {1}".format(
            page.page_title,
            url)

        self.get_irc().send_msg(line)
