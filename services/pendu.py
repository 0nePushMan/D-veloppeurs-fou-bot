import random
import re
from services.service import Service

words = open('../liste_francais.txt', 'r').read().split('\n')
EMOJIS = ['👶','🧒','👨‍🦱','👨🏼‍🏫','🧔','👨‍💼','👬','👪','👴','😷','🏥','💀']

class Pendu(Service):
    max_tries = 12

    def __init__(self):
        self.reset()

    def reset(self):
        self.choosen_word = ''
        self.guess_word = ''
        self.tries = []
        self.has_ended = False
        self.choosen_word = random.choice(words).lower()
        for index, char in enumerate(self.choosen_word):
            if index == 0 or char == "'" or char == "-":
                self.guess_word += char
            else:
                self.guess_word += '_'

    async def handle_message(self, bot_user, message):
        if message.author == bot_user:
            return
        if message.content.startswith('!play') and self.has_ended:
            self.reset()
            await self.print_guess(message, "Nouvelle partie :")
        elif message.content.startswith('!play'):
            await message.channel.send('Une partie est déjà en cours')
            await self.print_guess(message)
        elif message.content.startswith('!tries'):
            await self.print_tries(message)
        elif message.content.startswith('!guess'):
            await self.print_guess(message)
        elif not message.content.startswith('!'):
            await self.play(message)
    
    async def print_guess(self, message, prefix=""):
        await message.channel.send(prefix +' `'+' '.join(self.guess_word)+'`')
        
    async def play(self, message):
        if self.has_ended:
            await message.channel.send('This session has already ended. Call !play to start a new one.')
            return
        value = message.content
        author = message.author.name
        if value in self.tries:
            # Déjà essayé, on ne fait rien
            await message.channel.send("Déjà essayé")
            return
        if len(value) == 1:
            if value in self.guess_word[1:]:
                await message.channel.send("Déjà essayé")
                return
            # On essaie une lettre
            if value in self.choosen_word:
                indices = [i.start() for i in re.finditer(value, self.choosen_word)]
                for index in indices:
                    self.guess_word = self.guess_word[:index] + value + self.guess_word[index+1:]
                await self.print_guess(message, "Valeur correcte")
                await self.check_win(author, message)
            else:
                self.tries.append(value)
                await self.handle_error(author, message, value)
        else :
            if value == self.choosen_word:
                self.guess_word = self.choosen_word
                await self.print_guess(message, "Valeur correcte")
                await self.check_win(author, message)
            else:
                self.tries.append(value)
                await self.handle_error(author, message, value)
                
    async def check_win(self, author, message):
        if self.guess_word == self.choosen_word:
            await message.channel.send("Félicitations, vous avez trouvé le mot " + self.choosen_word + " 🎉🎉🎉")
            await self.end_game(message)
        return
            
    async def handle_error(self, author, message, value):
        tries_left = self.max_tries - len(self.tries)
        await message.channel.send("Valeur incorrecte : " + value + " " + EMOJIS[len(self.tries) - 1])
        if tries_left == 0:
            await message.channel.send("Vous avez épuisé vos chances, le mot était `" + self.choosen_word +"`")
            await self.end_game(message)
    
    async def end_game(self, message):
        self.has_ended = True
        await message.channel.send("Fin du Jeu")

    async def print_tries(self, message):
        tries_left = self.max_tries - len(self.tries)
        await message.channel.send("Il vous reste "+str(tries_left)+" essai(s)\nVous avez essayé : " + ', '.join(self.tries))

    

if __name__ == "__main__":
    pendu = Pendu()
    print(pendu.choosen_word)
    print(pendu.guess_word)
