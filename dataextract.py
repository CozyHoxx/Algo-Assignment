import pandas
import transport_objects as tr


pandas.set_option('display.expand_frame_repr', False)

# Prototype data parser
# Parse data from an excel file and create a list of route
# for now its just a bus route.


def generate_bus_route():
    data = pandas.read_excel('..\Dataset\MRT Bus Route.xlsx')
    df = pandas.DataFrame(data, columns=['Bus Stop Name', 'Latitud', 'Longitud', 'ROUTE ID', 'Route Name', ])

    bus_route_list = []
    current_route = ""
    stop = -1

    # This file is sorted according to routes, so we just check if the row is referring to the same route each loop.
    for i in df.index:
        # We insert a new route if its a new one
        if current_route != df['Route Name'][i]:
            current_route = df['Route Name'][i]
            stop += 1
            bus_route_list.append(
                tr.BusObject(df['Route Name'][i], [df['Bus Stop Name'][i], df['Latitud'][i], df['Longitud'][i]]))
        else:
            # We keep adding new stops to the current route.
            bus_route_list[stop].add_stops(df['Bus Stop Name'][i], df['Latitud'][i], df['Longitud'][i])

    return bus_route_list
