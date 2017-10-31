#!/usr/bin/python
import argparse
import learn
import gen
from sys import argv


def init_parser():
    parser = argparse.ArgumentParser(prog="bredogenerator")
    subparsers = parser.add_subparsers(
        title='available subcommands',
        description='',
        help='DESCRIPTION',
        metavar="SUBCOMMAND",
    )

    subparsers.required = True

    learn.add_parser(subparsers)
    gen.add_parser(subparsers)
    return parser


def main():
    parser = init_parser()
    options = parser.parse_args(argv[1:])
    options.func(options)


if __name__ == '__main__':
    main()
