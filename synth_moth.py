
from PySide6.QtCore import QObject, Slot, Signal

import threading

import sys
import asyncio
import datetime
import json
import os
import random
import re
import requests
from html.parser import HTMLParser
from io import StringIO
from PySide6.QtCore import QObject, Signal, Slot, QUrl, Property
from PySide6.QtWidgets import QApplication

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.chat import Chat, ChatEvent, EventData, ChatSub, ChatCommand, ChatMessage
from twitchAPI.type import AuthScope
from twitchAPI.helper import first

_loop = None
_loop_thread = None

def ensure_async_loop():
    global _loop, _loop_thread
    if _loop is not None:
        return _loop

    _loop = asyncio.new_event_loop()

    def run_loop():
        asyncio.set_event_loop(_loop)
        _loop.run_forever()

    _loop_thread = threading.Thread(target=run_loop, name="TwitchAsyncLoop", daemon=True)
    _loop_thread.start()
    return _loop

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

class TwitchChatBot(QObject):
    banUser = Signal(str, int)           # user: str, duration_seconds: int
    botStatusChanged = Signal(bool)      # true = запущен, false = остановлен
    messageReceived = Signal(str, str, str) # username, message, user_color

    def __init__(self, app_id: str, app_secret: str, target_channel: str):
        super().__init__()
        self.APP_ID = app_id
        self.APP_SECRET = app_secret
        self.TARGET_CHANNEL = target_channel.lower()

        self.USER_SCOPE = [
            AuthScope.CHAT_READ,
            AuthScope.CHAT_EDIT,
            AuthScope.MODERATOR_MANAGE_SHOUTOUTS,
            AuthScope.MODERATOR_MANAGE_BANNED_USERS,
            AuthScope.CHANNEL_MODERATE,
        ]

        self.twitch: Twitch | None = None
        self.chat: Chat | None = None
        self._isWorking = False
        self.START_TIME: datetime.datetime | None = None

        ensure_async_loop()
        # Подключаем сигнал бана
        self.banUser.connect(self.on_ban)

    # ====================== Свойство для QML ======================
    @Property(bool, notify=botStatusChanged)
    def isWorking(self):
        return self._isWorking

    def _set_working(self, value: bool):
        if self._isWorking != value:
            self._isWorking = value
            self.botStatusChanged.emit(value)
    
    # ====================== Слоты для вызова из QML ======================
    @Slot()
    def startBot(self):
        """Вызывается из QML кнопкой "Запустить бота" """
        if self._isWorking:
            print("Бот уже запущен")
            return

        loop = ensure_async_loop()
        asyncio.run_coroutine_threadsafe(self._start_bot_internal(), loop)

    @Slot()
    def stopBot(self):
        """Вызывается из QML кнопкой "Остановить бота" """
        if not self._isWorking:
            print("Бот уже остановлен")
            return
        
        loop = ensure_async_loop()
        asyncio.run_coroutine_threadsafe(self._stop_bot_internal(), loop)

    # ====================== Бан из GUI ======================
    @Slot(str, int)
    def on_ban(self, user: str, duration: int):
        user = strip_tags(user).strip()
        if not user or not self._isWorking or not self.twitch:
            return

        async def do_ban():
            try:
                # Получаем ID пользователя, которого баним
                user_to_ban = await first(self.twitch.get_users(logins=[user]))
                if not user_to_ban:
                    print(f"Пользователь {user} не найден")
                    return

                # Получаем ID канала (broadcaster)
                broadcaster = await first(self.twitch.get_users(logins=[self.TARGET_CHANNEL]))
                
                # Получаем ID модератора (бота)
                moderator = await first(self.twitch.get_users())   # текущий авторизованный пользователь

                if duration > 0:
                    # Таймаут
                    await self.twitch.ban_user(
                        broadcaster_id=broadcaster.id,
                        moderator_id=moderator.id,
                        user_id=user_to_ban.id,
                        duration=duration,
                        reason="Banned from SynthMoth"
                    )
                    print(f"✅ Таймаут {user} на {duration} сек")
                else:
                    # Перманентный бан
                    await self.twitch.ban_user(
                        broadcaster_id=broadcaster.id,
                        moderator_id=moderator.id,
                        user_id=user_to_ban.id,
                        reason="Banned from SynthMoth"
                    )
                    print(f"✅ Бан {user} выполнен")

            except Exception as e:
                print(f"❌ Ошибка бана {user}: {e}")
                self.botError.emit(str(e))

        loop = ensure_async_loop()
        asyncio.run_coroutine_threadsafe(do_ban(), loop)

    # ====================== Внутренний запуск ======================
    async def _start_bot_internal(self):
        try:
            print("Запуск Twitch чат-бота...")

            self.twitch = await Twitch(self.APP_ID, self.APP_SECRET)

            auth = UserAuthenticator(self.twitch, self.USER_SCOPE)
            token, refresh_token = await auth.authenticate()
            await self.twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)

            self.chat = await Chat(self.twitch)

            # Регистрация событий
            self.chat.register_event(ChatEvent.READY, self.on_ready)
            self.chat.register_event(ChatEvent.MESSAGE, self.on_message)
            self.chat.register_event(ChatEvent.SUB, self.on_sub)
            self.chat.register_event(ChatEvent.RAID, self.on_raid)

            # Пример регистрации команд (добавь свои)
            self.chat.register_command('reply', self.test_command)
            self.chat.register_command('roll', self.roll_command)
            self.chat.register_command('discord', self.ds_command)
            self.chat.register_command('uptime', self.uptime_command)

            self.START_TIME = datetime.datetime.now()
            self._set_working(True)

            print(f"✅ Бот запущен и присоединяется к каналу #{self.TARGET_CHANNEL}")

            # chat.start() блокирует — запускаем в отдельном потоке
            await asyncio.to_thread(self.chat.start)
        except Exception as e:
            error_msg = f"Критическая ошибка запуска бота: {e}"
            print(f"❌ {error_msg}")
            self.botError.emit(error_msg)
            await self._stop_bot_internal()

    async def _stop_bot_internal(self):
        print("Остановка бота...")
        try:
            if self.chat:
                self.chat.stop()
            if self.twitch:
                await self.twitch.close()
        except Exception as e:
            print(f"Ошибка при остановке: {e}")
        finally:
            self.chat = None
            self.twitch = None
            self.START_TIME = None
            self._set_working(False)
            print("✅ Бот остановлен")

    # ====================== Обработчики событий ======================
    async def on_ready(self, ready_event: EventData):
        print(f"Бот готов → присоединяемся к #{self.TARGET_CHANNEL}")
        await ready_event.chat.join_room(self.TARGET_CHANNEL)

    # this will be called whenever a message in a channel was send by either the bot OR another user
    async def on_message(self, msg: EventData):
        print(f"{msg}")
        print(f"{msg.user.name}: {msg.text}")
        # Здесь можно эмитировать сигналы в QML, если нужно показывать сообщенияglobal chat
        msgText = msg.text
        msgText = strip_tags(msgText)
        msgColor = msg.user.color if msg.user.color != None and msg.user.color != "None" else "#FFFFFF"
        self.messageReceived.emit(f'<font color="{msgColor}"><b>{strip_tags(msg.user.name)}</b></font>', msgText, msgColor)
        print(f'in {msg.room.name}, {msg.user.name} color: {msg.user.color} said: {msg.text}')

    async def on_sub(self, sub_event: ChatSub):
        print(f"Подписка от {sub_event.user.name}")

    async def on_raid(self, d: dict):
        #print(f"Рейд от {raid_event.user.name} ({raid_event.viewer_count} зрителей)")
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