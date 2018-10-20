from settings import get_keys

# from oauth2client.tools import argparser
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_KEY = get_keys("YOUTUBE_KEY")


class YouTube():
    def __init__(self):
        self.video_link_head = "https://www.youtube.com/watch?v="
        self.max_results = 10
        self.qstring = ""

    def add_query(self, ingredients):
        for i in ingredients:
            self.qstring += i + "+"

        self.qstring += "recipe"

    def youtube_search(self, order="relevance", token=None, location=None, location_radius=None):

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_KEY)

        search_response = youtube.search().list(
            q=self.qstring,
            type="video",
            pageToken=token,
            order=order,
            part="id,snippet",  # Part signifies the different types of data you want
            maxResults=self.max_results,
            location=location,
            locationRadius=location_radius).execute()

        title = []
        links = []
        image = []
        description = []

        if not search_response:
            return self.error_message()

        for search_result in search_response.get("items", [])[:5]:
            if search_result["id"]["kind"] == "youtube#video":
                title.append(search_result['snippet']['title'])
                links.append(self.video_link_head + search_result["id"]["videoId"])
                image.append(search_result['snippet']['thumbnails']['default']['url'])
                description.append(search_result['snippet']['description'])

        # for i in range(len(title)):
        #     print(title[i])
        #     print(links[i])
        #     print(image[i])
        #     print(description[i])

        return self.response(title, links, image, description)

    def error_message(self):
        '''
        Generates the error message if there was no search result or error happens
        '''
        res = {
            "fulfillmentText": "Sorry, looks like there is no videos I can find...",
            "fulfillmentMessages": [
                {
                    "platform": "FACEBOOK",
                    "text": {
                        "text": [
                                "Sorry, looks like there is no videos I can find..."
                        ]
                    }
                }
            ]
        }
        return res

    def response(self, title, links, image, description):
        res = {
            "fulfillmentText": "Here is the youtube videos I found for recipe: ",
            "fulfillmentMessages": [
                {
                    "platform": "FACEBOOK",
                    "text": {
                        "text": [
                            "Here is the youtube videos I found for recipe: "
                        ]
                    }
                }
            ],
        }

        for i in range(len(title)):
            res["fulfillmentMessages"].append(
                {
                    "platform": "FACEBOOK",
                    "card": {
                        "title": title[i],
                        "subtitle": description[i],
                        "imageUri": image[i],
                        "buttons": [
                            {
                                "text": "go to recipe",
                                "postback": links[i],
                            }
                        ]
                    }
                }
            )

        return res


# yt = YouTube()
# yt.add_query(['apple'])
# # result = yt.get_video()
# print(yt.youtube_search())
