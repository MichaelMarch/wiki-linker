import sys
import requests

from bs4 import BeautifulSoup, SoupStrainer
from ordered_set import OrderedSet
from queue import PriorityQueue

# Links that contain these characters are not valid wikipedia articles.
# E.g:
#    #Evolutionary_history
#    /wiki/Category:CS1_maint:_multiple_names:_authors_list
#    /w/index.php?title=Coconut_leaf_caterpillar&action=edit&redlink=1
BLACKLISTED_CHARACTERS = ('#', ':', '?')
# Each <a> tag needs to have 'href' and 'title' attributes set,
# but not the 'class' and 'accesskey'
ATTRIBUTES_FILTER = {"href": True, "title": True, "class": False,  "accesskey": False}
requests_session = requests.Session()
requests_session.headers.update({
    "Connection": "keep-alive"
})

BASE_ARTICLE_URL = "http://en.wikipedia.org/wiki/"

# Contains all unique articles extracted by `extract_links` function.
# It used to speed up the search and avoid infinite loops
extracted_articles = list[str]()


def extract_links(article_name: str) -> OrderedSet:
    """Returns a set of unqiue article that are references by `article_name`"""
    full_url: str = BASE_ARTICLE_URL + article_name
    response = requests_session.get(full_url)

    if not response.status_code == 200:
        print(f"Failed to get: {full_url}. Status code: {response.status_code}")
        return

    # lxml is 33% faster than html.parser
    dom = BeautifulSoup(response.text, "lxml", parse_only=SoupStrainer('a', attrs=ATTRIBUTES_FILTER))
    urls = OrderedSet()

    for a_tag in dom.find_all('a', recursive=False):
        sub_path: str = a_tag["href"][6:]
        if all(c not in a_tag["href"] for c in BLACKLISTED_CHARACTERS) and sub_path not in extracted_articles:
            urls.add(sub_path)
    return urls


def find_ladder(start_article, end_article) -> OrderedSet:
    end_page_links: OrderedSet = extract_links(end_article)

    # Mark the starting page as visited in case it's ever
    # referenced teice or more to avoid infinte loop
    extracted_articles.append(start_article)

    queue = PriorityQueue()
    # To make use of priority feature the priority number has to be the first element in the tuple
    queue.put((0, [start_article]))

    while not queue.empty():
        item: tuple[int, list[str]] = queue.get()

        priority: int = item[0]
        ladder: list[str] = item[1]

        # If the ladder exceeds 20 entries (articles) it is discarded
        # TODO: allow users to control the length of ladder in the web interface
        if len(ladder) > 20:
            continue

        links = extract_links(ladder[-1])

        # print(f"Ladder: {ladder}")
        # print(f"# of links of -1: {links_length}")
        # print(f"Ladder priority: {priority}")
        # print("")

        for link in links:
            # The link was found
            if link == end_article:
                ladder.append(end_article)
                return ladder

            extracted_articles.append(link)
            # Duplicate the ladder
            duplicated_ladder = ladder[:]
            duplicated_ladder.append(link)

            # Calculate priority of this ladder
            links_in_common = links.count_intersections_with(end_page_links)
            # TODO: check how cumulative priority performs (-links_in_common + priority), build-up method
            queue.put((-links_in_common, duplicated_ladder))
    return None


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("Too many arguments!")
        print("Usage: python wiki_linker.py article_A article_B")

    if len(sys.argv) < 3:
        print("Too few arguments!")
        print("Usage: python wiki_linker.py article_A article_B")

    article_a = sys.argv[1]
    article_b = sys.argv[2]

    print("The ladder is: ")
    for step in find_ladder(article_a, article_b):
        print(step)
    
    print("")
    print(f"The number of unique articles found is: {len(extract_links)}")
