import itertools
import sys

from helpers import partition, lists_overlap, routes_distance_is_smaller_than, calculate_all_routes_distance, print_same_line


class SolverBruteForce:

    def __init__(self, vehicles, jobs, matrix, verbose=None):
        self.vehicles, self.jobs, self.matrix, self.verbose = vehicles, jobs, matrix, verbose

    @staticmethod
    def _get_partitions_that_contain_vehicles(locations, vehicle_start_locations):
        # sil = list(partition(locations))
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
        if current_index == 1:  # sil
            aaa = 111 + 1

        if current_index == len(parts_permutations):
            yield prev_parts
            return
        # for i in range(current_index, len(parts_permutations)):
        for i in [current_index]:
            if i >= len(parts_permutations):
                break
            parts_current = parts_permutations[i]
            for part in parts_current:
                prev_parts1 = [*prev_parts, part]
                # sil = list(get_sub_parts(prev_parts1, current_index+1))

                for sub_part in SolverBruteForce.__get_sub_parts(parts_permutations, prev_parts1, current_index + 1):
                    yield sub_part

                # sub_parts = list(SolverBruteForce.__get_sub_parts(parts_permutations, prev_parts1, current_index + 1))
                # if len(sub_parts) == 1 and sub_parts[0] == prev_parts1:
                #     yield prev_parts1
                # else:
                #     for sub_part in sub_parts:
                #         yield [*prev_parts1, *sub_part]

                # for sub_parts in get_sub_parts(prev_parts1, current_index+1):
                #     yield sub_parts

    @staticmethod
    def _combine_permutations(parts_permutations):
        if not parts_permutations:
            return
        parts0 = parts_permutations[0]
        for part0 in parts0:
            # sil = list(get_sub_parts(part0, 1))
            # aaa = 1+6
            for routes in SolverBruteForce.__get_sub_parts(parts_permutations, [part0], 1):
                yield routes

        # for part_index, permutations_of_the_part in enumerate(parts_permutations):
        #     if part_index > current_index:
        #         for permutation in permutations_of_the_part:
        #             sub_permutations = list(SolverBruteForce._combine_permutations(parts_permutations, part_index))
        #             if len(sub_permutations) > 0:
        #                 # yield [permutation, *sub_permutations]
        #                 for sub_per in sub_permutations:
        #                     yield [permutation, sub_per]
        #             else:
        #                 # yield [permutation] if current_index < 0 else permutation
        #                 if current_index < 0:
        #                     yield [permutation]
        #                 else:
        #                     yield permutation

    @staticmethod
    def get_all_routes(locations, vehicle_start_locations):
        # sil = list(SolverBruteForce._get_partitions_that_contain_vehicles(locations, vehicle_start_locations))
        for parts in SolverBruteForce._get_partitions_that_contain_vehicles(locations, vehicle_start_locations):
            parts_permutations = []
            for part in parts:
                part_permutations = []
                for v_start in vehicle_start_locations:
                    if v_start in part:
                        part_without_v_start = [i for i in part if i != v_start]
                        # sil = list(itertools.permutations(part_without_v_start, len(part_without_v_start)))
                        permutations_without_vehicle = itertools.permutations(part_without_v_start, len(part_without_v_start))
                        part_permutations += [[v_start, *part1] for part1 in permutations_without_vehicle]
                parts_permutations.append(part_permutations)

            # # todo sil ###############
            # if len(parts_permutations) != 4:
            #     continue
            # sil = list(SolverBruteForce._combine_permutations(parts_permutations))
            for routes in SolverBruteForce._combine_permutations(parts_permutations):
                # print(routes)
                yield routes

            # for part in parts:
            #     res = []
            #     for v_start in vehicle_start_locations:
            #         if v_start in part:
            #             part_without_v_start = [i for i in part if i != v_start]
            #             # sil = list(itertools.permutations(part_without_v_start, len(part_without_v_start)))
            #             for part1 in itertools.permutations(part_without_v_start, len(part_without_v_start)):
            #                 res.append([v_start, *part1])
            #     yield res

    def solve(self):
        locations = list(range(len(self.matrix)))
        vehicle_start_locations = [vehicle["start_index"] for vehicle in self.vehicles]

        best_routes = None
        min_dist = sys.maxsize

        count = 0
        for routes in self.get_all_routes(locations, vehicle_start_locations):
            count += 1
            if self.verbose:
                print_same_line(f"{routes}  count: {count}")
            is_smaller, dist = routes_distance_is_smaller_than(routes, self.matrix, min_dist)
            if is_smaller:
                best_routes = routes
                assert calculate_all_routes_distance(routes, self.matrix) == dist  # sil
                min_dist = dist
                print(f"\rmin_dist: {min_dist} - {best_routes}")

        # sil
        print("\r*********** finished ***********")
        print(f"min_dist: {min_dist} - {best_routes}  count:{count}")
