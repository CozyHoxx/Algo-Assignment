import pandas
# import transport_objects as tr
import networkx as nx
from geopy import distance
from enum import Enum

# Prototype data parser
# Parse data from an excel file and create a list of route
# for now its just a bus route.

# Graph used is weighted directed graph
G = nx.DiGraph()


class Transport(Enum):
    NULL = -1
    BUS = 1
    TRAIN = 2
    AIRPLANE = 3
    WALK = 4


def generate_bus_route(graph: nx.Graph):
    data = pandas.read_excel('Dataset\\MRT Bus Route.xlsx')
    df = pandas.DataFrame(data, columns=['Bus Stop Name', 'Latitud', 'Longitud', 'ROUTE ID', 'Route Name', ])

    # bus_route_list = []
    current_route = ""
    stop = -1
    prev_lat = 0.0
    prev_lon = 0.0
    # This file is sorted according to routes, so we just check if the row is referring to the same route each loop.
    for i in df.index:
        lat = df['Latitud'][i]
        lon = df['Longitud'][i]
        stop_name = df['Bus Stop Name'][i]
        # We insert a new route if its a new one
        if current_route != df['Route Name'][i]:
            current_route = df['Route Name'][i]
            G.add_node((lat, lon), stop_name=stop_name, route_name=current_route)
        else:
            # We keep adding new stops to the current route.
            G.add_node((lat, lon), stop_name=stop_name, route_name=current_route)
            G.add_edge((prev_lat, prev_lon), (lat, lon), route_name=current_route, type=Transport.BUS,
                       weight=distance.distance((lat, lon), (prev_lat, prev_lon)).kilometers)
        prev_lat = lat
        prev_lon = lon


def generate_train_route(graph: nx.Graph):
    data = pandas.read_excel('Dataset\\Train Route.xlsx')
    df = pandas.DataFrame(data, columns=['Stop Name', 'Latitud', 'Longitud', 'ROUTE ID', 'Route Name', ])

    current_route = ""
    stop = -1
    prev_lat = 0.0
    prev_lon = 0.0

    for i in df.index:
        lat = df['Latitud'][i]
        lon = df['Longitud'][i]
        stop_name = df['Stop Name'][i]
        if current_route != df['Route Name'][i]:
            current_route = df['Route Name'][i]
            G.add_node((lat, lon), stop_name=stop_name, route_name=current_route)
        else:
            # We keep adding new stops to the current route.
            G.add_node((lat, lon), stop_name=stop_name, route_name=current_route)
            G.add_edge((prev_lat, prev_lon), (lat, lon), route_name=current_route, type=Transport.TRAIN,
                       weight=distance.distance((lat, lon), (prev_lat, prev_lon)).kilometers)
        prev_lat = lat
        prev_lon = lon


def generate_walking_route():
    count = 0
    for curr, curr_data in G.nodes(data=True):
        for neigh, neigh_data in G.nodes(data=True):
            dist = distance.distance((curr[0], curr[1]), (neigh[0], neigh[1])).kilometers
            if dist < 0.3:
                if (curr_data['route_name'] != neigh_data['route_name']) & (not G.has_edge(curr, neigh)):
                    G.add_edge((curr[0], curr[1]), (neigh[0], neigh[1]), route_name='walk', type=Transport.WALK,
                           weight=dist)
                    count+=1
                    print("Added" + str(count) + "Distance = " + str(dist))


def get_graph():
    return G


generate_bus_route(G)
generate_train_route(G)
for n, data in G.nodes(data=True):
    print(n)
    print(data['stop_name'])
    print(data['route_name'])
generate_walking_route()
for u, v, a in G.edges(data=True):
    print(str(u) + "->" + str(v))
    print(str(a['weight']) + "KM")

print(G.nodes)
print(G.edges)
