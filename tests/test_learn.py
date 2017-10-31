#!/usr/bin/env python3
import unittest
import sys
import os
from collections import Counter
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import learn
from node import Node


class GeneratorTests(unittest.TestCase):

    def test_split_line(self):
        l = ['abc.']
        self.assertListEqual(list(learn.get_tokens(l)), ['abc', '.', '#'])

    def test_split_line_title(self):
        l = ['abc.', 'Def']
        self.assertListEqual(list(learn.get_tokens(l)),
                             ['abc', '.', '#', 'def'])

    def test_split_line_marks(self):
        l = ['abc.', 'Def, z! A a?']
        self.assertListEqual(list(learn.get_tokens(l)),
                             ['abc', '.', '#', 'def', ',', 'z', '!',
                              '#', 'a', 'a', '?', '#'])

    def test_add_text_simple(self):
        root = Node()
        learn.add_text([], root, 2, Counter())
        self.assertDictEqual(root.links, {'#': root.links['#']})

    def test_add_text_root(self):
        root = Node()
        learn.add_text(['a', 'b', 'a', '#'], root, 3, Counter())
        self.assertSetEqual(set(root.frequency[1].most_common()), {('b', 1)})
        self.assertSetEqual(set(root.frequency[0].most_common()), {('a', 1)})

    def test_add_sent_root(self):
        root = Node()
        root.add_edge('#')
        words = ['#']
        sent = ['London',  'is', 'the', 'capital', '.', '#']
        learn.add_sent(words, root, sent, 5)
        self.assertSetEqual(
            set(root.frequency[4].most_common()), {('London', 1)})
        self.assertSetEqual(set(root.frequency[3].most_common()), {('is', 1)})
        self.assertSetEqual(set(root.frequency[2].most_common()), {('the', 1)})
        self.assertSetEqual(
            set(root.frequency[1].most_common()), {('capital', 1)})
        self.assertSetEqual(set(root.frequency[0].most_common()), {('.', 1)})

    def test_add_sent_node(self):
        root = Node()
        root.add_edge('#')
        words = ['#']
        sent = ['London',  'is', 'the', 'capital', '.', '#']
        learn.add_sent(words, root, sent, 5)
        node = root.links['is']
        self.assertSetEqual(set(node.frequency[2].most_common()), {('the', 1)})
        self.assertSetEqual(set(node.frequency[3].most_common()), set())

    def test_add_sent_node_multy(self):
        root = Node()
        root.add_edge('#')
        words = ['#']
        sent = ['London',  'is', 'the', 'capital', '.', '#']
        learn.add_sent(words, root, sent, 5)
        sent = ['London', 'Pari', 'pigeons', 'roof', '.', '#']
        learn.add_sent(words, root, sent, 5)
        node = root.links['London']
        self.assertSetEqual(set(node.frequency[3].most_common()), {
                            ('is', 1), ('Pari', 1)})

    def test_get_tokens_simple(self):
        self.assertListEqual(list(learn.get_tokens(
            ['And now, I dont know, why? She wouldnt say goodby.'])),
            ['and', 'now', ',', 'I', 'dont', 'know',
             ',', 'why', '?', '#', 'she', 'wouldnt', 'say', 'goodby', '.', '#']
        )

    def test_get_tokens_multy(self):
        self.assertListEqual(list(learn.get_tokens(
            ['And now, I dont know, why?',
             'She wouldnt say goodby.'])),
            ['and', 'now', ',', 'I', 'dont', 'know',
             ',', 'why', '?', '#', 'she', 'wouldnt',
                              'say', 'goodby', '.', '#']
        )


def main():
    unittest.main()

if __name__ == "__main__":
    main()
