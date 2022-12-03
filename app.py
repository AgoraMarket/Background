# coding=utf-8
from app import app

PORT = 5055
HOST = '0.0.0.0'
if __name__ == '__main__':
        app.run(
                debug=True,
                host=HOST,
                port=PORT,
                threaded=True
        )
