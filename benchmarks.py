import wiki_linker
import timeit

EXTRACT_INPUTS = [
    "Europe"
]

LADDER_INPUTS = [
    ("William_L._Webber", "12_Downing_Street"),
    ("Slug", "Strawberry"),
    ("Gregory_Krumbock", "Potok_Cave")
]


def benchmark_extract_links(input):
    print(f"Input: {input[0]}")
    wiki_linker.extract_links(input[0])


def benchmark_find_ladder(input):
    print(f"Input: {input[0]}, {input[1]}")
    print(f"Output: {wiki_linker.find_ladder(input[0], input[1])}")
    print(f"The number of unique articles found is: {len(wiki_linker.extracted_articles)}")


# The first arguemnt should be a function reference (not a function call!) with 0 parameters
# The second one speciefies how many times the function will be called.
def run(benchmark, input, number_of_runs=100):
    print(f"-------------{benchmark.__name__}-------------")

    total_duration = timeit.Timer(lambda: benchmark(input)).timeit(number=number_of_runs)

    print(f"Total time for {number_of_runs} run(s): {total_duration} seconds")
    if number_of_runs > 1:
        print(f"The average time was: {total_duration/number_of_runs} seconds")


if __name__ == "__main__":
    run(benchmark_find_ladder, LADDER_INPUTS[0], 1)
