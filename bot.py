###############################################
# This is the main file that contains all the #
# functionalities related to the discord bot  #
###############################################

import discord
from dotenv import load_dotenv
import os
from db import post_search_data, get_search_data
from google_search import search

load_dotenv()  # loads values from env file

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} with id: {client.user.id} is connected!')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # Initial Hey
    if message.content.startswith('hi'):
        msg = 'Hey {0.author.mention}'.format(message)
        await message.channel.send(msg)

    # Search functionality: Search for query using www.google.com
    if message.content.startswith('!google'):
        query = message.content.split(None, 1)[1]
        author_id = message.author.id

        # Stores the query in the database based on user
        post_search_data(author_id, query)
        results = search(query)  # get top five search results

        # Handling for no results found
        if results:
            links = ' \n'.join(results)
            msg = 'Hello {}, you searched for {}. The top five results are: \n {}'.format(
                message.author.mention, query, links)
        else:
            msg = 'Hello {}, you searched for {}. \n Sorry, no matching links found.'.format(
                message.author.mention, query)
        await message.channel.send(msg)

    # Returns history if related query was already searched
    if message.content.startswith('!recent'):
        query = message.content.split(None, 1)[1]
        author_id = message.author.id

        # retrieve searched results from database for the user
        results = get_search_data(author_id, query)

        if(len(results) > 0):
            keywords = 'Your matching search results are: \n' + \
                ' \n'.join([x[1] for x in results])
        else:
            keywords = 'No matching results found'
        await message.channel.send(keywords)


client.run(TOKEN)
