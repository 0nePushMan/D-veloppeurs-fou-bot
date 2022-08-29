import os
import threading
import discord
import base64
from googlesearch import search
import requests
import time
from dotenv import load_dotenv
from services.pendu import Pendu
from services.majuscule import Majuscule
from services.cemantix import Cemantix
from services.dalle import Dalle
from enum import Enum
load_dotenv()

token = os.environ['token']
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']

class Channels(Enum):
    Pendu = 999303816505737216
    Cemantix = 994154345778126858
    Majuscule = 983752718915108934 # Mur des lamentations
    Dalle = 991687399224655992

class MyClient(discord.Client):
    spotify = ''
    hot = []
    pendu = Pendu()
    maj = Majuscule()
    cemantix = Cemantix()
    dalle = Dalle()

    def getToken():
        d = base64.urlsafe_b64encode(
            (client_id + ':' + client_secret).encode("utf-8")).decode()
        result = requests.post('https://accounts.spotify.com/api/token', headers={
            'Authorization': 'Basic ' + d}, data={'grant_type': 'client_credentials'}, json=True).json()
        MyClient.spotify = result['access_token']

    def set_interval(func, sec):
        def func_wrapper():
            MyClient.set_interval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()

    set_interval(getToken, 3500)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        print("Channel : ", message.channel.id)

        print(Channels)
        if message.channel.id == Channels.Pendu.value:
            print("Pendu")
            await self.pendu.handle_message(self.user, message)
        elif message.channel.id == Channels.Majuscule.value:
            print("Majuscule")
            await self.maj.handle_message(self.user, message)
        elif message.channel.id == Channels.Cemantix.value:
            print("Cemantix")
            await self.cemantix.handle_message(self.user, message)
        elif message.channel.id == Channels.Dalle.value:
            print("Dalle")
            await self.dalle.handle_message(self.user, message)

        if message.content == '/help':
            commands = '<#991687399224655992> /d prompt\n <#943076081999679518> /s prompt\n <#990996145637564436> /s prompt\n <#984434964126904370> prompt'
            await message.channel.send(commands)
            return

        if (message.channel.id == 943076081999679518 or message.channel.id == 990996145637564436) and message.content.startswith('/'):
            if message.content.startswith('/g'):
                await message.delete()
                results = []
                for j in search(message.content.replace('/g', ''), num=10, stop=10, pause=2):
                    results.append(j)
                await message.channel.send(results[0])

        if message.channel.id == 984434964126904370 and not message.content.startswith('https'):
            try:
                if len(MyClient.spotify) == 0:
                    MyClient.getToken()
                await message.delete()
                query = 'https://api.spotify.com/v1/search?q=' + message.content + '&type=track'
                results = requests.get(query, headers={
                    'Authorization': 'Bearer ' + MyClient.spotify, "Accept": "application/json", "Content-Type": "application/json"}).json()
                await message.channel.send(results['tracks']['items'][0]['external_urls']['spotify'] + ' '+message.author.mention)
            except BaseException as err:
                print(err)
                raise

        
        elif message.channel.id == 991687399224655992 and not message.content.startswith('/'):
            await message.delete()


client = MyClient()
client.run(token)
