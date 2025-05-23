import json
import tornado.websocket
from websocket.dispatcher import dispatch_action

class ChatWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        ChatWebSocketHandler.clients.add(self)
        print("[WS] Client connecté")

    def on_close(self):
        if self in ChatWebSocketHandler.clients:
            ChatWebSocketHandler.clients.remove(self)
        print("[WS] Client déconnecté")

    async def on_message(self, message):
        try:
            data = json.loads(message)
            action = data.get("action")
            
            print(f"[WS] Action reçue: {action}")  # Debug
            
            # Utiliser le dispatcher
            await dispatch_action(action, data, self)
                
        except json.JSONDecodeError:
            await self.write_message(json.dumps({
                "type": "error",
                "message": "Format JSON invalide"
            }))
        except Exception as e:
            print(f"[WS] Erreur: {str(e)}")
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