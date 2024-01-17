import asyncio
import logging

from dotenv import load_dotenv


import telethon, os
from telethon import TelegramClient
from threading import Thread

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
assert TELEGRAM_API_ID , 'TELEGRAM_API_ID not found'
assert TELEGRAM_API_HASH , 'TELEGRAM_API_HASH not found'




class Client(Thread):


    def __init__(self, phone: str):
        super().__init__(daemon=True)
        self._client: telethon.TelegramClient = None
        self._phone = phone
        self._state = 'not connected'
        self._qr_link = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, st):
        self._state = st

    def get_qr(self):
        while True:
            if self._qr_link:
                return self._qr_link.url

    def run(self):
        loop = asyncio.new_event_loop()  # новый луп в паток для карутин
        asyncio.set_event_loop(loop)
        self._client = TelegramClient(self._phone, TELEGRAM_API_ID,
                                      TELEGRAM_API_HASH, loop=loop)

        async def ase():  # функция для ожидания логина по qr и пересоздание по истечению
            if (not self._client.is_connected()):
                await self._client.connect()
                print(await self._client.get_me())
            self._client.connect()
            self._qr_link = await self._client.qr_login()
            isLogin = False
            while not isLogin:
                if self.qr_link:
                    try:
                        isLogin = await self._qr_link.wait(10)
                    except:
                        await self._qr_link.recreate()
            self.state = 'connected'
            self.join()

        self._client.loop.run_until_complete(ase())

    async def get_message(self, uname: str, count: int = 50):
        if self._client.is_connected():
            try:
                entity = await self._client.get_entity(uname)
                return await self._client.get_messages(entity, limit=count)
            except TypeError:
                return 'bad chat'
            except Exception:
                return 'error'
        else:
            return {'error': 'login filed'}

    def send_message(self, uname, text):
        if self._client.is_connected():
            try:
                entity = self._client.get_entity(uname)
                self._client.send_message(entity=entity, message=text)
                return 'ok'
            except TypeError:
                return 'bad chat'
            except Exception:
                return 'error'
        else:
            return 'login filed'
