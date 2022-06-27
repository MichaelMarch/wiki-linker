import os
import timeit

from ladders.local_wiki_ladder_finder import LocalWikiLadderFinder


LADDER_INPUTS = [
    ("Fruit", "Strawberry"),
    ("Slug", "Strawberry"),
    ("Europe", "Slug"),
    ("Back_in_Time_(2015_film)", "Zabolotiv"),
    ("France", "Ottawa"),
    ("Peloponnese", "Back_in_Time_(2015_film)")
]


def benchmark_find_ladder(input):
    ladder_finder = LocalWikiLadderFinder(*input, 100)
    print(f"Input: {input[0]}, {input[1]}")
    print(f"Output: {ladder_finder.find()}")


def run(benchmark, input, number_of_runs=1):
    """
    `benchmark`: pointer to a bencharking function (see above)
    `input`: a 2 element tuple where each element is an article name
    `number_of_runs`: the amount of times that the benchmark should be repeated
    """
    print(f"-------------{benchmark.__name__}-------------")
    total_duration = timeit.Timer(lambda: benchmark(input)).timeit(number=number_of_runs)

    print(f"Total time for {number_of_runs} run(s): {total_duration} seconds")
    if number_of_runs > 1:
        print(f"The average time was: {total_duration / number_of_runs} seconds")


if __name__ == "__main__":
    print(f"Available cpu's: {os.cpu_count()}")
    print()
    
    #for input in LADDER_INPUTS:
    #    run(benchmark_find_ladder, input)
    run(benchmark_find_ladder, LADDER_INPUTS[-1])