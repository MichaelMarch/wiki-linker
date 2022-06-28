import os
import timeit

from ladders.local_wiki_ladder_finder import LocalWikiLadderFinder
from io import TextIOBase

LADDER_INPUTS = [
    ("Fruit", "Strawberry"),
    ("Slug", "Strawberry"),
    ("Europe", "Slug"),
    ("Back_in_Time_(2015_film)", "Zabolotiv"),
    ("France", "Ottawa"),
    ("Peloponnese", "Back_in_Time_(2015_film)")
]


def benchmark_find_ladder(input):
    ladder_finder = LocalWikiLadderFinder(100)
    print_and_write(fp, f"Input: {input[0]}, {input[1]}")
    print_and_write(fp, f"Output: {ladder_finder.find(*input)}")


def run(benchmark, input, fp, number_of_runs=1):
    """
    `benchmark`: pointer to a bencharking function (see above)
    `input`: a 2 element tuple where each element is an article name
    `number_of_runs`: the amount of times that the benchmark should be repeated
    """
    print_and_write(fp, f"-------------{benchmark.__name__}-------------")
    total_duration = timeit.Timer(lambda: benchmark(input)).timeit(number=number_of_runs)

    print_and_write(fp, f"Total time for {number_of_runs} run(s): {total_duration} seconds")
    if number_of_runs > 1:
        print_and_write(fp, f"The average time was: {total_duration / number_of_runs} seconds")


def print_and_write(fp: TextIOBase, message: str):
    print(message)
    fp.write(message)


if __name__ == "__main__":
    with open("app/benchmark_results/results.txt", "w") as fp:

        print_and_write(fp, f"Available cpu's: {os.cpu_count()}")
        print_and_write(fp, "")

        for input in LADDER_INPUTS:
            run(benchmark_find_ladder, input, fp)
