# This file is just a class file to store each transportation routes
# Split according to bus, train (tba), plane(tba), and maybe more if needed.


class BusObject:

    def __init__(self, name, stops):
        self.name = name
        self.stops = [stops]  # This is a list. Every item is a list with contents [stop_name, lat, long]
        self.firstStation = self.stops[0]  # Track first station
        self.lastStation = self.stops[0]  # Track second station

    def add_stops(self, stop_name, latitude, longitude):
        self.stops.append([stop_name, latitude, longitude])
        self.lastStation = self.stops[len(self.stops) - 1] # Update last station
