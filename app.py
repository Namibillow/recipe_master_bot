# !/usr/bin/env python

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify

import re

from recipe import Recipe
from youtube_scrape import YouTube
# import recipe_scrape as rs
# import check_validity as valid

import os
import json


app = Flask(__name__)


@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # See the json data we received as str
    print(request.is_json)
    print("Request:")
    print(json.dumps(req, indent=4))

    try:
        # get action name from Dialogflow
        action = req.get('queryResult').get('action')

    except AttributeError:
        return "json error"

    # return str(action)
    res = processRequest(req, action)

    return make_response(jsonify(res))


def processRequest(req, action):
    print("Action:")
    print(action)

    if action == "getIngredients":
        res = storeInfo(req, action)

    elif action == "video_recipe":
        res = storeInfo(req, "video")

    else:
        print("no action!!")
        res = {}

    return res


def storeInfo(req, action):
    '''
    stores all the ingredients and get response
    '''

    if action == "video":
        parameter = req['queryResult']['outputContexts'][0]['parameters']['ingredients']
    else:
        print("Looking for recipes")
        parameter = req['queryResult']["parameters"]['ingredients']

    parameter = parameter.lower()

    print('Dialogflow Parameters (Ingredients):')
    print(json.dumps(parameter, indent=4))
    print(type(parameter))

    parameters = parameter.split(",")

    # Strip all the non-alphabetic part and extra white space
    regex = re.compile('[^a-z]')
    parameters = [regex.sub(" ", i).strip() for i in parameters]

    if not parameters:  # if its empty
        response = {'fulfillmentText': "I think %s is not a food..." % parameter}

    else:
        if action == "video":
            video = YouTube()
            video.add_query(parameters)

            response = video.youtube_search()

        else:
            recipe = Recipe()

            # returns list
            # food_names = valid.food_exist(parameters)

            # if(food_names):
            recipe.add_ingredients(parameters)

            response = recipe.get_search_result()

    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
