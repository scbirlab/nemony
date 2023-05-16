"""Command line interface for nemony."""

import argparse
import sys

from .nemony import encode, _get_corpus

def _interactive_session() -> None:

    print("\n(Ctrl-C to exit.)\nWhat would you like to encode?\n",
          file=sys.stderr)

    while True:

        try:
            x = input("?> ")

            print(encode(x))

        except KeyboardInterrupt:

            break

    return None


def main() -> None:

    parser = argparse.ArgumentParser(description='''
    Encode lines of text deterministically as adjective-noun mnemonics.
    ''')
    parser.add_argument('input', 
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        nargs='?',
                        help='File to read and emit one mnemonic per line. Default STDIN.')
    parser.add_argument('--interactive', '-i', 
                        action='store_true',
                        help='Run interactively.')
    parser.add_argument('--output', '-o', 
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        nargs='?',
                        help='Output file. Default STDOUT.')
    
    args = parser.parse_args()

    adjectives, nouns = _get_corpus()

    print('\n## MNEMO: Generate adjective-noun mnemonics',
          file=sys.stderr)
    print(f'Word list version: {encode(adjectives + nouns)}\n',
          f'- Number of adjectives: {len(adjectives)}\n',
          f'- Number of nouns: {len(nouns)}\n',
          f'- Combinations: {len(adjectives) * len(nouns)}\n',
          file=sys.stderr)
    
    if args.interactive:

        _interactive_session()

    else:

        for line in args.input:

            args.output.write(encode(line.strip()) + '\n')

    return None


if __name__ == '__main__':

    main()
