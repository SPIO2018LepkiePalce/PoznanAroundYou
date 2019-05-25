# from geopy.distance import great_circle
from haversine import haversine


class GeoDistanceCalculator:
    @staticmethod
    def get_distance(user_location, target_location, dist_type):
        distance = -1
        if dist_type == "greatcircle":
            # distance = int(great_circle(user_location, target_location).meters)
            distance = int(haversine(user_location, target_location, unit = 'm'))
            distance
        return distance
