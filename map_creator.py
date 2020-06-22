import gmplot
import dataextract as dat
import itertools
from dataextract import Transport
import networkx as nx
from pyllist import sllist, sllistnode
import os

# bus_route_list = dat.generate_bus_route()
# train_route_list = dat.generate_train_route()
routes = dat.get_graph()


def generate_basic_map():
    gmap = gmplot.GoogleMapPlotter(3.147447, 101.655015, 7)
    gmap.draw('templates\\map.html')


def generate_full_map():
    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap = gmplot.GoogleMapPlotter(3.147447, 101.655015, 7)
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

    colours = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])

    # Generate location of all stations
    # Mark locations first
    lat, lon = map(list, zip(*routes.nodes))
    gmap.scatter(lat, lon, '#939393', size=40, marker=False)

    for u, v, data in routes.edges(data=True):
        if data['type'] == Transport.BUS:
            color = 'r'
        elif data['type'] == Transport.WALK:
            color = 'y'
        elif data['type'] == Transport.TRAIN:
            color = 'b'
        elif data['type'] == Transport.AIRPLANE:
            color = 'w'
        elif data['type'] == Transport.TAXI:
            color = 'y'
        else:
            color = 'w'
        gmap.polygon([u[0], v[0]], [u[1], v[1]], color, edge_width=2)
    # Draw
    #
    # lat2, lon2 = map(list, zip((5.41123, 100.33543), (4.50327, 101.3981), (4.849050, 100.739113), (6.4414, 100.19862),
    #                            (6.32649, 99.8432)))
    # gmap.scatter(lat2, lon2, 'w', edge_width=5)
    gmap.draw('templates\\full_map.html')


def generate_route(start_pos, end_pos):
    colours = itertools.cycle(['#0275d8', '#5cb85c', '#f0ad4e', '#d9534f', '#292b2c'])

    route_subgraph, route_list = dat.generate_path(start_pos, end_pos)
    map_id = 1
    for curr_route in route_subgraph:
        new_route_gmap = gmplot.GoogleMapPlotter(start_pos[0], start_pos[1], 8)
        new_route_gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

        lat, lon = map(list, zip(*curr_route.nodes))
        curr_color = next(colours)
        for u, v, data in curr_route.edges(data=True):
            stop1 = routes.nodes[u]['stop_name']
            stop2 = routes.nodes[v]['stop_name']
            if stop1 == 'Start point':
                new_route_gmap.marker(u[0], u[1], 'r', title=stop1)
            else:
                new_route_gmap.marker(u[0], u[1], curr_color, title=stop1)
            if  stop2 == 'End point':
                new_route_gmap.marker(v[0], v[1], 'r', title=stop2)
            else:
                new_route_gmap.marker(v[0], v[1], curr_color, title=stop2)

            new_route_gmap.polygon([u[0], v[0]], [u[1], v[1]], curr_color, edge_width=2)
        new_route_gmap.draw('templates\\routes\\route' + str(map_id) + '.html')
        map_id += 1

    # Draw
    return route_list
