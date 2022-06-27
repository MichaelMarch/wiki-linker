from ladders.ladder_finder import LadderFinder
from ordered_set import OrderedSet
from bs4 import BeautifulSoup


class LocalWikiLadderFinder(LadderFinder):
    def __init__(self, start_article: str, end_article: str, extract_limit: int, ladder_limit = 20):
        # def __init__(self, queue: PriorityQueue, dict: DictProxy, start_article: str, end_article: str):
        """
        A class for finding a path ("ladder") between two links on a local Wikipedia instance.
        """

        attribute_filter = {"href": True, "title": True, "class": False, "accesskey": False, "id": False}

        super().__init__("http://127.0.0.1:8080/wikipedia_en_all_maxi_2022-05/A/",
                         attribute_filter, start_article, end_article, extract_limit, ladder_limit)

    def _parse_dom(self, dom: BeautifulSoup):
        urls = OrderedSet()

        for a_tag in dom.find_all('a', recursive=False, limit=self.extract_limit):
            urls.add(a_tag["href"])
        return urls
