from flask import Flask, render_template
import map_creator

# This is basically a miniature web server.
app = Flask(__name__)

@app.route('/map')
def route():
   map_creator.generate_route([5.270712, 103.108608], [4.051934, 100.968997])
   return render_template('route.html')


@app.route('/')
def hello_world():
   map_creator.generate_map()
   return render_template('map.html')


# Runs the web server
if __name__ == '__main__':
   app.run()