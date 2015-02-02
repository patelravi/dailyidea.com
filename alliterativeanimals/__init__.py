import random
import os

PATH = os.path.dirname(os.path.abspath(__file__))

ADJECTIVES_FILE = os.path.join(PATH, 'adjectives.txt')
with open(ADJECTIVES_FILE) as f:
    adjectives = [i.strip() for i in f.readlines()]

ANIMALS_FILE = os.path.join(PATH, 'animals.txt')
with open(ANIMALS_FILE) as f:
    animals = [i.strip() for i in f.readlines()]

def get_name():
    adjective = random.choice(adjectives)
    first_letter = adjective[0]
    animal = random.choice([i for i in animals if i[0] == first_letter])
    return "{} {}".format(adjective, animal)

if __name__ == "__main__":
    for i in range(100):
        print get_name()

