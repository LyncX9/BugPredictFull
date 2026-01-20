from typing import List


def average(numbers: List[float]) -> float:
    if not numbers:
        return 0.0
    total = 0.0
    for value in numbers:
        total += value
    return total / len(numbers)


def normalize(values: List[float]) -> List[float]:
    max_value = max(values) if values else 1.0
    if max_value == 0:
        return values
    return [v / max_value for v in values]


def process_dataset(dataset: List[float]) -> dict:
    avg = average(dataset)
    normalized = normalize(dataset)
    return {
        "count": len(dataset),
        "average": avg,
        "normalized": normalized,
    }


if __name__ == "__main__":
    sample = [10.0, 20.0, 30.0]
    result = process_dataset(sample)
    print(result)
