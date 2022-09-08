import configparser
import json
import asyncio
import requests

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from telethon import connection
from telethon import functions, types

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import CheckChatInviteRequest

from req import use_requests

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
my_channel = config['Telegram']['my_channel']
node_url = config['Telegram']['node_url']

urls = [-1001671510699, -1001678266292, -1001674535071]

client = TelegramClient(username, api_id, api_hash)

#channel = await client(functions.messages.CheckChatInviteRequest(hash = "W-C6i5Co-7I5ZTk6")).chat


class Post:
    def __init__(self, channelId, channelTitle, text, author, datetime):
        self.channelId = channelId
        self.channelTitle = channelTitle
        self.text = text
        self.author = author
        self.datetime = datetime


@client.on(events.NewMessage(chats=urls))
async def handler_new_message(event):
    try:
        #await client.send_message(my_channel, event.message)
        # if "js" in event.raw_text or "Js" in event.raw_text or "JS" in event.raw_text:
        res = None
        res = await client.forward_messages(my_channel, event.message)
        print("====== POST START ====== ")


        channelId = str(event.peer_id)

        ch = '='

        channelConstId = '-100'
        channelId = channelConstId + \
            channelId.split(ch, 1)[1].rstrip(channelId[-1])

        channelFull = await client(functions.channels.GetFullChannelRequest(channel=int(channelId)))
        channelTitle = str(channelFull)
        start = "title='"
        end = "'"
        channelTitle = channelTitle.split(start, 1)[1].split(end, 1)[0]
        text = str(event.raw_text)
        author = str(event.post_author)
        datetime = str(event.date)

        # разница во времени с Минском 3 часа

        # datetime = str(event.date + timedelta(hours=3))


        p = Post(channelId, channelTitle, text, author, datetime)
        print("Channel id: ")
        print(p.channelId)
        print("Channel title: ")
        print(p.channelTitle)
        print("Message text: ")
        print(p.text)
        print("Post author: ")
        print(p.author)
        print("Date time: ")
        print(p.datetime)
        print("====== POST END ====== ")
        # Data to be written
        dictionary = {

            "id": channelId,

            "message": channelTitle,

            "channel": author,

            "text": text,

            "date": datetime

        }
        # Serializing json
        json_object = json.dumps(dictionary, indent=5, ensure_ascii=False)
        if res is not None:
            await use_requests(node_url, {"message": channelTitle, "channel": author, "time": datetime})

    except Exception as e:
        print(e)

# async def redirect_messages(channel):
# 	await client.send_message(entity = my_channel, message = 'working')


# async def main(interval = 1):
# 	while True:
# 		channel = await client.get_entity(url)
# 		await redirect_messages(channel)
# 		await asyncio.sleep(interval)

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()

