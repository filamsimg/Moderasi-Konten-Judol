import re

LEET_MAP = str.maketrans({
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "8": "b",
    "9": "g",
})


def _collapse_spaced_letters(text: str) -> str:
    pattern = re.compile(r"\b(?:[a-zA-Z]\s+){2,}[a-zA-Z]\b")

    def repl(match: re.Match) -> str:
        return match.group(0).replace(" ", "")

    return pattern.sub(repl, text)


def normalize_text(text: str) -> str:
    if not text:
        return ""
    normalized = text.lower()
    normalized = re.sub(r"(https?://\S+|www\.\S+)", "<URL>", normalized)
    normalized = normalized.translate(LEET_MAP)
    normalized = _collapse_spaced_letters(normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized
