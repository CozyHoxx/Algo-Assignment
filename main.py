from flask import Flask, render_template, send_file, request, redirect
from enum import Enum
import map_creator

# This is basically a miniature web server.
app = Flask(__name__)
app.send_file_max_age_default = 0


class Dest(Enum):
    PENANG = 'Penang'
    CAMERON = 'Cameron'
    LANGKAWI = 'Langkawi'
    PERLIS = 'Perlis'
    PERAK = 'Perak'


@app.route('/')
def hello_world():
    route_1 = {'route_1': ['Route 1 here!']}
    route_2 = {'route_2': ['Route 2 here!']}
    route_3 = {'route_3': ['Route 3 here!']}
    route_4 = {'route_4': ['Route 4 here!']}
    route_5 = {'route_5': ['Route 5 here!']}
    map_creator.generate_basic_map()
    # map_creator.generate_route([3.167026, 101.558437], [0, 0])
    return render_template('index.html', route_1=route_1, route_2=route_2, route_3=route_3, route_4=route_4,
                           route_5=route_5, map_src='map')


@app.route('/response', methods=['POST'])
def response():
    destination: str = request.form.get("destination")
    dest_name = ""
    print(destination)
    lat, lon = 0, 0
    if destination == Dest.PENANG.value:
        lat, lon = 5.41123, 100.33543
        dest_name = "Fort Cornwallis, Penang"
    elif destination == Dest.CAMERON.value:
        lat, lon = 4.50327, 101.3981
        dest_name = "Cameron Highland Butterfly Garden"
    elif destination == Dest.LANGKAWI.value:
        lat, lon = 6.32649, 99.8432
        dest_name = "Dataran Lang, Langkawi"
    elif destination == Dest.PERLIS.value:
        lat, lon = 6.4414, 100.19862
        dest_name = "Taman Anggur, Perlis"
    elif destination == Dest.PERAK.value:
        lat, lon = 4.849050, 100.739113
        dest_name = "Taiping Lake Garden, Perak"
    print(lat, lon)
    # map_creator.generate_route()
    route_list = map_creator.generate_route((3.167026, 101.558437), (lat, lon))
    print(route_list)
    # Ideally, if can la, return a list of routes for me to display thru here.
    route_1 = {'route_1': route_list[0]}
    route_2 = {'route_2': route_list[1]}
    route_3 = {'route_3': route_list[2]}
    route_4 = {'route_4': route_list[3]}
    route_5 = {'route_5': route_list[4]}
    return render_template('index.html', route_1=route_1, route_2=route_2, route_3=route_3, route_4=route_4,
                           route_5=route_5, dest=destination, map_src='route')


@app.route('/full_map')
def show_full_map():
    map_creator.generate_full_map()
    return render_template('full_map_page.html')


@app.route('/graph')
def show_word_graph():
    return render_template('graph.html')


@app.route('/map.html')
def show_map():
    return send_file('templates\\map.html')


@app.route('/full_map.html')
def show_the_real_map():
    return send_file('templates\\full_map.html')


@app.route('/route1.html')
def show_route_1():
    return send_file('templates\\routes\\route1.html')


@app.route('/route2.html')
def show_route_2():
    return send_file('templates\\routes\\route2.html')


@app.route('/route3.html')
def show_route_3():
    return send_file('templates\\routes\\route3.html')


@app.route('/route4.html')
def show_route_4():
    return send_file('templates\\routes\\route4.html')


@app.route('/route5.html')
def show_route_5():
    return send_file('templates\\routes\\route5.html')


# Runs the web server
if __name__ == '__main__':
    app.run()
