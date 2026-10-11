# 第6章6.5節に掲載した関数（本文と同一）
def calculate_average(numbers):
    """Return the average of a list of numbers."""
    if not numbers:
        raise ValueError("numbers must not be empty")
    return sum(numbers) / len(numbers)
