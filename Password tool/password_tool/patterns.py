import itertools
from datetime import datetime

# Character replacements commonly used in weak passwords.
LEET_MAP = {
    "a": ["4", "@"],
    "b": ["8"],
    "e": ["3"],
    "g": ["9"],
    "i": ["1", "!"],
    "l": ["1"],
    "o": ["0"],
    "s": ["5", "$"],
    "t": ["7"],
    "z": ["2"],
}


def capitalize_variations(word):
    return [word.lower(), word.upper(), word.capitalize()]


def append_numbers(word):
    current_year = datetime.now().year
    years = [str(year) for year in range(1990, current_year + 2)]
    common_suffixes = [
        "1", "12", "123", "1234", "12345", "007", "111", "000", "69", "420"
    ]

    values = set()
    for suffix in common_suffixes + years:
        values.add(f"{word}{suffix}")
        values.add(f"{word}_{suffix}")
        values.add(f"{word}-{suffix}")

    return sorted(values)


def apply_leetspeak(word, max_variants=256):
    if not word:
        return []

    replacement_sets = []
    for char in word:
        options = [char]
        mapped = LEET_MAP.get(char.lower(), [])
        for item in mapped:
            if item not in options:
                options.append(item)
        replacement_sets.append(options)

    variations = set()
    for combo in itertools.product(*replacement_sets):
        variations.add("".join(combo))
        if len(variations) >= max_variants:
            break

    return sorted(variations)


def combine_words(words):
    separators = ["", "_", "-", ".", "@"]
    combinations = []

    for pair in itertools.permutations(words, 2):
        for separator in separators:
            combinations.append(f"{pair[0]}{separator}{pair[1]}")

    return combinations
