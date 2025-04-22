def get_level(total_score: int) -> int:
    max_level = 15
    base = 5
    exponent = 1.1
    level = ((total_score * (exponent + 1)) / base) ** (1 / (exponent + 1))
    return min(max(int(level), 1), max_level)
