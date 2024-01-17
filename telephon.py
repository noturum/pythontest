import asyncio

from dotenv import load_dotenv

load_dotenv()
import telethon, os
from telethon import TelegramClient
from qrcode import QRCode
from base64 import urlsafe_b64encode as base64url

from threading import Thread


def qr(url):
    qr = QRCode()
    qr.clear()
    qr.add_data(url)
    qr.print_ascii()


class Client(Thread):
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')

    def __init__(self, phone: str):
        super().__init__(daemon=True)
        self._client: telethon.TelegramClient = TelegramClient(phone,
                                                               self.TELEGRAM_API_ID,
                                                               self.TELEGRAM_API_HASH)
        self._state = 'not connected'
        self._qr_link = None

    @property
    def qr_link(self):

        return self._qr_link

    @qr_link.setter
    def qr_link(self, link):
        self._qr_link = link

    @property
    def state(self):
        return self._state
        ...

    @state.setter
    def state(self, st):
        self._state = st

    async def get_qr(self):
        if (not self._client.is_connected()):
            await self._client.connect()
            print(await self._client.get_me())
        self._client.connect()
        self._qr_link = await self._client.qr_login()
        return self._qr_link.url

    def run(self):
        async def ase():

            isLogin = False
            while not isLogin:
                with open('2.txt', 'a') as f:
                    f.writelines('1')
                try:
                    isLogin = await self._qr_link.wait(1)
                except:
                    await self._qr_link.recreate()
            self.state = 'connected'
        loop=asyncio.new_event_loop()
        loop.run_until_complete(ase())


    async def get_message(self, uname: str, count: int = 50):
        if self._client.is_connected():
            print(self._client.is_connected())
            entity = await self._client.get_entity(uname)
            print(entity)
            return await self._client.get_messages(entity, limit=count)
        else:
            return {'error': 'login filed'}

    def send_message(self, uname, text):
        if self._client.is_connected():
            try:
                entity = self._client.get_entity(uname)
                self._client.send_message(entity=entity, message=text)
                return 'ok'
            except Exception:
                return 'error'
        else:
            return 'login filed'
