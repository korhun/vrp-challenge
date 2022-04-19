import argparse
from core import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", required=False, type=str)
    args = parser.parse_args()
    main("brute_force", args.filename)
