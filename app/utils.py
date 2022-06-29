import requests


def parse_requirements() -> dict[str, str]:
    with open("requirements.txt") as file_pointer:
        lines = file_pointer.readlines()

    packages = dict[str, str]()

    for line in lines:
        parts = line.split("==")
        packages[parts[0]] = f"v{parts[1]}"

    return packages


def get_random_article() -> str:
    response = requests.get("http://192.168.100.101:8080/random?content=wikipedia_en_all_maxi_2022-05")

    if not response.status_code == 200:
        return None

    return response.url[response.url.rfind('/') + 1:]
