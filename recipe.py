# -*- coding:utf8 -*-
# !/usr/bin/env python

"""
Module that defines the Recipe class and defines helper functions to
process and validate date related to the recipe class

I am using EDAMAM API to get recipes: http://api2.bigoven.com
"""

from settings import get_keys
import requests
import random


class Recipe(object):

    def __init__(self):
        self.ingredients = []
        self.url = "https://api.edamam.com/search?q="
        self.indexFrom = 0
        self.indexTo = 100  # Exclusive

    def add_ingredients(self, ingredients):
        for i in ingredients:
            self.ingredients.append(i)

    def call_edmam_api(self):

        temp = [i + "+" for i in self.ingredients]
        temp = "".join(temp)[:-1]
        # return " I am dissappinted"

        self.url += temp + "&app_id=" + get_keys("EDMAM_ID") + "&app_key=" + get_keys("EDMAM_KEY") + "&from=" + str(self.indexFrom) + "&to=" + str(self.indexTo)

        print(self.url)

        recipes_result = requests.get(self.url)

        # If request fails
        if not recipes_result.status_code == requests.codes.ok:
            recipes_result.raise_for_status()
            return "oups failed"

        recipes = recipes_result.json()

        response = []

        # print('total', recipes['count'])
        # print('recipe hits', len(recipes['hits']))
        c = random.randint(0, self.indexTo - 10)
        # randomely select
        print("random", c)

        for recipe in (recipes['hits'])[c:c + 10]:
            info = []
            info.append(recipe['recipe']['label'])
            info.append(recipe['recipe']['image'])
            info.append(recipe['recipe']['url'])
            # print(recipe['recipe']['label'])
            # print(recipe['recipe']['image'])
            # print(recipe['recipe']['url'])

            food = []
            for ingredient in self.ingredients:
                if any(ingredient in r for r in recipe['recipe']['ingredientLines']):
                    food.append(ingredient)
                    # print(ingredient)

            info.append(food)
            response.append(info)

        return response

    def get_search_result(self):
        '''
        conver the response to valid format for dialogflow
        '''
        response = self.call_edmam_api()

        if response:
            res = {
                "fulfillmentText": "Got it! Here is the results I found:",
                "fulfillmentMessages": [
                    {
                        "platform": "FACEBOOK",
                        "text": {
                            "text": [
                                "Got it! Here is the results I found:"
                            ]
                        }
                    }
                ],
            }

            # for r in response[:10]:
            for r in response:
                res["fulfillmentMessages"].append(
                    {
                        "platform": "FACEBOOK",
                        "card": {
                            "title": r[0],
                            "subtitle": "This recipe uses: " + ",".join(r[-1]),
                            "imageUri": r[1],
                            "buttons": [
                                {
                                        "text": "go to recipe",
                                        "postback": r[2],
                                }
                            ]
                        }
                    }
                )

            res["fulfillmentMessages"].append(
                {
                    "platform": "FACEBOOK",
                    "text": {
                        "text": [
                                "If you would like to see video recipes, type 'video'"
                        ]
                    }
                }
            )
        # no result found
        else:
            res = {
                "fulfillmentText": "Sorry, couldn't find the recipe... \n please check if there is any typos and try again!",
                "fulfillmentMessages": [
                    {
                        "platform": "FACEBOOK",
                        "text": {
                            "text": [
                                "Sorry, couldn't find the recipe... \n please check if there is any typos and then try again!"
                            ]
                        }
                    }
                ],
            }

        return res

    # def random_recipe_response(self):

# test call #######################################
# r = Recipe()
# r.ingredients.append("apple")
# r.ingredients.append("banana")
# result = r.get_search_result()

# print(result)

# # print(len(result))
# for r in result:
#     print(r)
#     print()
