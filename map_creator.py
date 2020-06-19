import gmplot
import dataextract as dat
import itertools
import transport_objects as tr
from pyllist import sllist, sllistnode
import os

# bus_route_list = dat.generate_bus_route()
# train_route_list = dat.generate_train_route()
routes = dat.get_graph()
gmap = gmplot.GoogleMapPlotter(3.147447, 101.655015, 13)


def generate_map():
    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

    colours = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])

    # Generate location of all stations
    # Mark locations first
    lat, lon = map(list, zip(*routes.nodes))
    gmap.scatter(lat, lon, '#939393', size=40, marker=False)

    for u, v, data in routes.edges(data=True):
        if data['type'] == dat.Transport.BUS:
            color = 'r'
        elif data['type'] == dat.Transport.WALK:
            color = 'y'
        elif data['type'] == dat.Transport.TRAIN:
            color = 'b'
        elif data['type'] == dat.Transport.AIRPLANE:
            color = 'k'
        else:
            color = 'b'
        gmap.scatter([u[0], v[0]], [u[1], v[1]], color, edge_width=5)
        gmap.plot([u[0], v[0]], [u[1], v[1]], color, edge_width=2)

    # Draw
    gmap.draw('templates\\map.html')


def generate_route():
    # start_pos [lat,lon] and end_pos [lat,lon]
    start_pos = (6.3322, 99.7322)  # FSKTM
    end_pos = (1.5818,	103.654083)  # MRT PB Daman

    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    gmap.marker(start_pos[0], start_pos[1], 'w', title="START")
    gmap.marker(end_pos[0], end_pos[1], 'w', title="END")
    # path finding logic may go here
    # We start by connecting the start and end position to any neighbour nodes around it (at LEAST one)

    path = dat.generate_path(start_pos, end_pos)
    for parth in path:
        lat, lon = map(list, zip(*parth))

        gmap.plot(lat, lon, 'w', edge_width=5)

    # Draw
    gmap.draw('templates\\map.html')


generate_map()
generate_route()
