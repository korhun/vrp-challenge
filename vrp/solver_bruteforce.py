import itertools
import sys

from helpers import partition, lists_overlap, routes_cost_is_smaller_than, calculate_all_routes_costs, print_same_line


class SolverBruteForce:

    def __init__(self, vehicles, jobs, matrix, verbose=None):
        self.vehicles, self.jobs, self.matrix, self.verbose = vehicles, jobs, matrix, verbose

    @staticmethod
    def _get_partitions_that_contain_vehicles(locations, vehicle_start_locations):
        for part in partition(locations):
            all_routes_contain_vehicle = True
            for route in part:
                if not lists_overlap(route, vehicle_start_locations):
                    all_routes_contain_vehicle = False
                    break
            if all_routes_contain_vehicle:
                yield part

    @staticmethod
    def __get_sub_parts(parts_permutations, prev_parts, current_index):
        if current_index == len(parts_permutations):
            yield prev_parts
            return
        for i in [current_index]:
            if i >= len(parts_permutations):
                break
            parts_current = parts_permutations[i]
            for part in parts_current:
                prev_parts1 = [*prev_parts, part]
                for sub_part in SolverBruteForce.__get_sub_parts(parts_permutations, prev_parts1, current_index + 1):
                    yield sub_part

    @staticmethod
    def _combine_permutations(parts_permutations):
        if not parts_permutations:
            return
        parts0 = parts_permutations[0]
        for part0 in parts0:
            for routes in SolverBruteForce.__get_sub_parts(parts_permutations, [part0], 1):
                yield routes

    @staticmethod
    def get_all_routes(locations, vehicle_start_locations):
        for parts in SolverBruteForce._get_partitions_that_contain_vehicles(locations, vehicle_start_locations):
            parts_permutations = []
            for part in parts:
                part_permutations = []
                for v_start in vehicle_start_locations:
                    if v_start in part:
                        part_without_v_start = [i for i in part if i != v_start]
                        permutations_without_vehicle = itertools.permutations(part_without_v_start, len(part_without_v_start))
                        part_permutations += [[v_start, *part1] for part1 in permutations_without_vehicle]
                parts_permutations.append(part_permutations)

            # test
            # if len(parts_permutations) != 4:
            #     continue

            for routes in SolverBruteForce._combine_permutations(parts_permutations):
                yield routes

    def solve(self):
        locations = list(range(len(self.matrix)))
        vehicle_start_locations = [vehicle["start_index"] for vehicle in self.vehicles]

        best_routes = None
        min_dist = sys.maxsize

        count = 0
        for routes in self.get_all_routes(locations, vehicle_start_locations):
            count += 1
            if self.verbose:
                print_same_line(f"{routes}  count: {count:,}")
            is_smaller, dist = routes_cost_is_smaller_than(routes, self.matrix, min_dist)
            if is_smaller:
                best_routes = routes
                assert calculate_all_routes_costs(routes, self.matrix) == dist
                min_dist = dist
                print(f"\rmin_dist: {min_dist} - {best_routes}")

        print("\r*********** finished ***********")
        print(f"min_dist: {min_dist} - {best_routes}  count:{count:,}")
