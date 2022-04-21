import itertools
import sys

from helpers import partition, routes_cost_is_smaller_than, calculate_all_routes_costs, print_same_line, \
    build_location_to_delivery, build_location_to_job, route_cost_is_more_than


class SolverBruteForce:

    def __init__(self, vehicles, jobs, matrix, options):
        self.verbose = options["verbose"]
        self.limited_capacity = options["limited_capacity"]

        self.location_to_delivery = build_location_to_delivery(jobs)
        self.location_to_job = build_location_to_job(jobs)

        self.matrix = matrix
        self.vehicle_locations = [vehicle["start_index"] for vehicle in vehicles]
        self.job_locations = [job["location_index"] for job in jobs]
        self.vehicle_capacities = [vehicle["capacity"][0] for vehicle in vehicles]

    def _are_capacities_ok(self, routes):
        for route in routes:
            vehicle_id = route[0]
            capacity = self.vehicle_capacities[vehicle_id]

            product_required = 0
            for location in route[1:]:
                product_required += self.location_to_delivery[location]
                if product_required > capacity:
                    return False
        return True

    @staticmethod
    def _combine_permutations(parts_permutations):
        if not parts_permutations:
            return

        def get_sub_parts(prev_parts, current_index):
            if current_index == len(parts_permutations):
                yield prev_parts
                return
            for i in [current_index]:
                if i >= len(parts_permutations):
                    break
                parts_current = parts_permutations[i]
                for part in parts_current:
                    prev_parts1 = [*prev_parts, part]
                    for sub_part in get_sub_parts(prev_parts1, current_index + 1):
                        yield sub_part

        parts0 = parts_permutations[0]
        for part0 in parts0:
            for routes in get_sub_parts([part0], 1):
                yield routes

    def _get_route_partitions(self):
        for parts in partition(self.job_locations):
            for vehicles in itertools.permutations(self.vehicle_locations, len(parts)):
                parts1 = list(parts)
                for i, vehicle in enumerate(vehicles):
                    parts1[i] = [vehicle, *parts1[i]]
                yield parts1

    def _get_all_routes(self):
        for parts in self._get_route_partitions():
            parts_permutations = []
            for part in parts:
                part_permutations = []
                part_without_v_start = part[1:]
                v_start = part[0]
                permutations_without_vehicle = itertools.permutations(part_without_v_start, len(part_without_v_start))
                part_permutations += [[v_start, *part1] for part1 in permutations_without_vehicle]
                parts_permutations.append(part_permutations)
            for routes in SolverBruteForce._combine_permutations(parts_permutations):
                yield routes

    def solve(self):
        best_routes = None
        min_dist = sys.maxsize

        count = 0
        for routes in self._get_all_routes():
            count += 1

            if self.limited_capacity and not self._are_capacities_ok(routes):
                if self.verbose:
                    print_same_line(f"{routes} count: {count:,} - capacity nok!")
                continue

            if self.verbose:
                print_same_line(f"{routes} count: {count:,}")

            is_smaller, dist = routes_cost_is_smaller_than(routes, self.matrix, min_dist)
            if is_smaller:
                best_routes = routes
                assert calculate_all_routes_costs(routes, self.matrix) == dist
                min_dist = dist
                print(f"\rmin_dist: {min_dist} - {best_routes}")

        print_same_line("*********** finished ***********")
        print(f"\nmin_dist: {min_dist} - {best_routes}  count:{count:,}")
