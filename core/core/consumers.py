import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from SwadeshChat.models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_slug']
        self.roomGroupName = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["message"]
        sender = text_data_json["sender"]
        group_name = text_data_json["room_name"]

        await self.save_message(content, sender, group_name)

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": content,
                "username": sender,
                "room_name": group_name,
            }
        )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))

    @sync_to_async
    def save_message(self, content, sender, group_name):
        user = User.objects.get(username=sender)
        Message.objects.create(content=content, sender=user, slug=group_name)
