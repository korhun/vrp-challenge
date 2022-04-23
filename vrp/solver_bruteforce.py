import itertools
import sys

from utils.generic_helpers import partition, print_same_line
from utils.solver_common import routes_cost_is_less_than, calculate_all_routes_costs, build_location_to_job_service_times, \
    build_location_to_delivery, build_location_to_job, calculate_route_cost, build_location_to_vehicle, route_costs_less_than, build_result, are_capacities_ok


class SolverBruteForce:

    def __init__(self, vehicles, jobs, matrix, options):
        self.verbose = options["verbose"]
        self.limited_capacity = options["limited_capacity"]

        self.service_times = build_location_to_job_service_times(jobs) if options["include_service"] else None
        self.location_to_delivery = build_location_to_delivery(jobs)
        self.location_to_job = build_location_to_job(jobs)
        self.location_to_vehicle = build_location_to_vehicle(vehicles)

        self.matrix = matrix
        self.vehicle_locations = [vehicle["start_index"] for vehicle in vehicles]
        self.vehicles_count = len(self.vehicle_locations)
        self.vehicle_ids = [vehicle["id"] for vehicle in vehicles]
        self.job_locations = [job["location_index"] for job in jobs]
        self.jobs_count = len(self.job_locations)
        self.vehicle_capacities = [vehicle["capacity"][0] for vehicle in vehicles]

    def _get_all_routes(self):
        # get permutations for job locations. ex: 3,4,5,6,7,8,9 | 4,3,5,6,7,8,9 | ...
        for job_locations in itertools.permutations(self.job_locations, self.jobs_count):
            # get all partition combinations for the job locations. ex: 3,4,5 - 6,7,8,9 | 3,4, - 5,6 - 7,8,9 | ...
            for parts in partition(list(job_locations), self.vehicles_count):
                # get all vehicle start location permutations that has the same count with the 'parts'
                # ex: the parts: [3,4,5 - 6,7,8,9] has 2 pieces, so -> vehicles: 0,1 | 0,2 | 1,2 | 2,0 |...
                for vehicles in itertools.permutations(self.vehicle_locations, len(parts)):
                    routes = []
                    for i, part in enumerate(parts):
                        # insert vehicle start location so that we have a proper route
                        route = [vehicles[i], *part]
                        routes.append(route)
                    yield routes

    def solve(self):
        best_routes = None
        min_duration = sys.maxsize

        count = 0
        for routes in self._get_all_routes():
            count += 1
            if self.limited_capacity and not are_capacities_ok(self, routes):
                if self.verbose:
                    print_same_line(f"{count:,} - {routes} - capacity nok!")
                continue

            if self.verbose:
                print_same_line(f"{count:,} - {routes}")

            is_smaller, dist = routes_cost_is_less_than(routes, self.matrix, min_duration, self.service_times)
            if is_smaller:
                best_routes = routes
                assert calculate_all_routes_costs(routes, self.matrix, self.service_times) == dist
                min_duration = dist
                if self.verbose:
                    print(f"\rbest: {min_duration} - {best_routes} - at iteration: - {count:,}")

        if self.verbose:
            print_same_line(f"final: {min_duration} - {best_routes} - total iterations: {count:,}")
            print("")

        return build_result(self, best_routes, min_duration)
