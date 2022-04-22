import itertools
import sys

from helpers import partition, routes_cost_is_less_than, calculate_all_routes_costs, print_same_line, \
    build_location_to_delivery, build_location_to_job, calculate_route_cost, build_location_to_vehicle, route_costs_less_than, build_location_to_job_service_times


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
        self.vehicle_ids = [vehicle["id"] for vehicle in vehicles]
        self.job_locations = [job["location_index"] for job in jobs]
        self.vehicle_capacities = [vehicle["capacity"][0] for vehicle in vehicles]

    def _build_result_json(self, best_routes, min_duration):
        if best_routes is None:
            return None

        tu = []
        for route in best_routes:
            vehicle_id = self.location_to_vehicle[route[0]]["id"]
            tu.append((vehicle_id, route))
        dic = dict(tu)

        routes = {}
        for vehicle_id in self.vehicle_ids:
            jobs = []
            cost = 0
            if vehicle_id in dic:
                route = dic[vehicle_id]
                for location in route[1:]:
                    jobs.append(str(self.location_to_job[location]["id"]))
                cost = calculate_route_cost(route, self.matrix, self.service_times)
            routes[str(vehicle_id)] = {
                "jobs": jobs,
                "delivery_duration": cost
            }

        return {
            "total_delivery_duration": min_duration,
            "routes": routes
        }

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

    def _get_routes_worth_checking(self):
        # get all partition combinations for job locations. ex: 3,4 - 5,6,7,8,9 | 3,4, - 5,6 - 7,8,9 | ...
        for parts in partition(self.job_locations):
            # get all vehicle start location permutations that has the same count with the 'parts'
            # ex: for: [3,4 - 5,6,7,8,9] -> vehicles: 0,1 | 0,2 | 1,2 | 2,0 |...
            for vehicles in itertools.permutations(self.vehicle_locations, len(parts)):
                # get all permutations for each part. ex: 3,4 - 5,6,7,8,9 | 4,3 - 9,7,8,6 | ...
                best_routes = []
                for i, part in enumerate(parts):
                    # find all permutations of each part and calculate the minimum costing route
                    min_cost = sys.maxsize
                    best_route = None
                    for part_permutation in itertools.permutations(part, len(part)):
                        # add the vehicle start location, so that we have a proper route
                        route = [vehicles[i], *part_permutation]
                        is_less, cost = route_costs_less_than(route, self.matrix, min_cost, self.service_times)
                        if is_less:
                            min_cost = cost
                            best_route = route
                    best_routes.append(best_route)
                yield best_routes

    def solve(self):
        best_routes = None
        min_duration = sys.maxsize

        for routes in self._get_routes_worth_checking():
            if self.limited_capacity and not self._are_capacities_ok(routes):
                if self.verbose:
                    print_same_line(f"{routes} - capacity nok!")
                continue

            if self.verbose:
                print_same_line(f"{routes}")

            is_smaller, dist = routes_cost_is_less_than(routes, self.matrix, min_duration, self.service_times)
            if is_smaller:
                best_routes = routes
                assert calculate_all_routes_costs(routes, self.matrix, self.service_times) == dist
                min_duration = dist
                if self.verbose:
                    print(f"\rduration: {min_duration} - {best_routes}")

        if self.verbose:
            print_same_line(f"total duration: {min_duration} - {best_routes}")
            print("")

        return self._build_result_json(best_routes, min_duration)
