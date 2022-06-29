from aiohttp import ClientSession

from bs4 import BeautifulSoup, SoupStrainer
from queue import PriorityQueue


from app.ordered_set import OrderedSet


class LadderFinder:
    def __init__(self, base_url: str, attribute_filter: dict[str, bool], session: ClientSession, extract_limit: int, ladder_limit):
        """
        An abstract interface for finding a path ("ladder") between two links on a given webpage.
        It's recommended that the webpage has a structured and predictable paths like wikis
        """
        self.base_url = base_url
        self.attribute_filter = attribute_filter
        self.extract_limit = extract_limit
        self.ladder_limit = ladder_limit
        self.session = session

    async def _extract_links(self, article_name: str) -> OrderedSet:
        """Returns a set of unqiue articles that are referenced in `article_name`"""

        full_url: str = self.base_url + article_name
        async with self.session.get(full_url) as response:
            text = await response.text()

        if not response.ok:
            return OrderedSet()

        # lxml is around 33% faster than html.parser
        dom = BeautifulSoup(text, "lxml", parse_only=SoupStrainer('a', attrs=self.attribute_filter))

        return self._parse_dom(dom)

    # Should be overridden in a subclass
    def _parse_dom(self, dom: BeautifulSoup) -> OrderedSet:
        return None

    # TODO: implement threaded version of this function for articles that have very few links in common.
    #       most of the time when articles aren't closely related it takes way too much time to find a path.
    # TODO: try Breadth-first search algorithm instead of prioritizing
    async def find(self, starting_article: str, ending_article: str) -> list[str]:
        """Find an optimal path between `start_article` and `end_article`"""

        self.extracted_articles = dict[str, ]()
        starting_article_links: OrderedSet = await self._extract_links(starting_article)
        endending_article_links: OrderedSet = await self._extract_links(ending_article)

        if len(starting_article_links) == 0:
            return ["It's impossible to find the ladder because the starting article doesn't have any valid links or it just doesn't exist."]
        if len(endending_article_links) == 0:
            return ["It's impossible to find the ladder because the ending article doesn't have any valid links or it just doesn't exist."]

        self.extracted_articles[starting_article] = None

        # This priority queue implementation uses lowest first ordering meaing that the items with the lowest priority come first.
        # This makes it so enqueued items need to have negative priorities (less then 0)
        queue = PriorityQueue()
        ladder = await self._process_links(queue, starting_article_links,
                                           [starting_article], ending_article, endending_article_links)
        if ladder:
            return ladder

        while not queue.empty():
            ladder: list[str] = queue.get()[1]

            # Limit how long can a ladder get.
            # When the limited length is small it usually finds the path faster.
            if len(ladder) > self.ladder_limit:
                continue

            processed_ladder = await self._process_ladder(queue, ladder, ending_article, endending_article_links)
            if processed_ladder:
                return processed_ladder

        return ["Unhandled exception"]

    async def _process_ladder(self, queue: PriorityQueue, ladder: list[str], ending_article: str, endending_article_links: str) -> list[str]:
        links = await self._extract_links(ladder[-1])
        return await self._process_links(queue, links, ladder, ending_article, endending_article_links)

    async def _process_links(self, queue: PriorityQueue, links: OrderedSet, ladder: list[str], ending_article: str, endending_article_links: str) -> list[str]:
        for link in links:
            if link == ending_article:
                ladder.append(link)
                return ladder

            if link in self.extracted_articles:
                continue

            self.extracted_articles[link] = None

            duplicated_ladder = ladder[:]
            duplicated_ladder.append(link)

            links_of_link = await self._extract_links(link)
            # In other words this is the priority of the new ladder
            # Important: this number must be negative!
            links_in_common = -links_of_link.count_intersections_with(endending_article_links)
            queue.put((links_in_common, duplicated_ladder))
        return []
