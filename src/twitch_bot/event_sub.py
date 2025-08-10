import asyncio
import json
import logging

import aiohttp
import requests
from PySide6.QtCore import QThread, Signal


class TwitchChatListener(QThread):
    new_message = Signal(str, str)  # username, message
    new_reward = Signal(str, str, str)  # reward_id, username, message

    def __init__(self, bot):
        super().__init__()

        self.bot = bot

        self.client_access_token = None
        self.channel_id = None
        self.access_token = None
        self.refresh_token = None
        self.session_id = None

    def run(self):
        asyncio.run(self.listen_twitch())

    async def listen_twitch(self):
        await self.get_client_access_token()
        await self.get_channel_id()
        await self.oauth_code_to_user_access_token()

        async with aiohttp.ClientSession() as session:
            while True:  # TODO END LOOP
                try:
                    async with session.ws_connect("wss://eventsub.wss.twitch.tv/ws", heartbeat=20) as ws:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)

                                if data.get("metadata", {}).get("message_type") == "session_welcome":
                                    session_id = data["payload"]["session"]["id"]
                                    await self.subscribe_to_chat(session, session_id)

                                elif data.get("metadata", {}).get("message_type") == "notification":
                                    event = data["payload"]["event"]

                                    username = event.get("chatter_user_name", "")
                                    text = event.get("message", {}).get("text", "")
                                    reward_id = event.get("channel_points_custom_reward_id", None)

                                    if reward_id is None:
                                        self.new_message.emit(username, text)
                                    else:
                                        self.new_reward.emit(reward_id, username, text)

                except Exception as e:
                    logging.exception(e)
                    await asyncio.sleep(5)

    async def subscribe_to_chat(self, session, session_id):
        logging.info("Subscribing")
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.bot.settings.client_id,
            "Content-Type": "application/json"
        }
        payload = {
            "type": "channel.chat.message",
            "version": "1",
            "condition": {
                "broadcaster_user_id": self.channel_id,
                "user_id": self.channel_id
            },
            "transport": {
                "method": "websocket",
                "session_id": session_id
            }
        }

        async with session.post("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers,
                                json=payload) as resp:
            data = await resp.json()
            logging.info("- Subscription faite")

    async def get_client_access_token(self):
        logging.info("Getting client access token")

        params = {
            "client_id": self.bot.settings.client_id,
            "client_secret": self.bot.settings.client_secret,
            "grant_type": "client_credentials"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://id.twitch.tv/oauth2/token", params=params) as resp:
                data = await resp.json()
                self.client_access_token = data["access_token"]
                logging.info(f"- Client access token : {self.client_access_token}")

    async def oauth_code_to_user_access_token(self):
        logging.info("Fetching user access token from oauth code")

        params = {
            "client_id": self.bot.settings.client_id,
            "client_secret": self.bot.settings.client_secret,
            "code": self.bot.oauth_code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://localhost:9555"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://id.twitch.tv/oauth2/token", params=params) as resp:
                data = await resp.json()

                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                logging.info(f"- Found access_token {self.access_token}")
                logging.info(f"- Found refresh_token {self.refresh_token}")

    async def get_channel_id(self):
        logging.info("Fetching channel id")

        headers = {
            "Authorization": "Bearer " + self.client_access_token,
            "Client-Id": self.bot.settings.client_id,
            "Content-Type": "application/json"
        }
        params = {
            "login": "philaeux"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.twitch.tv/helix/users", headers=headers, params=params) as resp:
                data = await resp.json()
                self.channel_id = data["data"][0]["id"]
                logging.info(f"- Found channel_id {self.channel_id}")

    def create_event_sub_subscription(self):
        logging.info("Creating event sub")

        url = "https://api.twitch.tv/helix/eventsub/subscriptions"

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Client-Id": self.bot.settings.client_id,
            "Content-Type": "application/json"
        }
        data = {
            "type": "channel.chat.message",
            "version": "1",
            "condition": {
                "broadcaster_user_id": self.channel_id,
                "user_id": self.channel_id
            },
            "transport": {
                "method": "websocket",
                "session_id": self.session_id
            }
        }
        response = requests.post(url, json=data, headers=headers)
        logging.info(response.json())
