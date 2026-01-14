import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OfficeConsumer(AsyncWebsocketConsumer):
    """Handles connections to office_{office_id} group"""
    
    async def connect(self):
        """Connect to office group"""
        self.office_id = self.scope['url_route']['kwargs']['office_id']
        self.group_name = f'office_{self.office_id}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        """Disconnect from office group"""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def queue_event(self, event):
        """Receive queue event from group"""
        await self.send(text_data=json.dumps({
            'type': event['event_type'],
            'data': event['data']
        }))


class RegionConsumer(AsyncWebsocketConsumer):
    """Handles connections to region_{region_id} group"""
    
    async def connect(self):
        """Connect to region group"""
        self.region_id = self.scope['url_route']['kwargs']['region_id']
        self.group_name = f'region_{self.region_id}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        """Disconnect from region group"""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def queue_event(self, event):
        """Receive queue event from group"""
        await self.send(text_data=json.dumps({
            'type': event['event_type'],
            'data': event['data']
        }))


class CounterConsumer(AsyncWebsocketConsumer):
    """Handles connections to counter_{counter_id} group"""
    
    async def connect(self):
        """Connect to counter group"""
        self.counter_id = self.scope['url_route']['kwargs']['counter_id']
        self.group_name = f'counter_{self.counter_id}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        """Disconnect from counter group"""
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def queue_event(self, event):
        """Receive queue event from group"""
        await self.send(text_data=json.dumps({
            'type': event['event_type'],
            'data': event['data']
        }))
