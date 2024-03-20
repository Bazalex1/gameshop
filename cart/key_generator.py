import random
import string

def generate_random_key():
    all_characters = string.ascii_letters + string.digits
    part_a = ''.join(random.choice(all_characters) for _ in range(5))
    part_b = ''.join(random.choice(all_characters) for _ in range(5))
    part_c = ''.join(random.choice(all_characters) for _ in range(5))
    return f"{part_a}-{part_b}-{part_c}"

