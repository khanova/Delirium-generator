#!/usr/bin/env python3
import unittest
import sys
import os
from collections import Counter
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import gen
import node
from node import Node


class GeneratorTests(unittest.TestCase):

    def test_title(self):
        l = ['abc']
        self.assertEqual(gen.sent_to_string(l, Counter()), 'Abc')

    def test_end(self):
        l = ['abc', '.']
        self.assertEqual(gen.sent_to_string(l, Counter()), 'Abc.')

    def test_marks(self):
        l = ['abc', ',', 'def', 'z', '?']
        self.assertEqual(gen.sent_to_string(l, Counter()), 'Abc, def z?')

    def test_generate_next_token_simple(self):
        w = []
        r = Node()
        r.add_word('a', 0)
        self.assertEqual(gen.generate_next_token(w, r, 0, 1), 'a')

    def test_generate_next_token_choose(self):
        w = []
        r = Node()
        r.add_word('b', 1)
        r.add_word('a', 0)
        self.assertEqual(gen.generate_next_token(w, r, 0, 1), 'a')

    def test_generate_next_token_out_of_range(self):
        w = []
        r = Node()
        r.add_word('b', 1)
        r.add_word('a', 0)
        r.add_word('c', node.MAGIC)
        self.assertEqual(gen.generate_next_token(w, r, 10, 100), 'c')

    def test_generate_next_sent_simple(self):
        w = []
        r = Node()
        r.add_word('!', 0)
        self.assertEqual(gen.generate_next_sent(w, r, 1, 2), ['!'])

    def test_generate_next_sent(self):
        w = []
        r = Node()
        r.add_word('London', 4)
        r.add_word('is', 3)
        r.add_word('the', 2)
        r.add_word('capital', 1)
        r.add_word('.', 0)
        self.assertEqual(gen.generate_next_sent(w, r, 5, 6), [
                         'London',  'is', 'the', 'capital', '.'])

    def test_to_normal_case_name(self):
        c = Counter()
        c['Anna'] = 10
        self.assertEqual(gen.to_normal_case('Anna', c), 'Anna')

    def test_to_normal_case_title(self):
        c = Counter()
        c['Book'] = 10
        c['book'] = 11
        self.assertEqual(gen.to_normal_case('Book', c), 'book')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
