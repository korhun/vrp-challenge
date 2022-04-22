import unittest

from vrp.helpers import calculate_route_cost, partition, routes_cost_is_less_than


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
                          [[2], [3], [1, 4]],
                          [[1], [2], [3], [4]]]
        actual_value = list(partition(collection))
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


if __name__ == '__main__':
    unittest.main()
