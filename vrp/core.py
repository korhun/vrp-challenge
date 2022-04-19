# -*- coding: utf-8 -*-
import argparse

from helpers import *


def main(style, input_filename=None):
    assert style in ["brute_force"]
    print(f"style: {style}")

    if input_filename is None:
        input_filename = "./input/input.json"
    assert os.path.isfile(input_filename)

    vrp_input = get_input(input_filename)
    assert "vehicles" in vrp_input
    assert "jobs" in vrp_input
    assert "matrix" in vrp_input

    print(vrp_input)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--style", required=True, type=str)
    parser.add_argument("-f", "--filename", required=False, type=str)
    args = parser.parse_args()
    main(args.style, args.filename)
