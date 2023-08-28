import json

from channels.generic.websocket import AsyncWebsocketConsumer


class FileCheckConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'file_check',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'file_check',
            self.channel_name
        )

    async def task_started(self, event):
        await self.send(text_data=json.dumps({
            'type': 'task_started',
            'task_id': event['task_id'],
        }))

    async def task_finished(self, event):
        await self.send(text_data=json.dumps({
            'type': 'task_finished',
            'task_id': event['task_id'],
            'result': event['result'],
        }))
