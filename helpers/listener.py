from queue import Queue
from threading import Thread
from flask import Flask, request
from network import find_free_port


LISTENER_HOST = '0.0.0.0'
LISTENER_PORT = find_free_port()
LISTENER_URL = f'http://{LISTENER_HOST}:{LISTENER_PORT}'


def run_listener(queue: Queue, daemon=True, port=LISTENER_PORT):
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def receive_msg():
        if request.json.get('message'):
            queue.put(request.json)
            return 'Message received.', 200

    task_thread = Thread(daemon=daemon, target=lambda: app.run(host=LISTENER_HOST, port=port, debug=False))
    task_thread.start()


if __name__ == '__main__':
    listener_queue = Queue()
    run_listener(listener_queue, False)
