import tornado.web
import tornado.websocket
import tornado.ioloop
import random
import json

HTMLDIR = "html"

# List to hold WebSocket clients
ws_clients = []

class IndexPage(tornado.web.RequestHandler):
    def get(self):
        self.write("<a href='/static/roulette.html'>Visit the casino</a>")

class RoulettePage(tornado.web.RequestHandler):
    def get(self):
        self.render("roulette.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")
        ws_clients.append(self)

    def on_message(self, message):
        data = json.loads(message)
        if data.get("action") == "spin":
            selectedNumber = random.choice(range(0, 37))
            spinResult = {
                "number": selectedNumber,
                "color": "Red" if selectedNumber % 2 != 0 else "Black",
                "evenOdd": "Even" if selectedNumber % 2 == 0 else "Odd",
                "failedPassed": "Failed" if selectedNumber > 18 else "Passed"
            }
            # Broadcast spin result to all connected WebSocket clients
            for client in ws_clients:
                client.write_message(json.dumps({"action": "spinResult", "spinResult": spinResult}))

    def on_close(self):
        print("WebSocket connection closed")
        ws_clients.remove(self)

def makeApp():
    endpoints = [
        ("/", IndexPage),
        ("/roulette", RoulettePage),
        ("/sock", WebSocketHandler),
        ("/static/(.*)", tornado.web.StaticFileHandler, {"path": HTMLDIR})
    ]
    app = tornado.web.Application(endpoints, static_path=HTMLDIR, template_path=HTMLDIR)
    return app

if __name__ == "__main__":
    app = makeApp()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
