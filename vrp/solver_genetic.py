import random
import sys
from array import array

from utils.generic_helpers import partition, print_same_line
from utils.solver_common import routes_cost_is_less_than, calculate_all_routes_costs, build_location_to_job_service_times, \
    build_location_to_delivery, build_location_to_job, calculate_route_cost, build_location_to_vehicle, route_costs_less_than, build_result, are_capacities_ok


class SolverGenetic:

    def __init__(self, vehicles, jobs, matrix, options):
        self.verbose = options["verbose"]
        self.limited_capacity = options["limited_capacity"]

        self.gen_iteration = options.get("gen_iteration", 1000)
        self.gen_k = options.get("gen_k", 50)
        self.gen_crossover = options.get("gen_crossover", 32)
        self.gen_mutation = options.get("gen_mutation", 14)
        self.gen_new = options.get("gen_new", 4)

        self.service_times = build_location_to_job_service_times(jobs) if options["include_service"] else None
        self.location_to_delivery = build_location_to_delivery(jobs)
        self.location_to_job = build_location_to_job(jobs)
        self.location_to_vehicle = build_location_to_vehicle(vehicles)

        self.matrix = matrix
        self.vehicle_locations = [vehicle["start_index"] for vehicle in vehicles]
        self.vehicle_ids = [vehicle["id"] for vehicle in vehicles]
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

    # @staticmethod
    # def _crossover(route1, route2):
    #     start = random.randint(0, len(route1) - 1)
    #     end = random.randint(start - 1, len(route2) - 1)
    #     try:
    #         end = random.randint(start + 1, len(route2) - 1)
    #     except:
    #         pass
    #     new_route = route1[start:end]
    #     for i in range(len(route2)):
    #         p = route2[i]
    #         if p not in new_route:
    #             new_route.append(p)
    #     return new_route

    # def _routes_can_crossover(self, routes1, routes2):
    #     if len(routes1) != len(routes2)

    @staticmethod
    def random_partition(list_in, n):
        # https://stackoverflow.com/a/51838144/1266873
        random.shuffle(list_in)
        return [list_in[i::n] for i in range(n)]

    def _generate_random_routes(self):
        # job partition ex: 3,4,5 - 6,7,8,9 | 3,4, - 5,6 - 7,8,9 | ...
        part_count = random.randint(1, len(self.vehicle_locations))
        vehicle_locations = self.vehicle_locations.copy()
        random.shuffle(vehicle_locations)
        vehicle_locations = vehicle_locations[:part_count]
        job_partitions = list(self.random_partition(self.job_locations, part_count))
        routes = []
        for i, part in enumerate(job_partitions):
            random.shuffle(part)
            routes.append([vehicle_locations[i], *part])
        return routes

    def solve(self):
        best_routes = None
        min_duration = sys.maxsize

        population = []
        for _ in range(self.gen_k):
            population.append(self._generate_random_routes())

        for generation in range(self.gen_iteration):
            len_population = len(population)
            new_members = []
            for _ in range(self.gen_crossover):
                index = random.randint(0, len_population)
                routes1 = population[index]
                routes2 = None
                # for i in range(len_population):
                #     if i != index and self._routes_can_crossover(routes1, population[i]):
                #         routes2 = population[i]
                #         break
                # if routes2 is None:
                #     continue
                #
                # new_members.append(self._generate_crossover(routes1, routes2))

            # for routes in population:
            #     if self.limited_capacity and not are_capacities_ok(self, routes):
            #         if self.verbose:
            #             print_same_line(f"Generation: {i} - {routes} - capacity nok!")
            #         continue
            #
            #     if self.verbose:
            #         print_same_line(f"Generation: {i} - {routes}")
            #
            #     is_smaller, dist = routes_cost_is_less_than(routes, self.matrix, min_duration, self.service_times)
            #     if is_smaller:
            #         best_routes = routes
            #         assert calculate_all_routes_costs(routes, self.matrix, self.service_times) == dist
            #         min_duration = dist
            #         if self.verbose:
            #             print(f"\rbest found: {min_duration} - {best_routes}")

        # if self.verbose:
        #     print_same_line(f"total duration: {min_duration} - {best_routes}")
        #     print("")

        return build_result(self, best_routes, min_duration)
