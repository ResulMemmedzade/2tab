import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.core.cache import cache
from django.contrib.auth import get_user_model

from .models import Message, Conversation
from .tasks import send_delayed_notification


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message_text = data.get("message")

        if message_text:
            new_message = await self.save_message(
                self.user.id,
                self.conversation_id,
                message_text
            )


            await self.trigger_notification(
                self.conversation_id,
                self.user.id
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_text,
                    "sender_name": self.user.name,
                    "sender_id": self.user.id,
                    "message_id": new_message.id,
                    "created_at": new_message.created_at.strftime("%H:%M"),
                }
            )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "action": "new_message",
                "message": event["message"],
                "image_url": event.get("image_url", None),
                "sender_name": event["sender_name"],
                "sender_id": event["sender_id"],
                "message_id": event["message_id"],
                "created_at": event["created_at"],
            })
        )

    async def message_edited(self, event):
        await self.send(
            text_data=json.dumps({
                "action": "edit_message",
                "message_id": event["message_id"],
                "new_text": event["new_text"],
            })
        )

    async def message_deleted(self, event):
        await self.send(
            text_data=json.dumps({
                "action": "delete_message",
                "message_id": event["message_id"],
            })
        )

    @database_sync_to_async
    def save_message(self, user_id, conversation_id, text):
        conversation = Conversation.objects.get(id=conversation_id)
        user = User.objects.get(id=user_id)

        return Message.objects.create(
            conversation=conversation,
            sender=user,
            text=text
        )

    @database_sync_to_async
    def trigger_notification(self, conversation_id, sender_id):
        conversation = Conversation.objects.get(id=conversation_id)


        receiver = conversation.participants.exclude(
            id=sender_id
        ).first()

        if receiver:
            lock_key = f"notify_lock_{conversation_id}_{receiver.id}"

            if cache.add(lock_key, "locked", timeout=3):

                send_delayed_notification.apply_async(
                    (conversation_id, receiver.id),
                    countdown=3
                )