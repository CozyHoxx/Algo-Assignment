from flask import Flask, render_template, send_file, request, redirect
import map_creator

# This is basically a miniature web server.
app = Flask(__name__)
app.send_file_max_age_default = 0


@app.route('/')
def hello_world():
    map_creator.generate_route([3.167026, 101.558437], [0, 0])
    return render_template('index.html')


@app.route('/response', methods=['POST'])
def response():
    # start_lat = float(request.form.get("start_lat"))
    # start_long = float(request.form.get("start_long"))
    # end_lat = float(request.form.get("end_lat"))
    # end_long = float(request.form.get("end_long"))

    map_creator.generate_route([3.167026, 101.558437], [0, 0])

    return render_template("index.html")

@app.route('/map.html')
def show_map():
    return send_file('templates\\map.html')


# Runs the web server
if __name__ == '__main__':
    app.run()
