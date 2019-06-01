from haversine import haversine
import unittest


class GeoDistanceCalculator:
    def __init__(self):
        pass

    @staticmethod
    def get_distance(user_location, target_location, dist_type):
        if dist_type == "greatcircle":
            distance = int(haversine(user_location, target_location, unit = 'm'))
        else:
            return -1
        return distance


class TestGDC(unittest.TestCase):
    def test_calculator_type(self):
        self.assertEqual(GeoDistanceCalculator().get_distance((10, 10), (20, 20),""), -1)

    def test_calculator_distance(self):
        self.assertEqual(GeoDistanceCalculator().get_distance((10, 10), (20, 20), "greatcircle"), 1544759)

if __name__ == '__main__':
    unittest.main()