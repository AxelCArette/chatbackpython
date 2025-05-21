import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import create_app
import tornado.ioloop

if __name__ == "__main__":
    app = create_app()
    app.listen(8888)
    print("http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
