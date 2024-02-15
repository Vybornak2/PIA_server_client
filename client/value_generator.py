import random

def generate_random_vector(length: int, min_value: float, max_value: float) -> list[float]:
    vector = []
    for _ in range(length):
        random_float = random.uniform(min_value, max_value)
        vector.append(random_float)
    return vector

def generate_vector3(min_value: float, max_value: float) -> list[float]:
    return generate_random_vector(3, min_value, max_value)

def generate_vector6(min_value: float, max_value: float) -> list[float]:
    return generate_random_vector(6, min_value, max_value)
