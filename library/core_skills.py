"""
Complete the following Python tasks in the core_skills.py file.
Create a list of 10 random numbers between 1 and 20.
Filter Numbers Below 10 (List Comprehension)
Filter Numbers Below 10 (Using filter)
"""
import random


def generate_10_random_numbers(
    start: int=1, end: int = 20
):
    """Generate random numbers between start and end (non-unique)"""
    return [
        random.randint(start, end)
        for _ in range(10)
    ]

def with_list_comprehension():
    rand_numbers = generate_10_random_numbers()
    return [
        i for i in rand_numbers
        if i < 10
    ]

def _filter_below_ten(x: int):
    return x < 10


def with_filter():
    rand_numbers = generate_10_random_numbers()
    return list(filter(_filter_below_ten, rand_numbers))


if "__main__" == __name__:
    print(generate_10_random_numbers())
    print(with_list_comprehension())
    print(with_filter())