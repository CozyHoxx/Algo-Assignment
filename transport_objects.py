# This file is just a class file to store each transportation routes
# Transportation types are now referred through enums

# EDIT: NEVERMIND, IM TOSSING THIS PART OUT.
from enum import Enum

class Transport(Enum):
        NULL = -1
        BUS = 1
        TRAIN = 2
        AIRPLANE = 3
        WALK = 4


class TransportObject:

    def __init__(self, name, type, stops):
        self.name = name
        self.type = type
        self.stops = [stops]  # This is a list. Every item is a list with contents [stop_name, lat, long]
        self.firstStation = self.stops[0]  # Track first station
        self.lastStation = self.stops[0]  # Track second station

    def add_stops(self, stop_name, latitude, longitude):
        self.stops.append([stop_name, latitude, longitude])
        self.lastStation = self.stops[len(self.stops) - 1] # Update last station

    # Returns a portion of the route
    def get_segment(self, start_index, end_index):
        return self.stops[start_index:end_index]


class JourneyPoint:

    def __init__(self, lat, lon, type):
        self.type = type
        self.lat = lat
        self.lon = lon
