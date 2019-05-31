from django.shortcuts import render
from django.http import HttpResponse
from haversine import haversine
import requests
import json
import os

class GeoDistanceCalculator:
    @staticmethod
    def get_distance(user_location, target_location, dist_type):
        distance = -1
        if dist_type == "greatcircle":
            # distance = int(great_circle(user_location, target_location).meters)
            distance = int(haversine(user_location, target_location, unit='m'))
        return distance


class TransportStopJSON:
    def __init__(self):
        self.bikejson = self.download_json_from_api()
        # with open("stops.txt") as stops_file:

    def get_json(self):
        return self.bikejson

    def download_json_from_api(self):
        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        r = requests.get(url)
        return r.json()


class TransportStop:
    def __init__(self, lat, lon, name, lines):
        self.lines = lines
        self.name = name
        self.lon = lon
        self.lat = lat
        self.distance_to = -1
        self.updated = 0

    def __str__(self):
        return "Współrzędne: {}, {}. Nazwa: {}, Linie: {}, Odległość: {} metrów, Ostatnia Aktualizacja {}"\
            .format(self.lon, self.lat, self.name, self.lines, self.distance_to, self.updated)

    def as_dict(self):
        transportstop_dict = dict()
        transportstop_dict['name'] = self.name
        transportstop_dict['free_bikes'] = self.lines
        transportstop_dict['lon'] = self.lon
        transportstop_dict['lat'] = self.lat
        transportstop_dict['distance_to'] = self.distance_to
        transportstop_dict['updated'] = self.updated
        return transportstop_dict


class TransportStops:
    def __init__(self):
        self.transportstops_data = []

        transportstopjson = TransportStopJSON()

        for transportstops in transportstopjson.get_json()['features']:
            lat = transportstops['geometry']['coordinates'][0]
            lon = transportstops['geometry']['coordinates'][1]
            name = transportstops['properties']['stop_name']
            lines = transportstops['properties']['headsigns'].replace(" ","").split(",")
            self.transportstops_data.append(TransportStop(lat, lon, name, lines))

def default(response):
    return HttpResponse("this is stops")

# Create your views here.

if __name__ == '__main__':
    ts = TransportStops()
    for t in ts.transportstops_data:
        print(t)
