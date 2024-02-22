import sys
import argparse
from cowsay import cowsay, list_cows

def main():
    parser = argparse.ArgumentParser(description='Program similar to cowsay')
    parser.add_argument(
            '-t',
            '--text',
            help='The text to be said'
            )
    parser.add_argument(
            '-f',
            '--file',
            help='Specify the cowfile',
            default='default'
            )
    parser.add_argument(
            '-e',
            '--eyes',
            help='Change the eyes', 
            default='o0'
            )
    parser.add_argument(
            '-T',
            '--tongue',
            help='The tongue file',
            default='U'
            )
    parser.add_argument(
            '-l',
            '--list', 
            action='store_true', 
            help='List available cowfiles'
            )
    args = parser.parse_args()

    if args.list:
        print(list_cows())
    else:
        print(
            cowsay(
                args.text, 
                cow=args.file,
                eyes=args.eyes,
                tongue=args.tongue
                )
            )

if __name__ == '__main__':
    main()
