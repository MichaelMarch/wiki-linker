from ladders.ladder_finder import LadderFinder
from app.ordered_set import OrderedSet
from bs4 import BeautifulSoup


class LocalWikiLadderFinder(LadderFinder):
    def __init__(self, extract_limit: int, ladder_limit=20):
        """
        A class for finding a path ("ladder") between two links on a local Wikipedia instance.
        """

        attribute_filter = {"href": True, "title": True, "class": False, "accesskey": False, "id": False}

        super().__init__("http://127.0.0.1:8080/wikipedia_en_all_maxi_2022-05/A/", attribute_filter, extract_limit, ladder_limit)

    def _parse_dom(self, dom: BeautifulSoup):
        urls = OrderedSet()

        for a_tag in dom.find_all('a', recursive=False, limit=self.extract_limit):
            urls.add(a_tag["href"])
        return urls
