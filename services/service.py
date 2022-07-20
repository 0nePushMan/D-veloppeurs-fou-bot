from abc import ABC, abstractmethod

class Service(ABC):
    @abstractmethod
    async def handle_message(self, bot_user, message):
        pass