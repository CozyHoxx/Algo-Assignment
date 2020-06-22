import pandas
import networkx as nx
from geopy import distance
from enum import Enum
from itertools import islice
import matplotlib.pyplot as plt

# Prototype data parser
# Parse data from an excel file and create a list of route
# for now its just a bus route.

# The Graph used is weighted directed graph
# G is weighted directed graph
G = nx.DiGraph()
H = nx.DiGraph()


# this comment is to test github


class Transport(Enum):
    NULL = -1
    BUS = 1
    TRAIN = 2
    AIRPLANE = 3
    WALK = 4
    TAXI = 5


def generate_bus_route(graph: nx.Graph):
    data = pandas.read_excel('Dataset\\MRT Bus Route.xlsx')
    df = pandas.DataFrame(data, columns=['Stop Name', 'Latitud', 'Longitud', 'ROUTE ID', 'Route Name', ])
    get_route_from_file(df, Transport.BUS)


def generate_train_route(graph: nx.Graph):
    data = pandas.read_excel('Dataset\\ETS Train.xlsx')
    df = pandas.DataFrame(data, columns=['Stop Name', 'Latitud', 'Longitud', 'ROUTE ID', 'Route Name', ])
    get_route_from_file(df, Transport.TRAIN)
    data = pandas.read_excel('Dataset\\KTM Komuter.xlsx')
    df = pandas.DataFrame(data, columns=['Stop Name', 'Latitud', 'Longitud', 'ROUTE ID', 'Route Name', ])
    get_route_from_file(df, Transport.TRAIN)


def generate_airplane_route(graph: nx.Graph):
    data = pandas.read_excel('Dataset\\Airports.xlsx')
    df = pandas.DataFrame(data, columns=['Airport', 'Latitud', 'Longitud', 'Route Name'])
    get_airport_route_from_file(df, Transport.AIRPLANE)


def get_airport_route_from_file(df: pandas.DataFrame, type):
    # Add every airport to the Graph H
    for i in df.index:
        lat = df['Latitud'][i]
        lon = df['Longitud'][i]
        H.add_node((lat, lon), stop_name=df['Airport'][i], route_name=df['Route Name'][i])

    for node in H.nodes(data=True):
        for other_node in H.nodes(data=True):
            if node != other_node:
                H.add_edge(node[0], other_node[0], route_name='airplane', type=Transport.AIRPLANE,
                           weight=distance.distance(node[0], other_node[0]).kilometers)


def get_route_from_file(df: pandas.DataFrame, type):
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
            G.add_edge((prev_lat, prev_lon), (lat, lon), route_name=current_route, type=type,
                       weight=distance.distance((lat, lon), (prev_lat, prev_lon)).kilometers)
            if type == Transport.TRAIN:
                G.add_edge((lat, lon), (prev_lat, prev_lon), route_name=current_route, type=type,
                           weight=distance.distance((lat, lon), (prev_lat, prev_lon)).kilometers)
        generate_walking_route(lat, lon, G.nodes[(lat, lon)])
        prev_lat = lat
        prev_lon = lon


# To add bus stop that are close to their bus station
# ie; Phileo Damansara Bus Stop + Phileo Damansara Train Station
def generate_walking_route(lat, lon, curr: G.nodes):
    for neigh, neigh_data in G.nodes(data=True):
        dist = distance.distance((lat, lon), (neigh[0], neigh[1])).kilometers
        if dist < 1:
            if (curr['route_name'] != neigh_data['route_name']) & (not G.has_edge((lat, lon), neigh)):
                G.add_edge((lat, lon), (neigh[0], neigh[1]), route_name='walk', type=Transport.WALK,
                           weight=dist)
                G.add_edge((neigh[0], neigh[1]), (lat, lon), route_name='walk', type=Transport.WALK,
                           weight=dist)
        elif dist < 10:
            if (curr['route_name'] != neigh_data['route_name']) & (not G.has_edge((lat, lon), neigh)):
                G.add_edge((lat, lon), (neigh[0], neigh[1]), route_name='taxi', type=Transport.TAXI,
                           weight=dist)
                G.add_edge((neigh[0], neigh[1]), (lat, lon), route_name='taxi', type=Transport.TAXI,
                           weight=dist)

    # BOILER PLATE CODE TO CONNECT DESTINATION POINTS TO NEARBY STAIONS TEMPORARILY
    # Just wanna see the destination markers.
    if (curr['stop_name'] == 'Start point' or curr['stop_name'] == 'End Point') and G[
        (lat, lon)].__len__() <= 0:
        print(curr['stop_name'] + "not connected")


def get_graph():
    return G


def generate_path(start_pos, end_pos):
    print("Connecting start and end......")

    G.add_node(start_pos, stop_name='Start point', route_name='none')

    G.add_node(end_pos, stop_name='End point', route_name='none')

    # Connect node to nearby neighbours

    generate_walking_route(start_pos[0], start_pos[1], G.nodes[start_pos])
    generate_walking_route(end_pos[0], end_pos[1], G.nodes[end_pos])

    # for p, d in G.nodes(data=True):
    #     dist = distance.distance(start_pos, (p[0], p[1])).kilometers
    #     if dist < 0.3:
    #         G.add_edge(start_pos, (p[0], p[1]), route_name='walk', type=Transport.WALK,
    #                    weight=dist)
    #
    # for p, d in G.nodes(data=True):
    #     dist = distance.distance(end_pos, (p[0], p[1])).kilometers
    #     if dist < 0.3:
    #         G.add_edge(end_pos, (p[0], p[1]), route_name='walk', type=Transport.WALK,
    #                    weight=dist)

    # path = nx.algorithms.dijkstra_path(G, start_pos, end_pos, weight='weight')
    # print(path)
    list_path = list(islice(nx.shortest_simple_paths(G, start_pos, end_pos, weight='weight'), 5))

    # Create a list of subgraphs containing the relevant nodes and edges to be displayed on the map.
    list_subgraph = []
    route_list = []
    for short_path in list_path:
        pairs = list(zip(short_path, short_path[1:]))
        # print(pairs)
        list_subgraph.append(G.edge_subgraph(pairs).copy())
        route_string = []
        for u, v in pairs:
            stop1 = G.nodes[u]['stop_name']
            stop2 = G.nodes[v]['stop_name']
            transport_type = G[u][v]['type']
            str_transport = " "
            if transport_type == Transport.WALK:
                str_transport = "walking"
            elif transport_type == Transport.BUS:
                str_transport = "bus"
            elif transport_type == Transport.TRAIN:
                str_transport = "train"
            elif transport_type == Transport.AIRPLANE:
                str_transport = "airplane"
            elif transport_type == Transport.TAXI:
                str_transport = "taxi"
            route_string.append(stop1 + " to " + stop2 + " by " + str(str_transport) + ".")
        route_list.append(route_string)

    return list_subgraph, route_list


generate_airplane_route(G)
G = nx.compose(G, H)  # Combine G and H
generate_train_route(G)
# Boiler plate code to see other coordinates
list_of_coord = ((5.41123, 100.33543), (4.50327, 101.3981), (4.849050, 100.739113), (6.4414, 100.19862),
                 (6.32649, 99.8432))
for coord in list_of_coord:
    G.add_node(coord, stop_name='Start point', route_name='none')
    generate_walking_route(coord[0], coord[1], G.nodes[coord])
# print(G.order())
# nx.draw(H) # Airport
# nx.draw(G) # Train + Bus route
# nx.draw(F)
# plt.show()

# print(G.nodes)
# print(G.edges)
