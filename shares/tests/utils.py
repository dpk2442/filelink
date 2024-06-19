import random
import string


def create_random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=20))
