import configparser
import json
import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import CheckChatInviteRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
my_channel = config['Telegram']['my_channel']

urls = [-1001671510699, -1001678266292, -1001674535071]

client = TelegramClient(username, api_id, api_hash)

#channel = await client(functions.messages.CheckChatInviteRequest(hash = "W-C6i5Co-7I5ZTk6")).chat

@client.on(events.NewMessage(chats=urls))
async def handler_new_message(event):
    try:
        #await client.send_message(my_channel, event.message)
        #if "js" in event.raw_text or "Js" in event.raw_text or "JS" in event.raw_text:
        await client.forward_messages(my_channel, event.message)
    except Exception as e:
        print(e)

async def redirect_messages(channel):
	await client.send_message(entity = my_channel, message = 'working')


async def main(interval = 1):
	while True:
		channel = await client.get_entity(url)
		await redirect_messages(channel)
		await asyncio.sleep(interval)

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
