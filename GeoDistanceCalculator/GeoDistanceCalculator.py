from geopy.distance import great_circle


class GeoDistanceCalculator:
    @staticmethod
    def get_distance(user_location, target_location, dist_type):
        distance = -1
        if dist_type == "greatcircle":
            distance = int(great_circle(user_location, target_location).meters)
        return distance
