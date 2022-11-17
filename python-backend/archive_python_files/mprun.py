from multiprocessing import Process, Manager
import multiprocessing
import main_socketio
import time
if __name__ == "__main__":
    shared_data_queue = Manager().Queue()
    p1 = Process(target=main_socketio.env_info_update,
                 args=(shared_data_queue,))
    p2 = Process(target=main_socketio.main, args=(shared_data_queue,))
    p1.start()
    p2.start()
