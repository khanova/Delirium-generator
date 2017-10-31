import sys
import pickle
import re
from node import Node
from collections import Counter
r = re.compile(r'[\w0-9-]+|[.,?!]+')
TERM = '#'


def add_sent(words, root, sent, depth):
    for i, word in enumerate(sent):
        node = root
        node.add_word(word, len(sent) - i - 2)
        for context in reversed(words):
            node = node.add_edge(context)
            node.add_word(word, len(sent) - i - 2)
            if context == TERM:
                break

        words.append(word)
        if len(words) > depth:
            words.pop(0)


def add_text(tokens, root, depth, freq):
    words = [TERM]
    root.add_edge(TERM)
    sent = []
    for token in tokens:
        freq[token] += 1
        sent.append(token)
        if token == TERM:
            add_sent(words, root, sent, depth)
            sent = []
            count = 0


def get_lines(file, encoding):
    if not file:
        return sys.stdin.readlines()
    else:
        with open(file, 'r', encoding=encoding) as f:
            return f.readlines()


def get_tokens(lines):
    after_end = True
    for line in lines:
        for token in r.findall(line):
            if token == '--':
                continue
            if after_end:
                yield token.lower()
            else:
                yield token
            after_end = False
            if token in '.!?':
                yield TERM
                after_end = True


def learn(depth, encoding, files, result, tree_data_file):
    root = Node()
    freq = Counter()
    try:
        with open(tree_data_file, 'rb') as f:
            root, depth, freq = pickle.load(f)
    except Exception:
        pass

    for file in files:
        add_text(get_tokens(get_lines(file, encoding)), root, depth, freq)

    try:
        with open(result, 'wb') as f:
            pickle.dump((root, depth, freq), f)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def add_parser(subparsers):
    parser_learn = subparsers.add_parser(
        'learn',
        help='Learn on texts'
    )

    parser_learn.add_argument('-e', '--encoding',
                              default='utf-8',
                              help='Files encoding default utf-8')
    parser_learn.add_argument('-r', '--relearn',
                              help='File with serialization context tree')
    parser_learn.add_argument('-d', '--depth',
                              type=int, default=5,
                              help='Length of n-grams')
    parser_learn.add_argument('result', help='File to save learning result')
    parser_learn.add_argument(
        'file', nargs='*', default=[None],
        help='List of files to add if empty -- stdin')
    parser_learn.set_defaults(func=lambda options: learn(
        options.depth, options.encoding, options.file,
        options.result, options.relearn))
