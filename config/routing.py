"""
WebSocket URL routing for the project.
"""
from apps.queue import routing as queue_routing

websocket_urlpatterns = []
websocket_urlpatterns += queue_routing.websocket_urlpatterns