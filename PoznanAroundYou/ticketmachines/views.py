from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import re
from GeoDistanceCalculator.GeoDistanceCalculator import GeoDistanceCalculator
from ServiceAPIJSON.ServiceAPIJSON import ServiceAPIJSON

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


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
        ticketmachine_dict['desc'] = remove_html_tags(self.desc)
        ticketmachine_dict['lon'] = self.lon
        ticketmachine_dict['lat'] = self.lat
        ticketmachine_dict['distance_to'] = self.distance_to
        ticketmachine_dict['updated'] = self.updated
        return ticketmachine_dict


class TicketMachines:
    def __init__(self):
        self.ticketmachines_data = []
        self.names = []

        ticketmachinesjson = ServiceAPIJSON("TICKETMACHINES")

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
    response = redirect('/ticketmachines/0/0')
    return response


def index(request, lat, lon):
    tm = TicketMachines()
    my_loc = (float(lon), float(lat))
    tm.find_ticket_machines_distances(my_loc)
    tm.sort_ticket_machines_by_distance()
    if lat == "0" and lon == "0":
        results = tm.get_ticket_machines_data_as_dict(0)
    else:
        results = tm.get_ticket_machines_data_as_dict(5)
    return render(request, 'ticketmachines/ticketmachines.html', {'results': results})

