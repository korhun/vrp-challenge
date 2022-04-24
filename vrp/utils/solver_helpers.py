import sys

# https://stackoverflow.com/a/38637774/1266873
gettrace = getattr(sys, 'gettrace', None)
if gettrace():
    print('debug mode')
    __debugging = True
else:
    __debugging = False


def calculate_route_cost(route, matrix, service_times):
    total = 0
    pre_index = route[0]
    for i in range(1, len(route)):
        index = route[i]
        total += matrix[pre_index][index]
        if service_times is not None:
            total += service_times[index]
        pre_index = index
    return total


def calculate_all_routes_costs(routes, matrix, service_times):
    return sum([calculate_route_cost(route, matrix, service_times) for route in routes])


def routes_cost_is_less_than(routes, matrix, cost, service_times):
    total = 0
    for route in routes:
        pre_index = route[0]
        for i in range(1, len(route)):
            index = route[i]
            total += matrix[pre_index][index]
            if service_times is not None:
                total += service_times[index]
            if total >= cost:
                return False, None
            pre_index = index
    return True, total


def route_costs_less_than(route, matrix, cost, service_times):
    """
    :return: (False, None) if route costs less than 'cost' else (True, cost value of the route)
    """
    total = 0
    pre_index = route[0]
    for i in range(1, len(route)):
        index = route[i]
        total += matrix[pre_index][index]
        if service_times is not None:
            total += service_times[index]
        if total > cost:
            return False, None
        pre_index = index
    return True, total


def build_location_to_delivery(jobs):
    return dict([(job["location_index"], job["delivery"][0]) for job in jobs])


def build_location_to_job(jobs):
    return dict([(job["location_index"], job) for job in jobs])


def build_location_to_job_service_times(jobs):
    return dict([(job["location_index"], job["service"]) for job in jobs])


def build_location_to_vehicle(vehicles):
    return dict([(vehicle["start_index"], vehicle) for vehicle in vehicles])


def are_capacities_ok(solver, routes):
    if __debugging:
        assert getattr(solver, "vehicle_capacities", None) is not None
        assert getattr(solver, "location_to_delivery", None) is not None

    for route in routes:
        vehicle_id = route[0]
        capacity = solver.vehicle_capacities[vehicle_id]

        product_required = 0
        for location in route[1:]:
            product_required += solver.location_to_delivery[location]
            if product_required > capacity:
                return False
    return True


def build_result(solver, best_routes, min_duration):
    if __debugging:
        assert getattr(solver, "location_to_vehicle", None) is not None
        assert getattr(solver, "vehicle_ids", None) is not None
        assert getattr(solver, "location_to_job", None) is not None
        assert getattr(solver, "matrix", None) is not None
        assert getattr(solver, "service_times", None) is not None

    if best_routes is None:
        return None

    tu = []
    for route in best_routes:
        vehicle_id = solver.location_to_vehicle[route[0]]["id"]
        tu.append((vehicle_id, route))
    dic = dict(tu)

    routes = {}
    for vehicle_id in solver.vehicle_ids:
        jobs = []
        cost = 0
        if vehicle_id in dic:
            route = dic[vehicle_id]
            for location in route[1:]:
                jobs.append(str(solver.location_to_job[location]["id"]))
            cost = calculate_route_cost(route, solver.matrix, solver.service_times)
        routes[str(vehicle_id)] = {
            "jobs": jobs,
            "delivery_duration": cost
        }

    return {
        "total_delivery_duration": min_duration,
        "routes": routes
    }
