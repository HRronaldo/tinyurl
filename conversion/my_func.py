import random


def generate_short_key():
    char_set = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    short_key = ""
    for i in range(6):
        random_num = random.randint(0, 61)
        short_key += char_set[random_num]

    return short_key
