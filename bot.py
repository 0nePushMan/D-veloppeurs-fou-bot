import os
from tabnanny import check
import threading
import discord
import base64
from googlesearch import search
import requests
import time
from datetime import date
from dotenv import load_dotenv
load_dotenv()

token = os.environ['token']
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']


class MyClient(discord.Client):
    spotify = ''
    hot = []
    found = ''
    founders = []

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

        if message.channel.id == 983752718915108934 and not message.content.isupper():
            await message.channel.send('UNIQUEMENT EN MAJUSCULES SVP')

            if message.author == self.user:
                return

        if message.channel.id == 994154345778126858 or message.channel.id == 994184781573140493:
            first = message.content.split()[0].lower()

            async def clearChannel():
                await message.channel.purge()
                return await message.channel.send('Le mot du ' + str(date.today()) + ' était ' + MyClient.found)

            async def temperature(score):
                if score <= 0:
                    return '🧊'
                if score <= 20:
                    return '🥶'
                if score <= 30:
                    return '😎'
                if score <= 40:
                    return '🥵'
                else:
                    return '🔥'

            async def req_word(word):
                r = requests.post(
                    "https://cemantix.herokuapp.com/score", data={"word": first}).json()
                print(r)
                if "error" in r and "tapez trop vite" in r["error"]:
                    time.sleep(.2)
                    return req_word(word)
                if "error" in r:
                    return False
                if "score" in r:
                    if r["score"] == 1:
                        MyClient.found = first
                        return True
                    else:
                        return r['score'] * 100

            # async def checkHot(score):
            #     if len(MyClient.hot) > 0:
            #         for index, value in MyClient.hot:
            #             if value[1] < score:
            #                 MyClient.hot[index] = [first, score, message.id]
            #                 return True
            #             else:
            #                 return False
            #     else:
            #         MyClient.hot.append([first, score, message.id])
            #         return True

            if message.content == '/clear':
                if message.author.id == 129570436278124545:
                    await clearChannel()
                return

            score = await req_word(first)

            if score == True:
                print('FOUNDERS', MyClient.founders)
                MyClient.found == first
                await message.delete()
                if len(MyClient.founders) > 0:
                    for user in MyClient.founders:
                        if user != message.author.id:
                            MyClient.founders.append(message.author.id)
                else:
                    MyClient.founders.append(message.author.id)
                if len(MyClient.founders) == 5:
                    await clearChannel()
                await message.channel.send(message.author.name + ' a trouvé le mot du jour 🔥🔥🔥')
            elif score == False:
                await message.channel.send('Je ne connais pas le mot ' + first)
            else:
                temp = await temperature(score)
                await message.channel.send(message.author.name + ' le mot ' + first + ' a une température de ' + str(round(score, 2)) + '°C  ' + temp)

        if message.channel.id == 984434964126904370 and not message.content.startswith('https'):
            try:
                if len(MyClient.spotify) == 0:
                    print('NO TOKEN')
                    MyClient.getToken()
                await message.delete()
                query = 'https://api.spotify.com/v1/search?q=' + message.content + '&type=track'
                results = requests.get(query, headers={
                    'Authorization': 'Bearer ' + MyClient.spotify, "Accept": "application/json", "Content-Type": "application/json"}).json()
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
