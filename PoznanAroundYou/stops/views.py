from django.shortcuts import render, redirect
from datetime import datetime
from GeoDistanceCalculator.GeoDistanceCalculator import GeoDistanceCalculator
from ServiceAPIJSON.ServiceAPIJSON import ServiceAPIJSON


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

        transportstopjson = ServiceAPIJSON("STOPS")

        for transportstops in transportstopjson.get_json()['features']:
            if transportstops['properties']['stop_name'] not in self.names:
                lat = transportstops['geometry']['coordinates'][0]
                lon = transportstops['geometry']['coordinates'][1]
                name = transportstops['properties']['stop_name']
                # 'headsigns' in the api is a string of line numbers, separated by comma and space
                lines = transportstops['properties']['headsigns'].replace(" ","").split(",")
                self.transportstops_data.append(TransportStop(lat, lon, name, lines))
                self.names.append(transportstops['properties']['stop_name'])
            else:
                #  Find stops with the same name, and in such case, only append the line numbers
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
    response = redirect('/ticketmachines/0/0')
    return response


def index(request, lat, lon):
    my_loc = (float(lon), float(lat))
    ts = TransportStops()
    ts.find_transport_stop_distances(my_loc)
    ts.sort_transport_stops_by_distance()
    if lat == "0" and lon == "0":
        results = ts.get_transport_stops_data_as_dict(0)
    else:
        results = ts.get_transport_stops_data_as_dict(5)
    return render(request, 'ticketmachines/ticketmachines.html', {'results': results})

