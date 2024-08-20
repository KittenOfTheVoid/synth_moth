import asyncio
import datetime
from dotenv import dotenv_values
from dotenv import load_dotenv
import json
import os
from PySide6.QtCore import QObject, Slot, Signal, Property
import random
import re
import requests
import threading
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from bridge import chat
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

_loop = asyncio.new_event_loop()

_thr = threading.Thread(target=_loop.run_forever, name="Async Runner",
                        daemon=True)

_turnOff = 0

class chatBotTwitch:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.config = dotenv_values(".env")
        self.isWorking = 0
        self.APP_ID = self.config['CLIENT_ID']
        self.APP_SECRET = self.config['SECRET']
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_MANAGE_SHOUTOUTS]
        self.TARGET_CHANNEL = self.config['TARGET_CHANNEL']
        self.START_TIME = datetime.datetime.now()

    async def on_ready(self, ready_event: EventData):
        print('Bot is ready for work, joining channels')
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await ready_event.chat.join_room(self.TARGET_CHANNEL)
        # you can do other bot initialization things in here


    # this will be called whenever a message in a channel was send by either the bot OR another user
    async def on_message(self, msg: ChatMessage):
        global chat
        msgText = msg.text
        msgText = strip_tags(msgText)
        chat.newChatMessage.emit(f'<font color="{msg.user.color}"><b> {msg.user.name}</b></font>: {msgText}')
        print(f'in {msg.room.name}, {msg.user.name} color: {msg.user.color} said: {msg.text}')


    # this will be called whenever someone subscribes to a channel
    async def on_sub(self, sub: ChatSub):
        print(f'New subscription in {sub.room.name}:\\n'
              f'  Type: {sub.sub_plan}\\n'
              f'  Message: {sub.sub_message}')

    # this will be called whenever someone raids your channel
    async def on_raid(self, d: dict):
        await self.chat.twitch.send_a_shoutout(d["tags"]["room-id"], d["tags"]["user-id"], d["tags"]["room-id"])

    # this will be called whenever the !reply command is issued
    async def test_command(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply('you did not tell me what to reply with')
        else:
            if random.randint(0, 100) <= 1:
                await cmd.reply(f'{cmd.user.name} -- пупсич')
            else:
                await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

    def dice_roll(self, d_q, d_s):
       ans = 0
       for i in range(d_q):
           ans += random.randint(1, d_s)
       return ans

    # this will be called whenever the !roll command is issued
    async def roll_command(self, cmd: ChatCommand):
        dice_size = 20
        dice_quant = 1
        print(cmd.parameter)
        print(len(cmd.parameter))
        if len(cmd.parameter) == 0:
            roll_result = self.dice_roll(dice_quant, dice_size)
            await cmd.reply(f'{roll_result}')
        elif len(cmd.parameter.split(" ")) != 1:
            await cmd.reply("wrong parameter, enter a positive int, dice size + quantity (format 1d20) or nothing for default 1d20")
        else:
            dices = cmd.parameter.split("d")
            if len(dices) > 2 or dices[0].isdigit() == False or (len(dices) == 2 and dices[1].isdigit() == False):
                await cmd.reply("wrong dice size + quantity, write in format 1d20, first number is dice quantity, second is dice size, both positive integers")
            if len(dices) == 1:
                dice_size = int(dices[0])
            else:
                dice_quant = int(dices[0])
                dice_size = int(dices[1])
            await cmd.reply(self.dice_roll(dice_quant, dice_size))

    async def ds_command(self, cmd: ChatCommand):
        await cmd.reply("https://discord.gg/RnpYD7vgP2")

    async def uptime_command(self, cmd: ChatCommand):
        await cmd.reply(str(datetime.datetime.now() - self.START_TIME))

    # this is where we set up the bot and start it
    async def run_bot(self):
        if self.isWorking == 1:
            return

        self.isWorking = 1

        # set up twitch api instance and add user authentication with some scopes
        self.twitch = await Twitch(self.APP_ID, self.APP_SECRET)
        auth = UserAuthenticator(self.twitch, self.USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        await self.twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)
        # create chat instance
        self.chat = await Chat(self.twitch)

        # register the handlers for the events you want
        
        # listen to when the bot is done starting up and ready to join channels
        self.chat.register_event(ChatEvent.READY, self.on_ready)
        # listen to chat messages
        self.chat.register_event(ChatEvent.MESSAGE, self.on_message)
        # listen to channel subscriptions
        self.chat.register_event(ChatEvent.SUB, self.on_sub)
        #listen to raids
        self.chat.register_event(ChatEvent.RAID, self.on_raid)
        # there are more events, you can view them all in this documentation

        # you can directly register commands and their handlers
        self.chat.register_command('reply', self.test_command)
        self.chat.register_command('roll', self.roll_command)
        self.chat.register_command('discord', self.ds_command)
        self.chat.register_command('uptime', self.uptime_command)

        print("start")
        # we are done with our setup, lets start this bot up!
        self.chat.start()

    # this is where we stop the bot
    async def stop_bot(self):
        if self.isWorking == 0:
            return
            # now we can close the chat bot and the twitch api client
        self.isWorking = 0
        self.chat.stop()
        await self.twitch.close()

def turn_on():
    global _turnOff
    _turnOff = 1

def turn_off():
    global _turnOff
    _turnOff = -1

async def run():
    global _turnOff
    twitch_chat_bot = chatBotTwitch()
    while True:
        #print("test")
        if _turnOff == 1:
            await twitch_chat_bot.run_bot()
            print("turned_on")
            _turnOff = 0
        elif _turnOff == -1:
            await twitch_chat_bot.stop_bot()
            print("turned_off")
            _turnOff = 0

def main_bot_thread():
    if not _thr.is_alive():
        _thr.start()
        asyncio.run_coroutine_threadsafe(run(), _loop)

#run_task = asyncio.create_task(run_bot())


# lets run our setup
if __name__ == "__main__":
    asyncio.run(run())
