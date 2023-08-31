import json

from channels.generic.websocket import AsyncWebsocketConsumer


class FileCheckConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "file_check"

        # Присоединяемся к группе каналов
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединяемся от группы каналов
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def task_message(self, event):
        message = event['message']['message']
        result = event['message']['result']
        await self.send(text_data=json.dumps({
            'message': message,
            'result': result,
        }))


class EmailSendComsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "email_send"

        # Присоединяемся к группе каналов
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединяемся от группы каналов
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def email_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))
