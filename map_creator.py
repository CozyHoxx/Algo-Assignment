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
gmap = gmplot.GoogleMapPlotter(3.147447, 101.655015, 7)


def generate_map():
    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
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
            color = 'k'
        elif data['type'] == Transport.TAXI:
            color = 'y'
        else:
            color = 'b'
        # gmap.scatter([u[0], v[0]], [u[1], v[1]], color, edge_width=5)
        gmap.polygon([u[0], v[0]], [u[1], v[1]], color, edge_width=2)

    # BOILER PLATE CODE TO DISPLAY DESTINATION POINTS TEMPORARILY
    # Just wanna see the destination markers.
    lat2, lon2 = map(list, zip((5.41123, 100.33543), (4.50327, 101.3981), (4.849050, 100.739113), (6.4414, 100.19862),
                               (6.32649, 99.8432)))
    gmap.scatter(lat2, lon2, 'w', edge_width=5)
    # Draw
    gmap.draw('templates\\map.html')


def generate_route():
    # start_pos [lat,lon] and end_pos [lat,lon]
    start_pos = (6.3322, 99.7322)  # FSKTM
    end_pos = (1.5818, 103.654083)  # MRT PB Daman
    colours = itertools.cycle(['#0275d8', '#5cb85c', '#f0ad4e', '#d9534f', '#292b2c'])
    gmap = gmplot.GoogleMapPlotter(3.147447, 101.655015, 7)
    # PATCH FOR RENDERING MARKERS! DO NOT TOUCH.
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    gmap.marker(start_pos[0], start_pos[1], 'w', title="START")
    gmap.marker(end_pos[0], end_pos[1], 'w', title="END")
    # path finding logic may go here
    # We start by connecting the start and end position to any neighbour nodes around it (at LEAST one)

    route_subgraph = dat.generate_path(start_pos, end_pos)
    route_list = []
    for curr_route in route_subgraph:
        print("NEXT ROUTE")
        print(curr_route.edges())
        lat, lon = map(list, zip(*curr_route.nodes))
        route_string = ""
        for u, v, data in curr_route.edges(data=True):
            curr_color = next(colours)
            stop1 = routes.nodes[u]['stop_name']
            stop2 = routes.nodes[v]['stop_name']
            transport_type = " "
            if data['type'] == Transport.WALK:
                transport_type = "walking"
            elif data['type'] == Transport.BUS:
                transport_type = "bus"
            elif data['type'] == Transport.TRAIN:
                transport_type = "train"
            elif data['type'] == Transport.AIRPLANE:
                transport_type = "airplane"
            print(stop1 + " to " + stop2 + " by " + str(transport_type))
            route_string += stop1 + " to " + stop2 + " by " + str(transport_type)
            gmap.marker(u[0], u[1], 'w', title=stop1)
            gmap.marker(v[0], v[1], 'w', title=stop2)
            # gmap.scatter([u[0], v[0]], [u[1], v[1]], 'r', edge_width=5)
            gmap.polygon([u[0], v[0]], [u[1], v[1]], curr_color, edge_width=2)
        route_list.append(route_string)

        # gmap.plot(lat, lon, 'w', edge_width=5)

    # Draw
    gmap.draw('templates\\map.html')
    return route_list


# generate_map()
# generate_route()
