import gmplot
import dataextract as dat
import itertools
import os

def generate_map():
    gmap = gmplot.GoogleMapPlotter(3.150447, 101.749015, 13)
    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    # data here
    bus_route_list = dat.generate_bus_route()
    colours = itertools.cycle(['b','g','r','c', 'm', 'y','k','w'])
    # Generate location of all stations.

    for route in bus_route_list:
        station_lats = []
        station_lons = []
        for stop in route.stops:
            station_lats.append(stop[1])
            station_lons.append(stop[2])
        current_colour = next(colours)
        gmap.scatter(station_lats, station_lons, '#3B0B39', size=40, marker=False)
        gmap.plot(station_lats, station_lons, current_colour, edge_width=5)
        gmap.marker(route.firstStation[1], route.firstStation[2], current_colour)
        gmap.marker(route.lastStation[1], route.lastStation[2], current_colour)

    # Marker
    hidden_gem_lat, hidden_gem_lon = 3.171593, 101.693305
    gmap.marker(hidden_gem_lat, hidden_gem_lon, "cornflowerblue")

    gmap.marker(3.147331, 101.750363, "red")

    # Draw
    gmap.draw('templates\\map.html')

def generate_route(start_pos, end_pos):

    # os.remove('templates\\map.html')

    # start_pos [lat,lon] and end_pos [lat,lon]
    gmap = gmplot.GoogleMapPlotter(3.150447, 101.749015, 5)
    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

    journey_lats = [start_pos[0]]
    journey_lons = [start_pos[1]]

    # path finding logic may go here
    # to be added later by SOMEONE ELSE DAMMIT
    journey_lats.append(end_pos[0])
    journey_lons.append(end_pos[1])

    gmap.scatter(journey_lats, journey_lons, '#3B0B39', size=40, marker=False)
    gmap.plot(journey_lats, journey_lons, 'b', edge_width=5)
    gmap.marker(journey_lats[0], journey_lons[0], 'g')
    gmap.marker(journey_lats[len(journey_lats) - 1], journey_lons[len(journey_lons) - 1], 'r')

    # Draw
    gmap.draw('templates\\map.html')