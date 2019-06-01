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


class TicketMachineJSON:
    def __init__(self):
        self.ticketmachinejson = self.download_json_from_api()
        # with open("stops.txt") as stops_file:

    def get_json(self):
        return self.ticketmachinejson

    def download_json_from_api(self):
        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=class_objects&class_id=4000"
        r = requests.get(url)
        return r.json()


class TicketMachine:
    def __init__(self, lat, lon, name, desc):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.desc = desc
        self.distance_to = -1
        self.updated = 0

    def __str__(self):
        return "Współrzędne: {}, {}. Nazwa: {}, Opis: {}, Odległość: {} metrów, Ostatnia Aktualizacja {}"\
            .format(self.lon, self.lat, self.name, self.desc, self.distance_to, self.updated)

    def as_dict(self):
        ticketmachine_dict = dict()
        ticketmachine_dict['name'] = self.name
        ticketmachine_dict['desc'] = self.desc
        ticketmachine_dict['lon'] = self.lon
        ticketmachine_dict['lat'] = self.lat
        ticketmachine_dict['distance_to'] = self.distance_to
        ticketmachine_dict['updated'] = self.updated
        return ticketmachine_dict


class TicketMachines:
    def __init__(self):
        self.ticketmachines_data = []
        self.names = []

        ticketmachinesjson = TicketMachineJSON()

        for ticketmachines in ticketmachinesjson.get_json()['features']:
            lat = ticketmachines['geometry']['coordinates'][0]
            lon = ticketmachines['geometry']['coordinates'][1]
            name = ticketmachines['properties']['nazwa']
            desc = ticketmachines['properties']['opis']
            self.ticketmachines_data.append(TicketMachine(lat, lon, name, desc))

    def find_ticket_machines_distances(self, user_location):
        for transport_stop in self.ticketmachines_data:
            target_location = (transport_stop.lat, transport_stop.lon)
            transport_stop.distance_to = GeoDistanceCalculator.get_distance(user_location, target_location, "greatcircle")
            transport_stop.updated = datetime.utcnow()

    def sort_ticket_machines_by_distance(self):
        self.ticketmachines_data.sort(key=lambda x: x.distance_to)

    def get_ticket_machines_data_as_dict(self, how_many=0):
        response = []
        for i in range(0, how_many):
            response.append(self.ticketmachines_data[i].as_dict())
        return {"response": response}

def default(request):
    ts = TicketMachines()
    ts.find_ticket_machines_distances((16.9086372, 52.432585))
    ts.sort_ticket_machines_by_distance()
    results = ts.get_ticket_machines_data_as_dict(5)
    return render(request, 'ticketmachines/ticketmachines.html', {'results': results})

# Create your views here.

if __name__ == '__main__':
    ts = TicketMachines()
    ts.find_ticket_machines_distances((16.9086372, 52.432585))
    ts.sort_ticket_machines_by_distance()
    for t in ts.ticketmachines_data:
        print(t)
