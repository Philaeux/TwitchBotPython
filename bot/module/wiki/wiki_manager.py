import urllib.parse

import mwclient

class WikiManager:
    """The module of the bot responsible for the calendar reading.

    Attributes:
        site: The Dota 2 Gamepedia wiki object.
    """

    WIKI_URL = ('http', 'dota2.gamepedia.com')

    def __init__(self, grenouille_bot):
        """Initialize the connection to the wiki API.

        Args:
            grenouille_bot: master class.
        """
        self.site = mwclient.Site(self.WIKI_URL, path='/')

    def get_page(self, page_name=None):
        if page_name is None:
            return None

        page = self.site.pages[page_name]

        if not page.exists:
            return None

        return page

    def generate_page_url(self, page):
        return "{0}://{1}/{2}".format(
            self.WIKI_URL[0],
            self.WIKI_URL[1],
            urllib.parse.quote(page.page_title))
