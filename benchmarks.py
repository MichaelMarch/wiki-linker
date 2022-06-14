import wiki_linker
import timeit


def benchmark_extract_links():
    wiki_linker.extract_links("Europe")


def run(benchmark, number_of_runs=100):
    total_duration = timeit.Timer(benchmark).timeit(number=number_of_runs)

    print(f"-------------{benchmark.__name__}-------------")
    print(f"Total time for {number_of_runs} runs: {total_duration}")
    print(f"The average time was: {total_duration/number_of_runs}")


if __name__ == "__main__":
    run(benchmark_extract_links, 1)
