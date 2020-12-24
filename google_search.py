############################################
# Using Google API: Custom Search JSON API #
# Programmable Search Engine               #
############################################

import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()  # loads values from env file

API_KEY = os.getenv('API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')


def search(query):

    # service object for interacting with the API
    service = build("customsearch", "v1",
                    developerKey=API_KEY)

    res = service.cse().list(
        q=query,
        cx=SEARCH_ENGINE_ID,
    ).execute()

    # Handles if no result is found
    try:
        items = res["items"]
        top_five_links = []
        for i in items:
            if(len(top_five_links) < 5):
                top_five_links.append(i["link"])
        return top_five_links
    except:
        return
