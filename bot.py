import os
import discord
import base64
from googlesearch import search 
import requests

from dotenv import load_dotenv
load_dotenv()

token = os.environ['token']
spotify = os.environ['spotify']

print('ENV')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == '/help': 
            commands = '<#991687399224655992> /d prompt\n <#943076081999679518> /s prompt\n <#990996145637564436> /s prompt\n <#984434964126904370> prompt'
            await message.channel.send(commands)
            return

        if (message.channel.id == 943076081999679518 or message.channel.id == 990996145637564436) and message.content.startswith('/'):
            if message.content.startswith('/g'):
                await message.delete()
                results = []
                for j in search(message.content, num=10, stop=10, pause=2):
                    results.append(j)
                await message.channel.send(results[0])

        if message.channel.id == 983752718915108934 and not message.content.isupper():
            await message.channel.send('UNIQUEMENT EN MAJUSCULES SVP')

        if message.channel.id == 984434964126904370 and not message.content.startswith('https'):
            try:
                await message.delete()
                query = 'https://api.spotify.com/v1/search?q=' + message.content + '&type=track'
                results = requests.get(query, headers={
                    'Authorization': 'Bearer ' + spotify, "Accept": "application/json", "Content-Type": "application/json"}).json()
                print(results)
                await message.channel.send(results['tracks']['items'][0]['external_urls']['spotify'] + ' '+message.author.mention)
            except BaseException as err:
                print(err)
                raise

        if message.channel.id == 991687399224655992 and message.content.startswith('/'):
            await message.channel.send('Veuillez patienter quelques minutes')
            results = requests.post('https://bf.dallemini.ai/generate', json={"prompt": message.content.replace('/d', '')}, headers={
                                    "Accept": "application/json", "Content-Type": "application/json"}).json()

            with open('./pictures/' + message.content + '.png', 'wb') as fh:
                x = base64.b64decode(results['images'][0])
                fh.write(x)

            await message.channel.send(message.author.mention, file=discord.File(r'./pictures/' + message.content + '.png'))
        elif message.channel.id == 991687399224655992 and not message.content.startswith('/'):
            await message.delete()


client = MyClient()
client.run(token)
