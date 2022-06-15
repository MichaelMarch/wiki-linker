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

For example if you run:
```
python wiki_linker.py William_L._Webber 12_Downing_Street
```

The output should be (as of 06-15-2022):
<details> 
  <summary>The output (click the arrow on the left to see it)</summary>
    The ladder is:<br>
    William_L._Webber<br>
    1876_Michigan_gubernatorial_election<br>
    1835_Michigan_gubernatorial_election<br>
    John_Biddle_(Michigan_politician)<br>
    Aaron_T._Bliss<br>
    51st_United_States_Congress<br>
    100th_United_States_Congress<br>
    1987_in_the_United_States<br>
    03_Greedo<br>
    Blink-182<br>
    2008_South_Carolina_Learjet_60_crash<br>
    BBC<br>
    2014_Scottish_independence_referendum<br>
    Deputy_Prime_Minister_of_the_United_Kingdom<br>
    12_Downing_Street<br><br>
    The number of unique articles found is: 36455
</details>  


### Benchmarking

There are set of benchmarks that show how different implementations perform. To try them out refer to the [benchmark.py](benchmark.py) file.

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

