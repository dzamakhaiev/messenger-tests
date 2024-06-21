import socket
from queue import Queue
from threading import Thread
from flask import Flask, request
from helpers.network import find_free_port


LISTENER_HOST = '0.0.0.0'


def run_listener(queue: Queue, port=None):
    app = Flask(__name__)
    if not port:
        port = find_free_port()

    @app.route('/', methods=['POST'])
    def receive_msg():
        if request.json.get('message'):
            queue.put(request.json)
            return 'Message received.', 200

    task_thread = Thread(target=lambda: app.run(host=LISTENER_HOST, port=port, debug=False), daemon=True)
    task_thread.start()
    return f'http://{socket.gethostbyname(socket.gethostname())}:{port}'


if __name__ == '__main__':
    listener_queue = Queue()
    run_listener(listener_queue, False)
