import unittest

from vrp.utils.helpers import partition
from vrp.utils.solver_helpers import calculate_route_cost, routes_cost_is_less_than, calculate_all_routes_costs
from vrp.solver_bruteforce import SolverBruteForce


class TestVrp(unittest.TestCase):

    def test_partition(self):
        collection = list(range(1, 5))
        expected_value = [[[1, 2, 3, 4]],
                          [[1], [2, 3, 4]],
                          [[1, 2], [3, 4]],
                          [[2], [1, 3, 4]],
                          [[1], [2], [3, 4]],
                          [[1, 2, 3], [4]],
                          [[2, 3], [1, 4]],
                          [[1], [2, 3], [4]],
                          [[1, 3], [2, 4]],
                          [[3], [1, 2, 4]],
                          [[1], [3], [2, 4]],
                          [[1, 2], [3], [4]],
                          [[2], [1, 3], [4]],
                          [[2], [3], [1, 4]]]
        actual_value = list(partition(collection, 3))
        self.assertEqual(actual_value, expected_value, "partition failed!")

    def test_calculate_route_cost(self):
        route = [0, 3, 4, 5, 6, 7, 8, 9]
        matrix = [[0, 516, 226, 853, 1008, 1729, 346, 1353, 1554, 827], [548, 0, 474, 1292, 1442, 2170, 373, 1801, 1989, 1068], [428, 466, 0, 1103, 1175, 1998, 226, 1561, 1715, 947], [663, 1119, 753, 0, 350, 1063, 901, 681, 814, 1111], [906, 1395, 1003, 292, 0, 822, 1058, 479, 600, 1518], [1488, 1994, 1591, 905, 776, 0, 1746, 603, 405, 1676], [521, 357, 226, 1095, 1167, 1987, 0, 1552, 1705, 1051], [1092, 1590, 1191, 609, 485, 627, 1353, 0, 422, 1583], [1334, 1843, 1436, 734, 609, 396, 1562, 421, 0, 1745], [858, 1186, 864, 1042, 1229, 1879, 984, 1525, 1759, 0]]

        expected_value = 7490
        actual_value = calculate_route_cost(route, matrix, None)

        self.assertEqual(actual_value, expected_value, "calculate_route_cost failed!")

    def test_routes_cost_is_less_than(self):
        routes = [[0, 3], [1, 6], [2, 9, 4, 7, 8, 5]]
        matrix = [[0, 516, 226, 853, 1008, 1729, 346, 1353, 1554, 827], [548, 0, 474, 1292, 1442, 2170, 373, 1801, 1989, 1068], [428, 466, 0, 1103, 1175, 1998, 226, 1561, 1715, 947], [663, 1119, 753, 0, 350, 1063, 901, 681, 814, 1111], [906, 1395, 1003, 292, 0, 822, 1058, 479, 600, 1518], [1488, 1994, 1591, 905, 776, 0, 1746, 603, 405, 1676], [521, 357, 226, 1095, 1167, 1987, 0, 1552, 1705, 1051], [1092, 1590, 1191, 609, 485, 627, 1353, 0, 422, 1583], [1334, 1843, 1436, 734, 609, 396, 1562, 421, 0, 1745], [858, 1186, 864, 1042, 1229, 1879, 984, 1525, 1759, 0]]
        service_times = {3: 327, 4: 391, 5: 297, 6: 234, 7: 357, 8: 407, 9: 382}

        cost = 8000
        expected_value = True, 7094
        actual_value = routes_cost_is_less_than(routes, matrix, cost, service_times)
        self.assertEqual(actual_value, expected_value, "routes_cost_is_less_than failed!")

        cost = 555
        expected_value = False, None
        actual_value = routes_cost_is_less_than(routes, matrix, cost, service_times)
        self.assertEqual(actual_value, expected_value, "routes_cost_is_less_than failed!")

    def test_calculate_all_routes_costs(self):
        routes = [[0, 3, 6, 4], [1, 5, 7, 8], [2]]
        matrix = [[0, 516, 226, 853, 1008, 1729, 346, 1353, 1554, 827], [548, 0, 474, 1292, 1442, 2170, 373, 1801, 1989, 1068], [428, 466, 0, 1103, 1175, 1998, 226, 1561, 1715, 947], [663, 1119, 753, 0, 350, 1063, 901, 681, 814, 1111], [906, 1395, 1003, 292, 0, 822, 1058, 479, 600, 1518], [1488, 1994, 1591, 905, 776, 0, 1746, 603, 405, 1676], [521, 357, 226, 1095, 1167, 1987, 0, 1552, 1705, 1051], [1092, 1590, 1191, 609, 485, 627, 1353, 0, 422, 1583], [1334, 1843, 1436, 734, 609, 396, 1562, 421, 0, 1745], [858, 1186, 864, 1042, 1229, 1879, 984, 1525, 1759, 0]]
        service_times = {3: 327, 4: 391, 5: 297, 6: 234, 7: 357, 8: 407, 9: 382}

        expected_value = 8129
        actual_value = calculate_all_routes_costs(routes, matrix, service_times)
        self.assertEqual(actual_value, expected_value, "calculate_all_routes_costs failed!")

    def test_bruteforce(self):
        # default input
        vehicles = [{'id': 1, 'start_index': 0, 'capacity': [4]}, {'id': 2, 'start_index': 1, 'capacity': [6]}, {'id': 3, 'start_index': 2, 'capacity': [6]}]
        jobs = [{'id': 1, 'location_index': 3, 'delivery': [2], 'service': 327}, {'id': 2, 'location_index': 4, 'delivery': [1], 'service': 391}, {'id': 3, 'location_index': 5, 'delivery': [1], 'service': 297}, {'id': 4, 'location_index': 6, 'delivery': [2], 'service': 234}, {'id': 5, 'location_index': 7, 'delivery': [1], 'service': 357}, {'id': 6, 'location_index': 8, 'delivery': [1], 'service': 407}, {'id': 7, 'location_index': 9, 'delivery': [1], 'service': 382}]
        matrix = [[0, 516, 226, 853, 1008, 1729, 346, 1353, 1554, 827], [548, 0, 474, 1292, 1442, 2170, 373, 1801, 1989, 1068], [428, 466, 0, 1103, 1175, 1998, 226, 1561, 1715, 947], [663, 1119, 753, 0, 350, 1063, 901, 681, 814, 1111], [906, 1395, 1003, 292, 0, 822, 1058, 479, 600, 1518], [1488, 1994, 1591, 905, 776, 0, 1746, 603, 405, 1676], [521, 357, 226, 1095, 1167, 1987, 0, 1552, 1705, 1051], [1092, 1590, 1191, 609, 485, 627, 1353, 0, 422, 1583], [1334, 1843, 1436, 734, 609, 396, 1562, 421, 0, 1745], [858, 1186, 864, 1042, 1229, 1879, 984, 1525, 1759, 0]]
        options = {'verbose': False, 'limited_capacity': True, 'include_service': True}
        solver = SolverBruteForce(vehicles, jobs, matrix, options)

        expected_value = {'total_delivery_duration': 6345, 'routes': {'1': {'jobs': ['7'], 'delivery_duration': 1209}, '2': {'jobs': ['4'], 'delivery_duration': 607}, '3': {'jobs': ['1', '2', '5', '6', '3'], 'delivery_duration': 4529}}}
        actual_value = solver.solve()
        self.assertEqual(actual_value, expected_value, "bruteforce failed with default input!")

        # single vehicle
        vehicles = [{'id': 1, 'start_index': 0, 'capacity': [4]}]
        jobs = [{'id': 1, 'location_index': 3, 'delivery': [2], 'service': 327}, {'id': 2, 'location_index': 4, 'delivery': [1], 'service': 391}, {'id': 3, 'location_index': 5, 'delivery': [1], 'service': 297}, {'id': 4, 'location_index': 6, 'delivery': [2], 'service': 234}, {'id': 5, 'location_index': 7, 'delivery': [1], 'service': 357}, {'id': 6, 'location_index': 8, 'delivery': [1], 'service': 407}, {'id': 7, 'location_index': 9, 'delivery': [1], 'service': 382}]
        matrix = [[0, 516, 226, 853, 1008, 1729, 346, 1353, 1554, 827], [548, 0, 474, 1292, 1442, 2170, 373, 1801, 1989, 1068], [428, 466, 0, 1103, 1175, 1998, 226, 1561, 1715, 947], [663, 1119, 753, 0, 350, 1063, 901, 681, 814, 1111], [906, 1395, 1003, 292, 0, 822, 1058, 479, 600, 1518], [1488, 1994, 1591, 905, 776, 0, 1746, 603, 405, 1676], [521, 357, 226, 1095, 1167, 1987, 0, 1552, 1705, 1051], [1092, 1590, 1191, 609, 485, 627, 1353, 0, 422, 1583], [1334, 1843, 1436, 734, 609, 396, 1562, 421, 0, 1745], [858, 1186, 864, 1042, 1229, 1879, 984, 1525, 1759, 0]]
        options = {'verbose': False, 'limited_capacity': False, 'include_service': False}
        solver = SolverBruteForce(vehicles, jobs, matrix, options)

        expected_value = {'total_delivery_duration': 4086, 'routes': {'1': {'jobs': ['4', '7', '1', '2', '5', '6', '3'], 'delivery_duration': 6481}}}
        actual_value = solver.solve()
        self.assertEqual(actual_value, expected_value, "bruteforce failed with single vehicle input!")


if __name__ == '__main__':
    unittest.main()
