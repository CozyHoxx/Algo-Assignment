import pandas
import networkx as nx
from geopy import distance
from enum import Enum
from itertools import islice
import Word_Pos_Neg_test

# The Graph used is weighted directed graph
# G is weighted directed graph
G = nx.DiGraph()
H = nx.DiGraph()
I = nx.DiGraph()
sentiment = Word_Pos_Neg_test.get_senti()
total_sentiment = sentiment[0] + sentiment[1] + sentiment[2]
bus_sc = sentiment[0]/total_sentiment
train_sc = sentiment[1]/total_sentiment
plane_sc = sentiment[2]/total_sentiment


class Transport(Enum):
    NULL = -1
    BUS = 1
    TRAIN = 2
    AIRPLANE = 3
    WALK = 4
    TAXI = 5


def generate_bus_route(graph: nx.Graph):
    data = pandas.read_excel('Dataset\\Bus.xlsx')
    df = pandas.DataFrame(data, columns=['Stop Name', 'Latitud', 'Longitud', 'ROUTE ID', 'Route Name', ])
    # get_route_from_file(df, Transport.BUS)
    for i in df.index:
        lat = df['Latitud'][i]
        lon = df['Longitud'][i]
        I.add_node((lat, lon), stop_name=df['Stop Name'][i], route_name=df['Route Name'][i])

    for node in I.nodes(data=True):
        for other_node in I.nodes(data=True):
            if node != other_node:
                dist = distance.distance(node[0], other_node[0]).kilometers
                I.add_edge(node[0], other_node[0], route_name='Bus', type=Transport.BUS,
                           weight=dist - (dist*bus_sc), dist=dist)


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
    get_airport_route_from_file(df)


def get_airport_route_from_file(df: pandas.DataFrame):
    # Add every airport to the Graph H
    for i in df.index:
        lat = df['Latitud'][i]
        lon = df['Longitud'][i]
        H.add_node((lat, lon), stop_name=df['Airport'][i], route_name=df['Route Name'][i])

    for node in H.nodes(data=True):
        for other_node in H.nodes(data=True):
            if node != other_node:
                dist = distance.distance(node[0], other_node[0]).kilometers
                H.add_edge(node[0], other_node[0], route_name='airplane', type=Transport.AIRPLANE,
                           weight=dist - (dist*plane_sc), dist=dist)


def get_route_from_file(df: pandas.DataFrame, transport_type):
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
            dist = distance.distance((lat, lon), (prev_lat, prev_lon)).kilometers
            G.add_edge((prev_lat, prev_lon), (lat, lon), route_name=current_route, type=transport_type,
                       weight=dist - (dist*train_sc), dist=dist)
            if transport_type == Transport.TRAIN:
                G.add_edge((lat, lon), (prev_lat, prev_lon), route_name=current_route, type=transport_type,
                           weight=dist - (dist*train_sc), dist=dist)
        generate_walking_route(lat, lon, G.nodes[(lat, lon)])
        prev_lat = lat
        prev_lon = lon


def generate_walking_route(lat, lon, curr: G.nodes):
    for neigh, neigh_data in G.nodes(data=True):
        dist = distance.distance((lat, lon), (neigh[0], neigh[1])).kilometers
        if dist < 1:
            if (curr['route_name'] != neigh_data['route_name']) & (not G.has_edge((lat, lon), neigh)):
                G.add_edge((lat, lon), (neigh[0], neigh[1]), route_name='walk', type=Transport.WALK,
                           weight=dist, dist=dist)
                G.add_edge((neigh[0], neigh[1]), (lat, lon), route_name='walk', type=Transport.WALK,
                           weight=dist, dist=dist)
        elif dist < 10:
            if (curr['route_name'] != neigh_data['route_name']) & (not G.has_edge((lat, lon), neigh)):
                G.add_edge((lat, lon), (neigh[0], neigh[1]), route_name='taxi', type=Transport.TAXI,
                           weight=dist, dist=dist)
                G.add_edge((neigh[0], neigh[1]), (lat, lon), route_name='taxi', type=Transport.TAXI,
                           weight=dist, dist=dist)

    # last hope for end points not connecting
    if (curr['stop_name'] == 'Start point' or curr['stop_name'] == 'End point') and G[
        (lat, lon)].__len__() <= 0:
        for neigh, neigh_data in G.nodes(data=True):
            dist = distance.distance((lat, lon), (neigh[0], neigh[1])).kilometers
            if dist < 20:
                if (curr['route_name'] != neigh_data['route_name']) & (not G.has_edge((lat, lon), neigh)):
                    G.add_edge((lat, lon), (neigh[0], neigh[1]), route_name='taxi', type=Transport.TAXI,
                               weight=dist, dist=dist)
                    G.add_edge((neigh[0], neigh[1]), (lat, lon), route_name='taxi', type=Transport.TAXI,
                               weight=dist, dist=dist)


def get_graph():
    return G


def generate_path(start_pos, end_pos):
    print("Connecting start and end......")

    G.add_node(start_pos, stop_name='Start point', route_name='none')

    G.add_node(end_pos, stop_name='End point', route_name='none')

    # Connect node to nearby neighbours
    generate_walking_route(start_pos[0], start_pos[1], G.nodes[start_pos])
    generate_walking_route(end_pos[0], end_pos[1], G.nodes[end_pos])

    # Using Yen's k shortest-path algorithm
    list_path = list(islice(nx.shortest_simple_paths(G, start_pos, end_pos, weight='weight'), 5))

    # Create a list of subgraphs containing the relevant nodes and edges to be displayed on the map.
    list_subgraph = []
    route_list = []
    for short_path in list_path:
        pairs = list(zip(short_path, short_path[1:]))
        # print(pairs)
        list_subgraph.append(G.edge_subgraph(pairs).copy())
        route_string = []
        total_dist = 0.0
        total_weight = 0.0
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
            dist = round(G[u][v]['dist'], 2)
            weight = round(G[u][v]['weight'], 2)
            total_dist += G[u][v]['dist']
            total_weight += G[u][v]['weight']
            route_string.append(
                stop1 + " to " + stop2 + " by " + str(str_transport) + ". (" + str(dist) + " km)" + "(Weight = " + str(
                    weight) + ")")
        total_dist = round(total_dist, 2)
        route_string.append("Total distance = " + str(total_dist) + " km")
        total_weight = round(total_weight, 2)
        route_string.append("Total weight = " + str(total_weight))
        route_list.append(route_string)

    return list_subgraph, route_list


generate_airplane_route(G)
G = nx.compose(G, H)  # Combine G and H
generate_train_route(G)
generate_bus_route(G)
G = nx.compose(G, I)  # Combine G and I

# Function below is to connect all the bus to all other nodes
for node in I.nodes(data=True):
    lat = node[0][0]
    lon = node[0][1]
    generate_walking_route(lat, lon, G.nodes[(lat, lon)])
