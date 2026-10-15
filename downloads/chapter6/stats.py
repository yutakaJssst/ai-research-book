# 第6章6.5節で説明した平均値の関数（コードはWebサポートに掲載）
def calculate_average(numbers):
    """Return the average of a list of numbers."""
    if not numbers:
        raise ValueError("numbers must not be empty")
    return sum(numbers) / len(numbers)
