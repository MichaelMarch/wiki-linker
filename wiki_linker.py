
import sys
import requests

from bs4 import BeautifulSoup, SoupStrainer
from ordered_set import OrderedSet


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
    #"Connection": "keep-alive"
})

BASE_ARTICLE_URL = "http://en.wikipedia.org/wiki/"

# Used to speed up the search and avoid infinite loops
visited_sites = list[str]()


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
        if all(c not in a_tag["href"] for c in BLACKLISTED_CHARACTERS) and sub_path not in visited_sites:
            urls.add(sub_path)
    return urls


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("Too many arguments!")
        print("Usage: python wiki_linker.py article_A article_B")
    
    if len(sys.argv) < 3:
        print("Too few arguments!")
        print("Usage: python wiki_linker.py article_A article_B")
    
    article_a = sys.argv[1]
    article_b = sys.argv[2]

    print("Article A:")
    for link in extract_links(article_a):
        print(link)
    print("\nArticle B:")
    for link in extract_links(article_b):
        print(link)
