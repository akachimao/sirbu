#import re
import os
import discord
import requests
import json
import random
import youtube_dl
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException




starter_animated_movies = ["Song of the Sea", "The Breadwinner", "Wolfwalkers", "The Secret of Kell", "Spirited Away", "The Secret World of Arrietty", "Mei and the Kitten Bus", "Soul", "Coraline", "Old Fangs",
                           "WALL-E", "Your Name", "Fantastic Mr. Fox", "How to Train Your Dragon", "The Hunchback of Notre Dame", "Spider-Man: Into the Spider-Verse", "The Iron Giant", "Up!", "Shrek", "Rango", "Ratatouille"]
starter_movies = ["A Quiet Place", "The Lord of the Rings", "Star Wars",
                  "The Hobbit", "Before I Wake", "Pan's Labyrinth", "12 Years a Slave"]
starter_bujor_quotes = ["Boom Kiss! :*", "Mirosi a primavara!"]


bad_words = ["bad word"]

response_list = ["Nu mai vorbeste asa!",
                 "Maaaaaaaaaaaaaai! ... Nu mai vorbeste urat!"]


commands_list = ["$inspire" , "$what animation should i watch?" , "$what movie should i watch?" ,
                "$bye" , "$bujor" , "$hello" , "$what do you do?" , "$what do i know?" , "$who is your creator?" , "$what is the ideea behind your name?" , "$how old is your creator?" ,
                 "$what does your creator like?" , "$what do you like to do?" , "$how do you feel?" , "$store_animation" , "$store_movie"]


known_list = ["Who made me?" , "What is the ideea behind my name?" , "How old is my creator?" , "What does my creator like?" , "What do i like to do?" , "How do i feel?"]
feels = ["I am doing great at the moment!" , "I am fine , thanks for asking!"]

#client = discord.Client()
client = commands.Bot(command_prefix="$")  # intents=discord.Intents.all())


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


@client.event
async def on_ready():
    print('{0.user} e gata de actiune!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    username = str(message.author).split('#')[0]
    user_message = str(msg)
    channel = str(message.channel.name)
    new_animation_list = starter_animated_movies.copy()
    new_movie_list = starter_movies.copy()

    print(f'{username}:{user_message}({channel})')

    if user_message.lower() == '$commands':
        await message.channel.send(commands_list)

    if user_message.lower() == '$inspire':
        quote = get_quote()
        await message.channel.send(quote)

    if user_message.lower() == ('$what animation should i watch?'):
        await message.channel.send(random.choice(new_animation_list))

    if user_message.lower() == ('$what movie should i watch?'):
        await message.channel.send(random.choice(new_movie_list))

    if user_message.lower() == ('$bye'):
        await message.channel.send(f'Cheaw {username}!')

    if user_message.lower() == ('$bujor'):
        await message.channel.send(random.choice(starter_bujor_quotes))

    if user_message.lower() == ('$hello'):
        await message.channel.send(f'Te salut {username}!')

    if user_message.lower() == ('$what do you do?'):
        await message.channel.send("I can respond to command messages (type $commands to see the commands list) , i can find specific words and have a custom response to them , i can randomly choose an element from a list and append other elements in that list and i'm currently learning to play music in voice chat and send gifs to text chat")

    if user_message.lower() == ('$what do i know?'):
        await message.channe.send(known_list)

    if user_message.lower() == ('$who is your creator?' or '$who made you?'):
        await message.channel.send('My creator is Sirbu Mihai-Alexandru.')

    if user_message.lower() == ('$what is the ideea behind your name?'):
        await message.channel.send('Totoro comes from a japanese animated movie written and directed by Hayao Miyazaki and animated by Studio Ghibli. Totoro is a fantasy bear-like animal.')

    if user_message.lower() == ('$how old is your creator?'):
        await message.channel.send('My creator is 17 years old.')

    if user_message.lower() == ('$what does your creator like?'):
        await message.channel.send('My creator likes art , video games , animations , long walks , good conversation , Catalina and books')
        
    if user_message.lower() == ('$what do you like to do?'):
        await message.channel.send('I love interacting and helping humans via discord chat.')

    if user_message.lower() == ('$how do you feel?'):
        await message.channel.send(random.choice(feels))    

    if message.content.startswith('$store_animation'):
        adaugare_in_lista = str(message.content[17:])
        await message.channel.send("Stored!")
        new_animation_list.append(adaugare_in_lista)
        print(new_animation_list)

    if message.content.startswith('$store_movie'):
        adaugare_in_lista = str(message.content[13:])
        await message.channel.send("Stored!")
        print(new_movie_list)
        new_movie_list.append(adaugare_in_lista)
        print(new_movie_list)


    # cauta cuvinte in mesage si daca sunt in lista data raspunde cu ceva
    if any(word in msg for word in bad_words):
        await message.channel.send(random.choice(response_list))
        

# nu functioneaza


@client.command()
async def gif(ctx, *, q="random"):

    api_key = "ABUOMyrBuMwRoNqCiTzV6xJzpxsZMnDL"
    api_instance = giphy_client.DefaultApi()

    try:

        api_response = api_instance.gifs_search_get(
            api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)

    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

#welcome!
@client.event
async def on_member_join(member):
    guild = client.get_guild(975472361363107840)
    channel = guild.get_channel(976421550783885322)
    await channel.send(f'Welcome to the server {member.mention} ! :patying_face:')


TOKEN = ('OTc1NzM2ODIwMTM2NTYyNzg4.G21AE6.-mzdXlzAcBFlR4dvuD_WmLi4S3RcpqaD-_VvpA')
# client.run(os.getenv('TOKEN'))
client.run(TOKEN)
