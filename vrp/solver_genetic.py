import random
import statistics
import sys

import numpy as np

from utils.generic_helpers import partition, print_same_line, all_equal
from utils.solver_common import routes_cost_is_less_than, calculate_all_routes_costs, build_location_to_job_service_times, \
    build_location_to_delivery, build_location_to_job, calculate_route_cost, build_location_to_vehicle, route_costs_less_than, build_result, are_capacities_ok


class SolverGenetic:

    def __init__(self, vehicles, jobs, matrix, options):
        self.verbose = options["verbose"]
        self.limited_capacity = options["limited_capacity"]
        self.include_service = options["include_service"]

        self.gen_iteration = options.get("gen_iteration", 1000000)

        # self.gen_k = options.get("gen_k", 50)
        # self.gen_crossover = options.get("gen_crossover", 32)
        # self.gen_mutation = options.get("gen_mutation", 14)
        # self.gen_new = options.get("gen_new", 4)

        self.gen_k = options.get("gen_k", 500)
        self.gen_crossover = options.get("gen_crossover", 320)
        self.gen_mutation = options.get("gen_mutation", 140)
        self.gen_new = options.get("gen_new", 40)

        # self.gen_k = options.get("gen_k", 5000)
        # self.gen_crossover = options.get("gen_crossover", 3200)
        # self.gen_mutation = options.get("gen_mutation", 1400)
        # self.gen_new = options.get("gen_new", 400)

        self.service_times = build_location_to_job_service_times(jobs)
        self.location_to_delivery = build_location_to_delivery(jobs)
        self.location_to_job = build_location_to_job(jobs)
        self.location_to_vehicle = build_location_to_vehicle(vehicles)

        self.matrix = matrix
        self.vehicle_locations = [vehicle["start_index"] for vehicle in vehicles]
        self.vehicle_ids = [vehicle["id"] for vehicle in vehicles]
        self.job_locations = [job["location_index"] for job in jobs]
        self.vehicle_capacities = [vehicle["capacity"][0] for vehicle in vehicles]

    def _generate_mutation(self, routes):
        def mutate(parent, mutate_count):
            start_index = random.randint(0, len(parent) - 1 - mutate_count)
            end_index = start_index + mutate_count
            piece = parent[start_index:end_index]
            random.shuffle(piece)
            res = parent.copy()
            res[start_index:end_index] = piece
            return res

        r = list(np.concatenate(routes))

        offspring = mutate(r, 3)
        # offspring = mutate(r, 5)
        if offspring[0] not in self.vehicle_locations:
            for i, val in enumerate(offspring):
                if val in self.vehicle_locations:
                    offspring[i] = offspring[0]
                    offspring[0] = val
                    break
        new_routes = []
        route = []
        for location in offspring:
            if location in self.vehicle_locations:
                if len(route) > 1:
                    new_routes.append(route)
                route = []
            route.append(location)
        if len(route) > 1:
            new_routes.append(route)
        return new_routes

    def _generate_crossover(self, routes1, routes2):
        # routes1 ex: [[2, 9, 8, 7], [1, 4, 6], [0, 5, 3]]
        # routes2 ex: [[2, 6, 9, 8, 4], [1, 3, 7, 5]]
        def crossover(parent1, parent2, cross_count):
            """
            example
            parent1: 1,3,4,2,5,7,6
            parent2: 1,7,5,2,3,4,6
            cross_count: 3
            cross_genes = 3,4,6 (from parent2)
            offspring_start = 1,2,5,7 (parent1 genes cross_genes excluded)
            return = offspring_start + randomized cross_genes
            """
            cross_genes = parent2[-cross_count:]

            # cross_genes alternative
            # start = random.randint(0, len(parent2) - 2)
            # end = random.randint(start + 1, len(parent2) - 1)
            # cross_genes = parent2[start: end]

            offspring_start = [gen for gen in parent1 if gen not in cross_genes]
            random.shuffle(cross_genes)
            return offspring_start + cross_genes

        r1 = list(np.concatenate(routes1))
        r2 = list(np.concatenate(routes2))

        offspring = crossover(r1, r2, 3)
        # offspring = crossover(r1, r2, 5)
        if offspring[0] not in self.vehicle_locations:
            for i, val in enumerate(offspring):
                if val in self.vehicle_locations:
                    offspring[i] = offspring[0]
                    offspring[0] = val
                    break
        new_routes = []
        route = []
        for location in offspring:
            if location in self.vehicle_locations:
                if len(route) > 1:
                    new_routes.append(route)
                route = []
            route.append(location)
        if len(route) > 1:
            new_routes.append(route)
        return new_routes

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
        min_cost = sys.maxsize
        service_times = self.service_times if self.include_service else None

        population = [self._generate_random_routes() for _ in range(self.gen_k)]

        generation = 0
        for generation in range(self.gen_iteration):
            len_population = len(population)
            len_population_1 = len_population - 1

            crossover_parents = [(random.randint(0, len_population_1), random.randint(0, len_population_1)) for _ in range(self.gen_crossover)]
            crossover_offsprings = [self._generate_crossover(population[i1], population[i2]) for i1, i2 in crossover_parents]

            mutation_parents = [random.randint(0, len_population_1) for _ in range(self.gen_mutation)]
            mutation_offsprings = [self._generate_mutation(population[i]) for i in mutation_parents]

            new_randoms = [self._generate_random_routes() for _ in range(self.gen_new)]

            population += crossover_offsprings + mutation_offsprings + new_randoms
            population.sort(key=lambda x: calculate_all_routes_costs(x, self.matrix, service_times))
            population = population[:self.gen_k]

            gen_all_costs = [calculate_all_routes_costs(x, self.matrix, service_times) for x in population]
            gen_average_cost = statistics.mean(gen_all_costs)
            gen_best_routes = population[0]
            gen_best_cost = calculate_all_routes_costs(gen_best_routes, self.matrix, service_times)

            if self.verbose:
                print_same_line(f"generation: {generation:,} - average: {gen_average_cost:.0f}")

            if min_cost > gen_best_cost:
                min_cost = gen_best_cost
                best_routes = gen_best_routes
                if self.verbose:
                    print(f"\rbest: {min_cost} - {best_routes} - at generation: - {generation:,}")

            if all_equal(gen_all_costs):
                break

        if self.limited_capacity and not are_capacities_ok(self, best_routes):
            print_same_line(f"final: {min_cost} - {best_routes} - total generations: {generation:,} - capacity not ok!")
            print("")
            return None

        if self.verbose:
            print_same_line(f"final: {min_cost} - {best_routes} - total generations: {generation:,}")
            print("")

        return build_result(self, best_routes, min_cost)
