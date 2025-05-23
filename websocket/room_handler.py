import json
import tornado.websocket
from room.actions.create_room import handle_create_room
from room.actions.get_rooms import handle_get_rooms
from room.actions.delete_room import handle_delete_room  # ← Si tu l’as
from datetime import datetime


class RoomWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        RoomWebSocketHandler.clients.add(self)

    def on_close(self):
        RoomWebSocketHandler.clients.discard(self)

    async def on_message(self, message):
        try:
            data = json.loads(message)
            action = data.get("action")
            
            print(f"[WS Room] Action reçue: {action}")

            if action == "create_room":
                new_room = await handle_create_room(data, self)
                if new_room:
                    # Envoyer confirmation au client actuel
                    await self.write_message(json.dumps({
                        "action": "room_created",
                        "room": new_room
                    }))
                    # Broadcast à tous les autres clients
                    await RoomWebSocketHandler.broadcast_to_all({
                        "action": "room_created",
                        "room": new_room
                    })
            elif action == "get_rooms":
                await handle_get_rooms(data, self)
            elif action == "delete_room":
                await handle_delete_room(data, self)
            else:
                await self.write_message(json.dumps({
                    "type": "error",
                    "message": "Action inconnue pour les rooms"
                }))

        except json.JSONDecodeError:
            await self.write_message(json.dumps({
                "type": "error",
                "message": "Format JSON invalide"
            }))
        except Exception as e:
            print(f"[WS Room] Erreur: {str(e)}")
            await self.write_message(json.dumps({
                "type": "error",
                "message": f"Erreur serveur: {str(e)}"
            }))

    def check_origin(self, origin):
        return True

    @classmethod
    async def broadcast_to_all(cls, message):
        if cls.clients:
            for client in cls.clients.copy():
                try:
                    await client.write_message(json.dumps(message))
                except Exception as e:
                    print(f"Erreur broadcast: {e}")
                    cls.clients.discard(client)
