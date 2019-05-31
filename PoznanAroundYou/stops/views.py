from django.shortcuts import render
from django.http import HttpResponse
from haversine import haversine
import requests
import json
import os
from datetime import datetime

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
        transportstop_dict['lines'] = self.lines
        transportstop_dict['lon'] = self.lon
        transportstop_dict['lat'] = self.lat
        transportstop_dict['distance_to'] = self.distance_to
        transportstop_dict['updated'] = self.updated
        return transportstop_dict


class TransportStops:
    def __init__(self):
        self.transportstops_data = []
        self.names = []

        transportstopjson = TransportStopJSON()

        for transportstops in transportstopjson.get_json()['features']:
            if transportstops['properties']['stop_name'] not in self.names:
                lat = transportstops['geometry']['coordinates'][0]
                lon = transportstops['geometry']['coordinates'][1]
                name = transportstops['properties']['stop_name']
                lines = transportstops['properties']['headsigns'].replace(" ","").split(",")
                self.transportstops_data.append(TransportStop(lat, lon, name, lines))
                self.names.append(transportstops['properties']['stop_name'])
            else:
                # super dirty method to find stops with the same name, and in such case, only append the line numbers
                for transportstops_data_search in self.transportstops_data:
                    if transportstops_data_search.name == transportstops['properties']['stop_name']:
                        transportstops_data_search.lines.extend(transportstops['properties']['headsigns'].replace(" ","").split(","))
                        transportstops_data_search.lines = list(set(transportstops_data_search.lines))
                        transportstops_data_search.lines.sort()

    def find_transport_stop_distances(self, user_location):
        for transport_stop in self.transportstops_data:
            target_location = (transport_stop.lat, transport_stop.lon)
            transport_stop.distance_to = GeoDistanceCalculator.get_distance(user_location, target_location, "greatcircle")
            transport_stop.updated = datetime.utcnow()

    def sort_transport_stops_by_distance(self):
        self.transportstops_data.sort(key=lambda x: x.distance_to)

    def get_transport_stops_data_as_dict(self, how_many=0):
        response = []
        for i in range(0, how_many):
            response.append(self.transportstops_data[i].as_dict())
        return {"response": response}

def default(request):
    ts = TransportStops()
    ts.find_transport_stop_distances((16.9086372,52.432585))
    ts.sort_transport_stops_by_distance()
    results = ts.get_transport_stops_data_as_dict(5)
    return render(request, 'stops/stops.html', {'results': results})

# Create your views here.

if __name__ == '__main__':
    ts = TransportStops()
    ts.find_transport_stop_distances((16.9086372,52.432585))
    ts.sort_transport_stops_by_distance()
    for t in ts.transportstops_data:
        print(t)
