import json
from datetime import datetime
from GeoDistanceCalculator import GeoDistanceCalculator


class BikeRackJSON:
    def __init__(self):
        self.bikejson = ""
        with open("bikes.txt", "r", encoding="utf-8") as bikefile:
            self.bikejson = json.load(bikefile)

    def get_json(self):
        return self.bikejson


class BikeRack:
    def __init__(self, lat, lon, name, free_bikes):
        self.free_bikes = free_bikes
        self.name = name
        self.lon = lon
        self.lat = lat
        self.distance_to = -1
        self.updated = 0

    def __str__(self):
        return "place: {}, {}. name: {}, free bikes: {}, distance: {}, last updated {}"\
            .format(self.lon, self.lat, self.name, self.free_bikes, self.distance_to, self.updated)

    def as_dict(self):
        bikerack_dict = dict()
        bikerack_dict['name'] = self.name
        bikerack_dict['free_bikes'] = self.free_bikes
        bikerack_dict['lon'] = self.lon
        bikerack_dict['lat'] = self.lat
        bikerack_dict['distance_to'] = self.distance_to
        bikerack_dict['updated'] = self.updated
        return bikerack_dict


class BikeRacks:
    def __init__(self):
        self.bikeracks_data = []

        bikerackjson = BikeRackJSON()

        for bikeracks in bikerackjson.get_json()['features']:
            lat = bikeracks['geometry']['coordinates'][0]
            lon = bikeracks['geometry']['coordinates'][1]
            name = bikeracks['properties']['label']
            free_bikes = bikeracks['properties']['bikes']
            self.bikeracks_data.append(BikeRack(lat, lon, name, free_bikes))

    def print_racks_data(self, how_many=0):
        for bkr in self.bikeracks_data[0:how_many]:
            print(bkr)

    def print_racks_dict(self, how_many=0):
        for bkr in self.bikeracks_data[0:how_many]:
            print(bkr.as_dict())

    def get_racks_data_as_str(self, how_many=0):
        response = ""
        for bkr in self.bikeracks_data[0:how_many]:
            response += str(bkr)
            response += "<br/>"
        return str(response)

    def get_racks_data_as_list(self, how_many=0):
        return self.bikeracks_data[0:how_many]

    def get_single_rack_data(self, which=0):
        return self.bikeracks_data[which]

    def find_bikerack_distances(self, user_location):
        for bikerack in self.bikeracks_data:
            target_location = (bikerack.lat, bikerack.lon)
            bikerack.distance_to = GeoDistanceCalculator.GeoDistanceCalculator.get_distance(user_location, target_location, "greatcircle")
            bikerack.updated = datetime.utcnow()

    def sort_bikeracks_by_distance(self):
        self.bikeracks_data.sort(key=lambda x: x.distance_to)


if __name__ == '__main__':
    brj = BikeRackJSON()
    # print(brj.get_json())
    br = BikeRacks()
    print(br.bikeracks_data[0])
    print(br.get_single_rack_data(0))
    print(br.get_racks_data_as_str(10))

