import os
from tornado.web import Application, StaticFileHandler
from websocket.chat_ws_handler import ChatWebSocketHandler
from websocket.room_handler import RoomWebSocketHandler

def create_app():
    # 🔧 Utilise une variable d'env avec fallback
    front_path = os.getenv("FRONT_PATH", "/var/www/html/MicroService/ms-chat/front/dist")

    return Application([
        # WebSocket handlers
        (r"/ws/chat", ChatWebSocketHandler),
        (r"/ws/rooms", RoomWebSocketHandler),  # ← Ajouter le "s" pour matcher le frontend

        # Static files (SPA React/Vite/etc.)
        (r"/(.*)", StaticFileHandler, {
            "path": front_path,
            "default_filename": "index.html"
        }),
    ])