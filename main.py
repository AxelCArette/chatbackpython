import os
from tornado.web import Application, StaticFileHandler
from chat.handler import ChatWebSocketHandler

def create_app():
    front_path = "/var/www/html/MicroService/ms-chat/front/dist"

    return Application([
        (r"/ws/chat", ChatWebSocketHandler),
        (r"/(.*)", StaticFileHandler, {
            "path": front_path,
            "default_filename": "index.html"
        }),
    ])
