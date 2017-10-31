from collections import Counter
import random_extention

MAGIC = 5


class Node():
    '''Node in trie'''

    def __init__(self, par=None):
        self.links = {}
        self.frequency = [Counter() for i in range(MAGIC + 1)]
        self.par = par

    def add_edge(self, word):
        return self.links.setdefault(word, Node(self))

    def add_word(self, word, left):
        left = min(left, MAGIC)
        self.frequency[left][word] += 1

    def get_rand(self, left):
        left = min(left, MAGIC)
        if left < 0:
            raise IndexError('list index out of range')
        return random_extention.weighted_choice(
            self.frequency[left].most_common())

    def try_get_next(self, word):
        if not word in self.links:
            return self, False
        return self.links[word], True
