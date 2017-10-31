import random


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = int(random.uniform(0, total))
    current_sum = 0
    for c, w in choices:
        if current_sum + w > r:
            return c
        current_sum += w
    raise IndexError('list index out of range')
