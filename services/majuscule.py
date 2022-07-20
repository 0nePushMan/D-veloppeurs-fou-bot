from services.service import Service

class Majuscule(Service):
    async def handle_message(self, bot_user, message):
        if message.author == bot_user:
            return
        await message.channel.send('UNIQUEMENT EN MAJUSCULES SVP')
