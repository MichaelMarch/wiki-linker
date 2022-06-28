from bs4 import BeautifulSoup, SoupStrainer
from queue import PriorityQueue

import requests

from app.ordered_set import OrderedSet


class LadderFinder:
    def __init__(self, base_url: str, attribute_filter: dict[str, bool], extract_limit: int, ladder_limit):
        """
        An abstract interface for finding a path ("ladder") between two links on a given webpage.
        It's recommended that the webpage has a structured and predictable paths like wikis
        """
        self.base_url = base_url
        self.attribute_filter = attribute_filter
        self.extract_limit = extract_limit
        self.ladder_limit = ladder_limit

        self.requests_session = requests.Session()
        self.requests_session.headers.update({
            "Connection": "keep-alive"
        })

    def _extract_links(self, article_name: str) -> OrderedSet:
        """Returns a set of unqiue articles that are referenced in `article_name`"""

        full_url: str = self.base_url + article_name
        response = self.requests_session.get(full_url)

        if not response.status_code == 200:
            return OrderedSet()

        # lxml is around 33% faster than html.parser
        dom = BeautifulSoup(response.text, "lxml", parse_only=SoupStrainer('a', attrs=self.attribute_filter))

        return self._parse_dom(dom)

    # Should be overridden in a subclass
    def _parse_dom(self, dom: BeautifulSoup) -> OrderedSet:
        return None

    # TODO: implement threaded version of this function for articles that have very few links in common.
    #       most of the time when articles aren't closely related it takes way too much time to find a path.
    # TODO: try Breadth-first search algorithm instead of prioritizing
    def find(self, start_article: str, end_article: str) -> list[str]:
        """Find an optimal path between `start_article` and `end_article`"""
        end_page_links: OrderedSet = self._extract_links(end_article)

        # keep track of seen article to avoid infinite loop
        extracted_articles = dict[str, ]()
        extracted_articles[start_article] = None

        # This priority queue implementation uses lowest first ordering meaing that the items with the lowest priority come first.
        # This makes it so enqueued items need to have negative priorities (less then 0)
        queue = PriorityQueue()
        # Starting with priority 0 doesn't matter since it's immediately dequeued
        queue.put((0, [start_article]))

        while not queue.empty():
            ladder: list[str] = queue.get()[1]

            # Limit how long can a ladder get.
            # When the limited length is small it usually finds the path faster.
            if len(ladder) > self.ladder_limit:
                continue

            links = self._extract_links(ladder[-1])

            for link in links:
                if link == end_article:
                    ladder.append(link)
                    return ladder

                if link in extracted_articles:
                    continue

                extracted_articles[link] = None

                duplicated_ladder = ladder[:]
                duplicated_ladder.append(link)

                links_of_link = self._extract_links(link)
                # In other words this is the priority of the new ladder
                # Important: this number must be negative!
                links_in_common = -links_of_link.count_intersections_with(end_page_links)

                queue.put((links_in_common, duplicated_ladder))
        return None
