import zmq


def ping(port = 5555) -> dict:
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://127.0.0.1:{port}")
    socket.send_json({"command": "ping"})
    resp = socket.recv_json()
    return resp


def get_status(port = 5555) -> dict:
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://127.0.0.1:{port}")
    socket.send_json({"command": "get_status"})
    resp = socket.recv_json()
    return resp


def stop(port = 5555) -> None:
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://127.0.0.1:{port}")
    socket.send_json({"command": "stop"})


def reload(port=5555) -> dict:
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://127.0.0.1:{port}")
    socket.send_json({"command": "reload"})
    resp = socket.recv_json()
    return resp


def start_bot(bot_id: int, port=5555) -> dict:
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://127.0.0.1:{port}")
    socket.send_json({"command": "start_bot", "bot_id": bot_id})
    resp = socket.recv_json()
    return resp


def stop_bot(bot_id: int, port=5555) -> dict:
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://127.0.0.1:{port}")
    socket.send_json({"command": "stop_bot", "bot_id": bot_id})
    resp = socket.recv_json()
    return resp


def restart_bot(bot_id: int, port=5555) -> dict:
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://127.0.0.1:{port}")
    socket.send_json({"command": "restart_bot", "bot_id": bot_id})
    resp = socket.recv_json()
    return resp


