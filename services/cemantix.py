from services.service import Service
import time
import requests
from datetime import date

class Cemantix(Service):
    found = ""
    founders = []
    # def __init__(self):
    
    async def clearChannel(self, message):
        await message.channel.purge()
        return await message.channel.send('Le mot du ' + str(date.today()) + ' était ' + self.found)
    def temperature(self, score):
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
    async def req_word(self, word):
        r = requests.post(
            "https://cemantix.herokuapp.com/score", data={"word": word}).json()
        print(r)
        if "error" in r and "tapez trop vite" in r["error"]:
            time.sleep(.2)
            return self.req_word(word)
        if "error" in r:
            return False
        if "score" in r:
            if r["score"] == 1:
                self.found = word
                return True
            else:
                return r['score'] * 100

    async def handle_message(self, bot_user, message):
        if message.author == bot_user:
            return
        first = message.content.split()[0].lower()
        if message.content == '/clear':
            if message.author.id == 129570436278124545:
                await self.clearChannel(message)
            return
        score = await self.req_word(first)
        if score == True:
            self.found == first
            await message.delete()
            if len(self.founders) > 0:
                for user in self.founders:
                    if user != message.author.id:
                        self.founders.append(message.author.id)
            else:
                self.founders.append(message.author.id)
            if len(self.founders) == 5:
                await self.clearChannel()
            await message.channel.send(message.author.name + ' a trouvé le mot du jour 🔥🔥🔥')
        elif score == False:
            await message.channel.send('Je ne connais pas le mot ' + first)
        else:
            temp = self.temperature(score)
            await message.channel.send(message.author.name + ' le mot ' + first + ' a une température de ' + str(round(score, 2)) + '°C  ' + temp)