from tornado.websocket import WebSocketHandler
from core.services.message_service import save_message, get_messages_by_room
from core.services.room_service import save_room, get_all_rooms
from utils.format import json_serial
import json

class ChatWebSocketHandler(WebSocketHandler):
    clients = set()

    def open(self):
        print("[WS] Client connected")
        ChatWebSocketHandler.clients.add(self)

    def on_close(self):
        ChatWebSocketHandler.clients.remove(self)
        print("[WS] Client disconnected")

    async def on_message(self, message):
        print(f"[WS] Message reçu: {message}")
        try:
            data = json.loads(message)
            action = data.get("action")

            if action == "send_message":
                username = data["username"]
                content = data["message"]
                room_id = data.get("room_id", "general")

                await save_message(username, content, room_id)

                for client in ChatWebSocketHandler.clients:
                    await client.write_message(json.dumps({
                        "action": "new_message",
                        "username": username,
                        "message": content,
                        "room_id": room_id
                    }, default=json_serial))

            elif action == "create_room":
                name = data["name"]
                users = data.get("users", [])
                room_id = await save_room(name, users)

                await self.write_message(json.dumps({
                    "action": "room_created",
                    "room_id": room_id,
                    "name": name,
                    "users": users
                }, default=json_serial))

            elif action == "get_rooms":
                rooms = await get_all_rooms()
                await self.write_message(json.dumps({
                    "action": "rooms_list",
                    "rooms": rooms
                }, default=json_serial))

            elif action == "get_messages":
                room_id = data.get("room_id")
                messages = await get_messages_by_room(room_id)
                await self.write_message(json.dumps({
                    "action": "room_messages",
                    "room_id": room_id,
                    "messages": messages
                }, default=json_serial))

            else:
                await self.write_message(json.dumps({
                    "error": "Action inconnue"
                }, default=json_serial))

        except Exception as e:
            print("❌ Erreur traitement WS:", e)
            await self.write_message(json.dumps({
                "error": "Erreur serveur"
            }, default=json_serial))
