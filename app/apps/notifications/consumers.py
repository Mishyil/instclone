from channels.generic.websocket import AsyncWebsocketConsumer
import json
import redis
from django.conf import settings


# Redis client instance for interacting with the Redis server
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=3)

class NotificationConsumer(AsyncWebsocketConsumer):
	"""
	The NotificationConsumer class is responsible for transmitting information
	about new notifications via WebSocket.

	Each time a user visits a page on the site, a WebSocket connection is established.

	Additionally, a unique record is created in the Redis database based on the user's ID.
	
	Subsequently, information about new notifications will be sent based on this record.

	Only the fact of the notification is transmitted, not its details (this is used only
	for updating the unread notifications counter).
	
	"""

	async def connect(self):
		# Establish a WebSocket connection when a user connects
		user = self.scope['user']
		# Store the channel name in Redis for the user
		redis_client.set(f"user_{user.id}_channel", self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		# Close the WebSocket connection when a user disconnects
		user = self.scope['user']
		# Remove the channel name from Redis for the user
		redis_client.delete(f"user_{user.id}_channel")

	async def new_notification(self, event):
		# Send a new_notification event to the WebSocket client
		await self.send(text_data=json.dumps(
			{
				'type': 'new_notification'
			}
		))
