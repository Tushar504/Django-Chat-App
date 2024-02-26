import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from SwadeshChat.models import User, Message, Contact, MessageStatus, Status, Group, GroupMember


class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_slug']
        self.roomGroupName = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        if not self.scope['user'].username in self.__class__.connected_users:

            self.__class__.connected_users[self.scope['user'].username] = (self.scope['user'].username)
            await self.send_connected_users()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

        if self.scope['user'].username in self.__class__.connected_users:
            del self.__class__.connected_users[self.scope['user'].username]
            await self.send_connected_users()

    async def send_connected_users(self):

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "updateConnectedUsers",
                "reload": json.dumps({"refresh": True}),
            }
        )

    async def updateConnectedUsers(self, event):
        await self.send(text_data=json.dumps({"reload": event["reload"]}))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["message"]
        sender = text_data_json["sender"]
        group_name = text_data_json["room_name"]
        receiver_type = text_data_json["receiver_type"]

        message_status, user, read_receipt, created_at = await self.save_message(content, sender, group_name, receiver_type)

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "content": {"message": content,
                            "sender": {"username": user.username, "first_name": user.first_name, "last_name": user.last_name},
                            "room_name": group_name,
                            "read_receipt": read_receipt,
                            "created_at": str(created_at),
                            }

            }
        )

    async def sendMessage(self, event):
        content = event['content']
        await self.send(text_data=json.dumps(content))

    @sync_to_async
    def save_message(self, content, sender, group_name, receiver_type):
        user = User.objects.get(username=sender)
        message = Message.objects.create(content=content, sender=user, slug=group_name)
        message_status = {}
        read_receipt = True
        if receiver_type == "User":
            contact = Contact.objects.get(slug=group_name)

            if contact.contact_id.username in self.connected_users:
                message_stat = MessageStatus.objects.create(message=message, status=Status.objects.get(name="SEEN"), user=contact.contact_id)
            else:
                message_stat = MessageStatus.objects.create(message=message, status=Status.objects.get(name="DELIVERED"), user=contact.contact_id)

            message_status[message_stat.user.username] = {"name": message_stat.status.name, "username": message_stat.user.username}
            if message_stat.status.name == "DELIVERED":
                read_receipt = False
        else:
            group = Group.objects.get(slug=group_name)
            group_members = GroupMember.objects.filter(group=group).all()
            for group_member in group_members:
                if group_member.user != user:
                    if group_member.user.username in self.connected_users:
                        message_stat = MessageStatus.objects.create(message=message, status=Status.objects.get(name="SEEN"), user=group_member.user)
                    else:
                        message_stat = MessageStatus.objects.create(message=message, status=Status.objects.get(name="DELIVERED"), user=group_member.user)
                        if read_receipt:
                            read_receipt = False

                    message_status[message_stat.user.username] = {"name": message_stat.status.name, "username": message_stat.user.username}

        return message_status, user, read_receipt, message.created_at
