import argparse
import cowsay as cs

parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(cs.cowsay(args.square))
