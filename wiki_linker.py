import sys
import requests

from bs4 import BeautifulSoup, SoupStrainer
from ordered_set import OrderedSet
from queue import PriorityQueue

# Some links on a Wikipedia page aren't links to other articles and so they need to be excluded
BLACKLISTED_CHARACTERS = ('#', ':', '?')
# Another layer of ensuring that the extracted links are article links
ATTRIBUTES_FILTER = {"href": True, "title": True, "class": False, "accesskey": False}


requests_session = requests.Session()
requests_session.headers.update({
    "Connection": "keep-alive"
})

BASE_ARTICLE_URL = "http://en.wikipedia.org/wiki/"

extracted_articles = dict[str, ]()


def extract_links(article_name: str) -> OrderedSet:
    """Extracts a set of unqiue article that are references by `article_name`"""
    full_url: str = BASE_ARTICLE_URL + article_name
    response = requests_session.get(full_url)

    if not response.status_code == 200:
        print(f"Failed to get: '{full_url}'. Status code: {response.status_code}")
        return OrderedSet()

    # lxml is 33% faster than html.parser
    dom = BeautifulSoup(response.text, "lxml", parse_only=SoupStrainer('a', attrs=ATTRIBUTES_FILTER))
    urls = OrderedSet()

    for a_tag in dom.find_all('a', recursive=False):
        sub_path: str = a_tag["href"][6:]
        if all(c not in a_tag["href"] for c in BLACKLISTED_CHARACTERS):
            urls.add(sub_path)
    return urls


def find_ladder(start_article: str, end_article: str) -> list[str]:
    """Find an optimal path between `start_article` and `end_article`"""
    end_page_links: OrderedSet = extract_links(end_article)
    extracted_articles[start_article] = None

    queue = PriorityQueue()
    # Here the priority isn't important since it's the only item in the queue
    queue.put((0, [start_article]))

    while not queue.empty():
        ladder: list[str] = queue.get()[1]

        # TODO: make the length of a ladder be controlled by the UI
        if len(ladder) > 20:
            continue

        links = extract_links(ladder[-1])

        for link in links:
            if link == end_article:
                ladder.append(end_article)
                return ladder

            if link in extracted_articles:
                continue

            extracted_articles[link] = None

            duplicated_ladder = ladder[:]
            duplicated_ladder.append(link)

            links_of_link = extract_links(link)
            links_in_common = links_of_link.count_intersections_with(end_page_links)

            queue.put((-links_in_common, duplicated_ladder))
    return None


if __name__ == "__main__":
    if sys.version_info < (3, 7):
        print("This program requires to be run on python version 3.7+.")
        exit(-1)

    if len(sys.argv) > 3:
        print("Too many arguments!")
        print(f"Usage: python {sys.argv[0]} article_A article_B")
        exit(-2)

    if len(sys.argv) < 3:
        print("Too few arguments!")
        print(f"Usage: python {sys.argv[0]} article_A article_B")
        exit(-3)

    article_a = sys.argv[1]
    article_b = sys.argv[2]

    print("The ladder is: ")
    for step in find_ladder(article_a, article_b):
        print(step)

    print("")
    print(f"The number of unique articles found is: {len(extract_links)}")
