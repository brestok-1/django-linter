from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from checker.tasks import check_file_errors


class YourConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            "file_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "file_group",
            self.channel_name
        )

    async def websocket_receive(self, event):
        file_id = event.get('file_id')
        result = await check_file_errors.delay(file_id)
        await self.send(text_data=result.result)
