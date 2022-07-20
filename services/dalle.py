from services.service import Service
import base64
import requests
import discord

class Dalle(Service):
    async def handle_message(self, bot_user, message):
        if message.author == bot_user:
            return
        await message.channel.send('Veuillez patienter quelques minutes')
        results = requests.post('https://bf.dallemini.ai/generate', json={"prompt": message.content.replace('/d', '')}, headers={
                                "Accept": "application/json", "Content-Type": "application/json"}).json()
        with open('./pictures/' + message.content + '.png', 'wb') as fh:
            x = base64.b64decode(results['images'][0])
            fh.write(x)
        await message.channel.send(message.author.mention, file=discord.File(r'./pictures/' + message.content + '.png'))