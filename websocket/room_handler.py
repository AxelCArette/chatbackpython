import json
import tornado.websocket
from room.actions.create_room import handle_create_room
from room.actions.get_rooms import handle_get_rooms


class RoomWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        RoomWebSocketHandler.clients.add(self)
        print("[WS Room] Client connecté au gestionnaire de room")

    def on_close(self):
        if self in RoomWebSocketHandler.clients:
            RoomWebSocketHandler.clients.remove(self)
        print("[WS Room] Client déconnecté du gestionnaire de room")

    async def on_message(self, message):
        try:
            data = json.loads(message)
            action = data.get("action")
            
            print(f"[WS Room] Action reçue: {action}")  # Pour debug

            if action == "create_room":
                await handle_create_room(data, self)
            elif action == "get_rooms":
                await handle_get_rooms(data, self)
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
        # Permettre les connexions depuis localhost en développement
        return True

    @classmethod
    async def broadcast_to_all(cls, message):
        """Diffuse un message à tous les clients connectés"""
        if cls.clients:
            for client in cls.clients.copy():
                try:
                    await client.write_message(json.dumps(message))
                except Exception as e:
                    print(f"Erreur broadcast: {e}")
                    cls.clients.discard(client)