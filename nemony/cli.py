"""Command line interface for nemony."""

import argparse
import sys

from .nemony import _check_version, _get_wordlist, encode 

def _interactive_session() -> None:

    print("", "(Ctrl-C to exit.)", "What would you like to encode?",
          sep='\n',
          file=sys.stderr, flush=True)

    while True:

        try:

            x = input("?> ")
        
        except KeyboardInterrupt or EOFError:

            break

        else:

            if len(x) > 0:
                print(encode(x), flush=True)

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

    adjectives, nouns = _get_wordlist()
    version_name = _check_version()

    print('\n## MNEMO: Generate adjective-noun mnemonics',
          file=sys.stderr)
    print(f'Word list version: {version_name}\n',
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
