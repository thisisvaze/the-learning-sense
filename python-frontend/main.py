import socketio


sio = socketio.Client(logger=True, reconnection=True, engineio_logger=True)


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print(data)


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.event
def message(data):
    print("message recieved")


@sio.on('my message')
def on_message(data):
    print('I received a message!')


sio.connect('ws://localhost:8000/',
            socketio_path='ws')
sio.wait()
