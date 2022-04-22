# -*- coding: utf-8 -*-
import argparse
import json
import os
import time

from helpers import load_json_file
from solver_bruteforce import SolverBruteForce


def _default_options(verbose=None, limited_capacity=None, include_service=None):
    return {
        "verbose": verbose if verbose is not None else False,
        "limited_capacity": limited_capacity if limited_capacity is not None else False,
        "include_service": include_service if include_service is not None else False,
    }


def main(style, input_filename=None, options=None):
    if input_filename is None:
        input_filename = "./input/input.json"
        # input_filename = "./input/input_4_vehicles.json"
        # input_filename = "./input/input_single_vehicle.json"
    if options is None:
        options = _default_options()
    for key in _default_options().keys():
        assert key in options
    assert os.path.isfile(input_filename), f"Input file does not exist! {input_filename}"

    vrp_input = load_json_file(input_filename)
    assert "vehicles" in vrp_input, "Bad input file!"
    assert "jobs" in vrp_input, "Bad input file!"
    assert "matrix" in vrp_input, "Bad input file!"

    vehicles, jobs, matrix = vrp_input["vehicles"], vrp_input["jobs"], vrp_input["matrix"]
    solver = None
    if style == "bruteforce":
        solver = SolverBruteForce(vehicles, jobs, matrix, options)
    if solver is None:
        raise ValueError(f"Bad style: '{style}'")

    if options["limited_capacity"]:
        solver_info = f"style: {style} - limited capacity"
    else:
        solver_info = f"style: {style} - unlimited capacity"
    if options["include_service"]:
        solver_info = f"{solver_info} - job service times are included"
    print(solver_info)

    start = time.time()
    plan = solver.solve()
    end = time.time()

    print("🐢🐢🐢 finished 🐢🐢🐢")
    print(f"elapsed time: {(end - start):.2}sec")
    if plan is None:
        print("No feasible solution could be found!")
    else:
        print(json.dumps(plan, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--style", required=True, type=str)
    parser.add_argument("-f", "--filename", required=False, type=str)
    parser.add_argument("-v", "--verbose", required=False, action='store_true')
    parser.add_argument("-l", "--limited_capacity", required=False, action='store_true')
    parser.add_argument("-i", "--include_service", required=False, action='store_true')
    args = parser.parse_args()
    main(args.style, args.filename, _default_options(args.verbose, args.limited_capacity, args.include_service))
