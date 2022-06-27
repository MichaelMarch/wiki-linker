# Wiki Linker

A python bot for finding a path (of articles) between 2 Wikipedia articles.

## Prerequisites

You need to prepare several things before you can test the project:
- A [kiwix application](https://www.kiwix.org/en/download/)
- The copy of this project
- Python 3.7+
- At least 55 GB of free disk space

Note: This project can scrape both [Wikipedia](https://wikipedia.org/) and any other site that hosts the Wikipedia project. I advise you not to scrape any of the existing mirrors and instead host one yourself. [Why you should do it](https://en.wikipedia.org/wiki/Wikipedia:Database_download#Please_do_not_use_a_web_crawler).

## Installing

### Kiwix

Head over to https://www.kiwix.org/en/download/ and get kiwix for your platform.
Once you open it search for Wikipedia and download the wiki that has around 46 GB.
To host the wiki press (CTRL + I) and click "Start kiwix server". Then click "Open in browser", click on the tile that has "Wikipedia" on it and write down the url.

### Project setup

First make sure you have Python 3.7+ installed.

```
python --version
```

Clone the repository and create new virtual environment
```
python -m venv .venv
```

Then enter the environment:

```
# for Windows (powershell)
.\.venv\Scripts\activate

# or for UNIX systems
source .venv\Scripts\activate.sh
```

Finally you should install the required modules by running:

```
pip install -r requirements.txt
```

### Running the project

```
python wiki_linker.py article_A article_B
```

## Benchmarking

Refer to the [benchmarks.py](benchmarks.py) file for more information.  
Several articles were chosen to test this program. The results can be seen in [benchmark_results](benchmark_results/results.txt).  

Running the benchmark:

```
python benchmark.py
```

## Implementation

Since Wikipedia is enormous a simple algorithm that just checks all articles in the order of their appearance is not enough. To speed things up there needs to be a way for the algorithm to make smart decisions based on the available data.

One way of doing that is assigning priorities for each algorithm's path. A priority is a number that determines how many pages an article has with the end page in common. The reasoning is that if an article has a high amount of pages in common with the end page chances are they're closely related to each other.

## Motivation

Ever since I started playing wikiracer, which I am really bad at to this day, I wanted to see if a machine could beat a human. But I could never find time to do so.  

The opportunity came at the end of the semester of Computer Programming class which results can be seen here.

## Challanges

1. Extracting links from an article:
> When I started this project I was scraping Wikipedia servers. Due to its ecosystem, it was hard to find all the correct links. Some of them were bookmarks to other parts of the same article and some pointed outside Wikipedia. I solved it with the help of BeautifulSoup and more precisely the SoupStrainer. Later on, when I switched to kiwix local hosting the filtering that needed to be done was minimal. 
2. Getting slowed down by Wikipedia:
> Making too many requests to a site will result in a forcibly slowed connection or even a temporary ban. To mitigate this I looked around for a way to host wikipedia myself and found kiwix.
3. The performance is terrible:
> As of now if articles aren't related enough the priority queue implementation of the algorithm will perform poorly.

## Development

The project was created and tested only on Windows. Don't know if the project runs on other platforms. I am 90% sure it will run faster on UNIX.

Any contribution is welcome :)

## License

This project is unlicensed - please refer to the [LICENSE](LICENSE) file for more details.

