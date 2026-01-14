"""
WebSocket URL routing for queue app.
"""
from django.urls import re_path
from apps.queue.consumers import consumers

websocket_urlpatterns = [
    re_path(r'ws/office/(?P<office_id>\d+)/$', consumers.OfficeConsumer.as_asgi()),
    re_path(r'ws/region/(?P<region_id>\d+)/$', consumers.RegionConsumer.as_asgi()),
    re_path(r'ws/counter/(?P<counter_id>\d+)/$', consumers.CounterConsumer.as_asgi()),
]
