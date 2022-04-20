# -*- coding: utf-8 -*-
import argparse
import os
import time

from helpers import get_input
from solver_bruteforce import SolverBruteForce


def main(style, input_filename=None):
    print(f"style: {style}")

    if input_filename is None:
        # input_filename = "./input/input.json"
        input_filename = "./input/input_4_vehicles.json"
        # input_filename = "./input/input_single_vehicle.json"  # sil
    assert os.path.isfile(input_filename), f"Input file does not exist! {input_filename}"

    vrp_input = get_input(input_filename)
    assert "vehicles" in vrp_input, "Bad input file!"
    assert "jobs" in vrp_input, "Bad input file!"
    assert "matrix" in vrp_input, "Bad input file!"

    vehicles, jobs, matrix = vrp_input["vehicles"], vrp_input["jobs"], vrp_input["matrix"]
    solver = None
    if style == "bruteforce":
        solver = SolverBruteForce(vehicles, jobs, matrix)
    if solver is None:
        raise ValueError(f"Bad style: '{style}'")

    start = time.time()
    solver.solve()
    end = time.time()
    print(f"elapsed {end - start}sec.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--style", required=True, type=str)
    parser.add_argument("-f", "--filename", required=False, type=str)
    args = parser.parse_args()
    main(args.style, args.filename)
