def parse_requirements() -> dict[str, str]:
    with open("requirements.txt") as file_pointer:
        lines = file_pointer.readlines()
    
    packages = dict[str, str]()

    for line in lines:
        parts = line.split("==")
        packages[parts[0]] = f"v{parts[1]}"
    
    return packages