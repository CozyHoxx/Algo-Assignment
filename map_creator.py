import gmplot
import dataextract as dat
import itertools
import transport_objects as tr
from pyllist import sllist, sllistnode
import os

# bus_route_list = dat.generate_bus_route()
# train_route_list = dat.generate_train_route()
routes = dat.get_graph()
gmap = gmplot.GoogleMapPlotter(3.150447, 101.749015, 13)

def generate_map():

    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    # data here

    # bus_route_list = []

    colours = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])
    # Generate location of all stations.

    # for seq in (bus_route_list, train_route_list):
    #     current_colour = next(colours)
    #     for route in seq:
    #         station_lats = []
    #         station_lons = []
    #         for stop in route.stops:
    #             station_lats.append(stop[1])
    #             station_lons.append(stop[2])
    #         gmap.scatter(station_lats, station_lons, '#3B0B39', size=40, marker=False)
    #         gmap.plot(station_lats, station_lons, current_colour, edge_width=5)
    #         gmap.marker(route.firstStation[1], route.firstStation[2], current_colour)
    #         gmap.marker(route.lastStation[1], route.lastStation[2], current_colour)

    # Mark locations first

    lat, lon = map(list, zip(*routes.nodes))
    gmap.scatter(lat, lon, '#000000', size=40, marker=False)
    for u, v, data in routes.edges(data=True):
        color = ''
        if data['type'] == dat.Transport.BUS:
            color = 'r'
        elif data['type'] == dat.Transport.WALK:
            color = 'y'
        else:
            color = 'b'
        gmap.plot([u[0],v[0]], [u[1],v[1]], color, edge_width=5)

    start_pos = (3.12986, 101.64247)
    end_pos = (3.128304, 101.64286)
    gmap.marker(start_pos[0], start_pos[1], "red", title="START")
    gmap.marker(end_pos[0], end_pos[1], "red", title="END")


    # Draw
    gmap.draw('templates\\map.html')



def generate_route():
    # os.remove('templates\\map.html')
    start_pos = (3.128440, 101.650146) # FSKTM
    # start_pos = (3.119611, 101.643204) # MRT Phileo Station
    # end_pos = (3.128304, 101.64286)  # MRT Phileo Station
    end_pos = (3.13732, 101.68734) # MRT PB Daman


    # start_pos [lat,lon] and end_pos [lat,lon]
    # gmap = gmplot.GoogleMapPlotter(start_lat, start_lon, 13)
    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    gmap.marker(start_pos[0], start_pos[1], 'r', title="START")
    gmap.marker(end_pos[0], end_pos[1], 'r', title="END")
    # path finding logic may go here
    # We start by connecting the start and end position to any neighbour nodes around it (at LEAST one)

    path = dat.generate_path(start_pos, end_pos)
    lat, lon = map(list, zip(*path))
    # PLACEHOLDER ROUTE
    # generate_map()
    # Draw out the lines


    # gmap.scatter(journey_lats, journey_lons, '#3B0B39', size=40, marker=False)
    gmap.plot(lat, lon, 'g', edge_width=5)
    # gmap.marker(journey_lats[0], journey_lons[0], 'g')
    # gmap.marker(journey_lats[len(journey_lats) - 1], journey_lons[len(journey_lons) - 1], 'r')

    # Draw
    gmap.draw('templates\\map.html')


generate_map()
generate_route()