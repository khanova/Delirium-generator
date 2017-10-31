import pickle
import node
import sys
import random
from contextlib import suppress
from node import Node
TERM = '#'


def generate_next_token(words, root, l, r):
    node = root
    tokens = []
    for i in range(r - 1, l - 1, -1):
        with suppress(IndexError):
            tokens.append(node.get_rand(i))
            
    for context in reversed(words):
        node, is_ok = node.try_get_next(context)
        if not is_ok:
            break
        for i in range(r - 1, l - 1, -1):
            with suppress(IndexError):
                tokens.append(node.get_rand(i))

    return tokens[-1]


def generate_next_sent(words, root, l, r):
    count = 0
    sent = [TERM]
    l = l + int(random.uniform(0, r - l))
    while not sent[-1] in '.!?' or count < l:
        count += 1
        word = generate_next_token(words, root, l - count, r - count)
        sent.append(word)
        words.append(word)
    words.append(TERM)
    return list(filter(lambda w: w != TERM, sent))


def to_normal_case(token, freq):
    return token if freq[token] >= freq[token.lower()] else token.lower()


def sent_to_string(sent, freq):
    str_sent = [sent[0].title()]
    for token in sent[1:]:
        if not token in ',.!?':
            str_sent[-1] += ' '
        str_sent.append(to_normal_case(token, freq))
    return ''.join(str_sent)


def gen(tree_data_file, count, file, length_bound):
    l, r = length_bound[0], length_bound[1] + 1
    if r <= l:
        print('Minimum number of words({0}) \
must be not greater than maximum({1})'.format(l, r - 1))
        sys.exit(1)
    try:
        with open(tree_data_file, 'rb') as f:
            root, depth, freq = pickle.load(f)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    words = [TERM]
    out = ''
    for i in range(count):
        out += sent_to_string(generate_next_sent(words,
                                                 root, l, r), freq) + ' '

    if not file:
        print(out)
    else:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(out)


def add_parser(subparsers):
    parser_gen = subparsers.add_parser(
        'generate',
        help='Generate text'
    )
    parser_gen.add_argument('-c', '--count',
                            type=int, default=10,
                            help='Number of generated sentences')
    parser_gen.add_argument('-l', '--length', type=int, nargs=2,
                            default=(3, 10), metavar=('MINIMUM', 'MAXIMUM'),
                            help='Minimum and maximum length of the sentences')
    parser_gen.add_argument(
        'file', help='File with serialization context tree')
    parser_gen.add_argument('--out', help='Output file')
    parser_gen.set_defaults(func=lambda options: gen(
        options.file, options.count, options.out, options.length))
