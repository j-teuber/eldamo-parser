def replace(string: str, replacements: list) -> str:
    for old, new in replacements:
        string = string.replace(old, new)

    return string
