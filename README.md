# Wiki Linker

A python bot for finding a path (of articles) between 2 Wikipedia articles.

## Usage

### Prerequisites and Installing
To try this project you should have the modules that are listed in [requirements.txt](requirements.txt) installed. The best way to do this is to create a virtual environment:

```
python -m venv .venv
```

and then enter the virtual environment:

```
# for Windows (powershell)
.\.venv\Scripts\activate

# or for UNIX systems
source .venv\Scripts\activate.sh
```

Finally you can install the required modules by:

```
pip install -r requirements.txt
```

### Running the project

```
python wiki_linker.py article_A article_B
```

### Benchmarking

There are set of benchmarks that show how different implementations perform. To try them out refer to the [benchmarks.py](benchmarks.py) file.

```
python benchmark.py
```

I also provide some results of my own from testing the project in [benchmark_results/](benchmark_results/)

## Implementation

Since Wikipedia is enormous a simple algorithm that just checks all articles in the order of their appearance is not enough. To speed things up there needs to be a way for the algorithm to make smart decisions based on the available data.

One way of doing that is assigning priorities for each algorithm's path. A priority is a number that determines how many pages an article has with the end page in common. The reasoning is that if an article has a high amount of pages in common with the end page chances are they're closely related to each other.

## Development

The project was created and tested only on Windows. Don't know if the project runs on other platforms. I am 90% sure it will run faster on UNIX.

Any contribution is welcome :)

## License

This project is unlicensed - please refer to the [LICENSE](LICENSE) file for more details.

