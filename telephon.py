import asyncio

from dotenv import load_dotenv
load_dotenv()
import telethon, os
from telethon import TelegramClient
from qrcode import QRCode
from base64 import urlsafe_b64encode as base64url

qr = QRCode()

def gen_qr(token:str):
    qr.clear()
    qr.add_data(token)
    qr.print_ascii()
def display_url_as_qr(url):
    print(url)  # do whatever to show url as a qr to the user
    gen_qr(url)

class Client():
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')

    def __init__(self, phone: str):
        self._client: telethon.TelegramClient = TelegramClient(phone,
                                                               self.TELEGRAM_API_ID,
                                                               self.TELEGRAM_API_HASH)
        self._state = 'not connected'
        self._qr_link=None

    @property
    def qr_link(self):

        return self._qr_link
    @qr_link.setter
    def qr_link(self,link):
        self._qr_link=link

    @property
    def state(self):
        return self._state
        ...
    @state.setter
    def state(self,st):
        self._state=st

    async def login(self):
        await self._client.connect()
        if  self._client.is_connected():
            print(self._client.is_user_authorized())
            self.state='connected'
            return
        qr_login = await self._client.qr_login()
        isLogin=False
        while not isLogin:
            self.qr_link = qr_login.url
            display_url_as_qr(self.qr_link)
            try:
                isLogin = await qr_login.wait(10)
            except:
                await qr_login.recreate()
        print('connected')


    async def get_message(self, uname: str, count: int = 50):
        if  self._client.is_connected():
            for dialog in self._client.iter_dialogs():
                if dialog.is_channel:
                    print(f'{dialog.id}:{dialog.title}')
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
c=Client('a')


