import flask
from flask import request
from recommender_api import make_prediction
from flask import jsonify
import pickle

# Initialize the app

app = flask.Flask(__name__)
# form_basic is the prediction site
@app.route("/form_basic.html", methods=["GET"])
def form():
    input_values = 0
    recommendations = 0
    pic_url=0
    # First time loading page, nothing is passed. After fields are entered, pass 
    # those arguments into model
    if request.args:
        username_in = str(request.args['username_in'])
        genres_in = str(request.args['genres_in'])
        games_in = str(request.args['games_in'])
        input_values, recommendations, _= make_prediction(username_in, genres_in, games_in)

    return flask.render_template('form_basic.html',
                                     user_input=input_values,
                                     recommendation=recommendations)

# Landing page

@app.route("/index.html", methods=["GET"])
def index():
    return flask.render_template('index.html')
@app.route("/", methods=["GET"])
def predict():
    return flask.render_template('index.html')
    # request.args contains all the arguments passed by our form
    # comes built in with flask. It is a dictionary of the form
    # "form name (as set in template)" (key): "string in the textbox" (value)
    print(request.args)

# Start the server, continuously listen to requests.
if __name__=="__main__":
    # For local development:
    app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()
