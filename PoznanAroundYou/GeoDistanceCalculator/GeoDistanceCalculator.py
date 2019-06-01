from haversine import haversine


class GeoDistanceCalculator:
    @staticmethod
    def get_distance(user_location, target_location, dist_type):
        distance = -1
        if dist_type == "greatcircle":
            distance = int(haversine(user_location, target_location, unit = 'm'))
        return distance
