from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_20_messages()
        content = {
            'messages': self.messages_to_json(messages)
        }

    def new_message(self, data):
        print('new message')
        pass

    def messages_to_json(self, messages):
        results= []
        for message in messages:
            result.append(self.mesage_to_json(message))
        return result

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    } 

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):

        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))