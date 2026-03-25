try:
    from .patterns import capitalize_variations, append_numbers, apply_leetspeak, combine_words
except ImportError:
    from patterns import capitalize_variations, append_numbers, apply_leetspeak, combine_words

import os


def _expand_word_patterns(word):
    variants = set()
    base_variants = set(capitalize_variations(word))

    for base_word in base_variants:
        variants.add(base_word)
        variants.update(append_numbers(base_word))

        for leet_word in apply_leetspeak(base_word):
            variants.add(leet_word)
            variants.update(append_numbers(leet_word))

    return variants


def generate_wordlist(name=None, pet=None, dob=None, keyword=None):
    base_words = []

    for item in [name, pet, dob, keyword]:
        if item:
            normalized = str(item).strip().lower()
            if normalized:
                base_words.append(normalized)

    wordlist = set()

    for word in base_words:
        wordlist.update(_expand_word_patterns(word))

    if len(base_words) >= 2:
        combos = combine_words(base_words)
        for combo in combos:
            wordlist.update(_expand_word_patterns(combo))

    return wordlist


def export_wordlist(wordlist, filename="output/wordlist.txt"):
    os.makedirs(os.path.dirname(filename) or "output", exist_ok=True)

    with open(filename, "w", encoding="utf-8", newline="\n") as file_obj:
        for word in sorted(wordlist):
            file_obj.write(word + "\n")

    print(f"\n[OK] Wordlist saved to {filename}")
    print(f"Total words generated: {len(wordlist)}")
