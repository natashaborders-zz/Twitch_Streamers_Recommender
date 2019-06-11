import flask
from flask import request
from recommender_api import make_prediction
from flask import jsonify

# Initialize the app

app = flask.Flask(__name__)

# An example of routing:
# If they go to the page "/" (this means a GET request
# to the page http://127.0.0.1:5000/), return a simple
# page that says the site is up!
@app.route("/form_basic.html", methods=["GET"])
def form():
    input_values = 0
    recommendations = 0
    # print(type(request.args))
    if request.args:
        # print(list(request.args.keys()))
        username_in = str(request.args['username_in'])
        genres_in = str(request.args['genres_in'])
        games_in = str(request.args['games_in'])
        input_values, recommendations = make_prediction(username_in, genres_in, games_in)

    return flask.render_template('form_basic.html',
                                     user_input=input_values,
                                     recommendation=recommendations)

@app.route("/index.html", methods=["GET"])
def index():
    x_input = 0
    predictions = 0
    return flask.render_template('index.html',
                                     chat_in=x_input,
                                     prediction=predictions)

@app.route("/", methods=["GET"])
def predict():
    x_input = 0
    predictions = 0
    return flask.render_template('index.html',
                                     chat_in=x_input,
                                     prediction=predictions)
    # request.args contains all the arguments passed by our form
    # comes built in with flask. It is a dictionary of the form
    # "form name (as set in template)" (key): "string in the textbox" (value)
    print(request.args)
    # if(request.args):
    #     x_input, predictions = make_prediction(request.args['chat_in'])
    #     print(x_input)
    #     return flask.render_template('predictor.html',
    #                                  chat_in=x_input,
    #                                  prediction=predictions)
    # else: 
    #     #For first load, request.args will be an empty ImmutableDict type. If this is the case,
    #     # we need to pass an empty string into make_prediction function so no errors are thrown.
    #     x_input, predictions = make_prediction('')
    #     return flask.render_template('predictor.html',
    #                                  chat_in=x_input,
    #                                  prediction=predictions)


# Start the server, continuously listen to requests.

if __name__=="__main__":
    # For local development:
    app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()
