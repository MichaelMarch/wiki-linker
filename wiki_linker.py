import sys

from ladders.ladder_finder import LadderFinder
from ladders.local_wiki_ladder_finder import LocalWikiLadderFinder
from ladders.wiki_ladder_finder import WikiLadderFinder

if __name__ == "__main__":
    if sys.version_info < (3, 7):
        print("This program requires python version 3.7+.")
        exit(-1)

    if len(sys.argv) > 4:
        print("Too many arguments!")
        print("Usage: python wiki_linker.py article_A article_B")
        exit(-2)

    if len(sys.argv) < 3:
        print("Too few arguments!")
        print("Usage: python wiki_linker.py starting_article ending_article")
        exit(-3)

    starting_article = sys.argv[1]
    ending_article = sys.argv[2]

    if len(sys.argv) == 4 and sys.argv[3] == "online":
        ladder_finder: LadderFinder = WikiLadderFinder(starting_article, ending_article, 100)
    else:
        ladder_finder: LadderFinder = LocalWikiLadderFinder(starting_article, ending_article, 100)

    print("The ladder is: ")
    for step in ladder_finder.find():
        print(step)
