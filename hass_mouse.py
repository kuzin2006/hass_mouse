# mouse motion sensor for Home Assistant


from pynput.mouse import Listener
import threading
import time
import socket
import sys


still_seconds = 0


# mouse motion listener
def on_move(x, y):
    # print('Pointer moved to {0}'.format((x, y)))
    moved.set()


# tcp socket listener
def socket_server():
    # Wait for client
    try:
        while 1:
            conn, addr = s.accept()
            print('# Connected to ' + addr[0] + ':' + str(addr[1]))
            # data = conn.recv(1024)
            conn.send(str(still_seconds).encode('ascii'))
    finally:
        s.close()


HOST = ''
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('# Socket created')

# Create socket on port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('# Bind failed. ')
    sys.exit()
print('# Socket bind complete')

# Start listening on socket
s.listen(10)
print('# Socket now listening')


# start threads
try:
    listener = Listener(on_move=on_move)
    listener.name = 'mouseListener'
    listener.setDaemon(True)
    listener.start()

    server = threading.Thread(name='socket_server', target=socket_server)
    server.setDaemon(True)
    server.start()
except Exception as e:
    print(e.args)

moved = threading.Event()

while 1:
    # server
    time.sleep(1)
    still_seconds += 1
    # print(still_seconds)
    if moved.isSet():
        still_seconds = 0
        moved.clear()
        # print("Motion")

