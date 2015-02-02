import random

with open("adjectives.txt") as f:
    adjectives = [i.strip() for i in f.readlines()]

with open("animals.txt") as f:
    animals = [i.strip() for i in f.readlines()]


def get_name():
    adjective = random.choice(adjectives)
    first_letter = adjective[0]
    animal = random.choice([i for i in animals if i[0] == first_letter])
    return "{} {}".format(adjective, animal)

import string
letters = string.letters[:26]

total = 0
for letter in letters:
    foo = len([i for i in adjectives if i.startswith(letter)])
    bar = len([i for i in animals if i.startswith(letter)])
    print "{}: {} * {} = {}".format(letter,
                               foo,
                               bar,
                               foo * bar
                              )
    total += foo * bar

print "TOTAL", total


