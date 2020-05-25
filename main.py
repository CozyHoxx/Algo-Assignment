from flask import Flask, render_template
import map_creator

# This is basically a miniature web server.
app = Flask(__name__)

@app.route('/')
def hello_world():
   map_creator.generate_map()
   return render_template('map.html')


# Runs the web server
if __name__ == '__main__':
   app.run()