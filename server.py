import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import json
import numpy
from io import BytesIO
from PIL import Image
from tornado.options import define, options
import opencv
import base64
import datetime

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/live", LiveStreamSocketHandler),
        ]

        settings = dict(
            cookie_secret="asdsafl.rleknknfkjqweonrkbknoijsdfckjnk 234jn",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            autoescape=None,
            debug=True
        )

        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        logging.info('new connection')
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(":","-")
        filename = time + ".log"
        self.log = open("logs/" + filename, "a")

    def on_message(self, message):
        self.process(json.loads(message))

    def on_close(self):
        logging.info('connection closed')

    def process(self, cv_image):
        logging.info("nothing to do....")


class LiveStreamSocketHandler(SocketHandler):

    def process(self, message):
        # convert to cv image for analysis

        data = dict()

        # convert to cv image for analysis
        cv_image = self.to_cv_image(message)

        if message["emotion"]:

            data['emotion'] = opencv.detect_emotion(cv_image)

            if data['emotion']:
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.log.write("[" + time + "]" + "\t" + data['emotion'] + "\n")

        if message["face"]:

            img = opencv.detect_face(cv_image, 0)

            # convert back to base64
            data['img'] = self.to_image(img)

        else:

            data['img'] = message["img"]

        self.write_message(json.dumps(data))

    def to_cv_image(self, message):
        image_str = message['img'][message['img'].find(",") + 1:]
        image = Image.open(BytesIO(base64.b64decode(image_str)))
        return numpy.array(image)

    def to_image(self, img):
        image = Image.fromarray(img)
        buff = BytesIO()
        image.save(buff, format="JPEG")
        return base64.b64encode(buff.getvalue()).decode("utf-8")


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.info("Starting...")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
