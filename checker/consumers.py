import json

from channels.generic.websocket import AsyncWebsocketConsumer
from celery.result import AsyncResult


class FileCheckConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'file_check'
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def open_websocket(self, event):
        task_id = event['task_id']
        result = AsyncResult(task_id)
        if result.state == 'SUCCESS':
            await self.send(text_data=json.dumps({
                'type': 'task_success',
                'task_id': task_id
            }))
