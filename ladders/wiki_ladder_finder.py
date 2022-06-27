from ladders.ladder_finder import LadderFinder
from ordered_set import OrderedSet
from bs4 import BeautifulSoup


class WikiLadderFinder(LadderFinder):
    def __init__(self, start_article: str, end_article: str, extract_limit: int, ladder_limit = 20):
        """
        A class for finding a path ("ladder") between two links on Wikipedia online.

        Note: Please be mindful and don't use this class to scrape the real Wikipedia or any publically hosted Wiki project.
        I have implemented a way to scrape a local instance of Wikipedia that is much faster (see LocalWikiLadderfinder class). 
        To set up your own instance see the README.md file.
        """

        attribute_filter = {"href": True, "title": True, "class": False, "accesskey": False}
        # Links that contain these characters are not valid wikipedia articles.
        # E.g.:
        #    "#Evolutionary_history" <- This is just a bookmark to a section on the same article
        #    "/wiki/Category:CS1_maint:_multiple_names:_authors_list" <- The colon is used to point to non-article sites that are still part of wikipedia
        #    "/w/index.php?title=Coconut_leaf_caterpillar&action=edit&redlink=1" <- Some kind of ambiguous link that doesn't make sense to parse
        self.characters_blacklist = ('#', ':', '?')

        super().__init__("http://en.wikipedia.org/wiki/", attribute_filter, start_article, end_article, extract_limit, ladder_limit)

    def _parse_dom(self, dom: BeautifulSoup):
        urls = OrderedSet()

        for a_tag in dom.find_all('a', recursive=False, limit=self.extract_limit):
            # All valid wikipedia articles start with "/wiki/" and so they can be trimmed out to save some memory
            sub_path: str = a_tag["href"][6:]
            if all(c not in a_tag["href"] for c in self.characters_blacklist):
                urls.add(sub_path)
        return urls
