from aiohttp import ClientSession
from app.ladders.ladder_finder import LadderFinder
from app.ordered_set import OrderedSet
from bs4 import BeautifulSoup, SoupStrainer


class LocalWikiLadderFinder(LadderFinder):
    def __init__(self, session: ClientSession, extract_limit: int = None, ladder_limit=20):
        """
        A class for finding a path ("ladder") between two links on a local Wikipedia instance.
        """

        attribute_filter = {"href": True, "title": True, "class": False, "accesskey": False, "id": False}

        super().__init__("http://127.0.0.1:8080/wikipedia_en_all_maxi_2022-05/A/", attribute_filter, session, extract_limit, ladder_limit)

    def _parse_dom(self, dom: BeautifulSoup):
        urls = OrderedSet()

        for a_tag in dom.find_all('a', recursive=False, limit=self.extract_limit):
            urls.add(a_tag["href"])
        return urls

    async def _get_description(self, article: str) -> str:
        full_url: str = self.base_url + article
        async with self.session.get(full_url) as response:
            text = await response.text()

        if not response.ok:
            return OrderedSet()

        # lxml is around 33% faster than html.parser
        dom = BeautifulSoup(text, "lxml", parse_only=SoupStrainer('p'))
        for part in dom.find('p').get_text().split('.'):
            if len(part) > 30:
                return part
        return ""
