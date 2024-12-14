import subprocess
from microservice_core.microservices import *

import asyncio
import os
from user_manager import UserManager
from key_manager import KeyManager


import django


# Установите настройки Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/userservice')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userservice.settings')
django.setup()

async def start_django_server():
    process = subprocess.Popen(['python', 'userservice/manage.py', 'runserver', '0.0.0.0:8000'])
    await asyncio.sleep(2)
    return process

class Server(BaseServer):
    class ClientHandler(AbstractClientHandler):
        async def handle(self):
            user_manager = self.server.user_manager
            key_manager = self.server.key_manager
            while True:
                msg = await self.recv_msg()

                if msg is None:
                    break

                if msg['header']['command'] == "get_or_create":
                    response = await user_manager.get_or_create(msg['body'])
                elif msg['header']['command'] == "delete_user_internal":
                    response = await user_manager.delete_user_internal(msg['body'])
                elif msg['header']['command'] == "get_user_info_internal":
                    response = await user_manager.get_user_info_internal(msg['body'])
                elif msg['header']['command']== "get_all_users":
                    response = await user_manager.get_all_users(msg['body'])
                elif msg['header']['command'] == "update_user_internal":
                    response = await user_manager.update_user_internal(msg['body'])

                elif msg['header']['command'] == "add_key":
                    response = await key_manager.add_key(msg['body'])
                elif msg['header']['command']== "add_key_internal":
                    response = await key_manager.add_key(msg['body'])
                elif msg['header']['command']== "get_key_internal":
                    response = await key_manager.get_key_internal(msg['body'])
                elif msg['header']['command']== "list_keys":
                    response = await key_manager.list_keys(msg['body'])
                elif msg['header']['command']== "list_keys_internal":
                    response = await key_manager.list_keys_internal(msg['body'])
                elif msg['header']['command']== "delete_key":
                    response = await key_manager.delete_key(msg['body'])
                elif msg['header']['command']== "update_key":
                    response = await key_manager.update_key(msg['body'])

                elif msg['header']['command']== "get_exchanges":
                    response = await key_manager.get_exchanges(msg['body'])

                else:
                    response = {"status": "error", "message": "Неизвестная команда."}
                await self.send_msg(response)

    def __init__(self, host, port):
        super().__init__(host, port)
        self.user_manager = UserManager()
        self.key_manager = KeyManager()
        asyncio.run(start_django_server())
