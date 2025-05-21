from tornado.web import Application, RequestHandler
from chat.handler import ChatWebSocketHandler

class MainHandler(RequestHandler):
    def get(self):
        self.render("test.html")

def create_app():
    return Application([
        (r"/", MainHandler),
        (r"/ws/chat", ChatWebSocketHandler),
    ], template_path="templates")
