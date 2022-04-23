import itertools
import sys

from utils.generic_helpers import partition, print_same_line
from utils.solver_common import routes_cost_is_less_than, calculate_all_routes_costs, build_location_to_job_service_times, \
    build_location_to_delivery, build_location_to_job, calculate_route_cost, build_location_to_vehicle, route_costs_less_than, build_result, are_capacities_ok


class SolverGenetic:

    def __init__(self, vehicles, jobs, matrix, options):
        self.verbose = options["verbose"]
        self.limited_capacity = options["limited_capacity"]

        self.population_size = options.get("population_size", 50)

        self.service_times = build_location_to_job_service_times(jobs) if options["include_service"] else None
        self.location_to_delivery = build_location_to_delivery(jobs)
        self.location_to_job = build_location_to_job(jobs)
        self.location_to_vehicle = build_location_to_vehicle(vehicles)

        self.matrix = matrix
        self.vehicle_locations = [vehicle["start_index"] for vehicle in vehicles]
        self.vehicle_ids = [vehicle["id"] for vehicle in vehicles]
        self.vehicles_count = len(vehicles)
        self.job_locations = [job["location_index"] for job in jobs]
        self.vehicle_capacities = [vehicle["capacity"][0] for vehicle in vehicles]

    # def _find_the_best_routes_in_permutations_of_the_parts(self, vehicles, parts):
    #     # get all permutations for each part. ex: 3,4 - 5,6,7,8,9 | 4,3 - 9,7,8,6 | ...
    #     # and fill the best_routes list with the pieces having the minimum cost
    #     best_routes = []
    #     for i, part in enumerate(parts):
    #         min_cost = sys.maxsize
    #         best_route = None
    #         for part_permutation in itertools.permutations(part, len(part)):
    #             # add the vehicle start location, so that we have a proper route
    #             route = [vehicles[i], *part_permutation]
    #             is_less, cost = route_costs_less_than(route, self.matrix, min_cost, self.service_times)
    #             if is_less:
    #                 min_cost = cost
    #                 best_route = route
    #         best_routes.append(best_route)
    #     return best_routes
    #
    # def _get_routes_worth_checking(self):
    #     # get all partition combinations for job locations. ex: 3,4,5 - 6,7,8,9 | 3,4, - 5,6 - 7,8,9 | ...
    #     for parts in partition(self.job_locations):
    #         # get all vehicle start location permutations that has the same count with the 'parts'
    #         # ex: the parts: [3,4,5 - 6,7,8,9] has 2 pieces, so -> vehicles: 0,1 | 0,2 | 1,2 | 2,0 |...
    #         for vehicles in itertools.permutations(self.vehicle_locations, len(parts)):
    #             yield self._find_the_best_routes_in_permutations_of_the_parts(vehicles, parts)



    def _partition_random(collection, max_parts_count):
        def _partition(collection):
            # https://stackoverflow.com/a/30134039/1266873
            if len(collection) == 1:
                yield [collection]
                return

            first = collection[0]
            for smaller in _partition(collection[1:]):
                # insert `first` in each of the subpartition's subsets
                for n, subset in enumerate(smaller):
                    yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
                # put `first` in its own subset
                yield [[first]] + smaller

        for parts in _partition(collection):
            if len(parts) <= max_parts_count:
                yield parts

    def _generate_genomes(self):
        # get all partition combinations for job locations. ex: 3,4,5 - 6,7,8,9 | 3,4, - 5,6 - 7,8,9 | ...
        job_parts = list(partition(self.job_locations, self.vehicles_count))
        print("aaa")

    def solve(self):
        best_routes = None
        min_duration = sys.maxsize

        self._generate_genomes()

        # for routes in self._get_routes_worth_checking():
        #     if self.limited_capacity and not are_capacities_ok(self, routes):
        #         if self.verbose:
        #             print_same_line(f"{routes} - capacity nok!")
        #         continue
        #
        #     if self.verbose:
        #         print_same_line(f"{routes}")
        #
        #     is_smaller, dist = routes_cost_is_less_than(routes, self.matrix, min_duration, self.service_times)
        #     if is_smaller:
        #         best_routes = routes
        #         assert calculate_all_routes_costs(routes, self.matrix, self.service_times) == dist
        #         min_duration = dist
        #         if self.verbose:
        #             print(f"\rduration: {min_duration} - {best_routes}")

        if self.verbose:
            print_same_line(f"total duration: {min_duration} - {best_routes}")
            print("")

        return build_result(self, best_routes, min_duration)
