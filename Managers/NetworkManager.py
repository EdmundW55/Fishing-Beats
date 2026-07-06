import socket
import struct
import time
import threading

class NetworkManager:
    def __init__(self, host="127.0.0.1", port=62743):
        self.connected = False
        self.host = ""
        self.port = ""

        self.host = host
        self.port = port
        self.socket = None
        self.kill = False

    def send_data(self, data):
        if self.socket:
            self.socket.sendall(struct.pack("b", data))

    def deserialize(self, data):
        dataFormat = "B"
        if len(data) >= struct.calcsize(dataFormat):
            turn, winner, board = struct.unpack_from(dataFormat, data, 0)
            print(turn, chr(winner), list(board.decode("utf-8")))

    def run_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            s.settimeout(1)
            print("connected", s)
            self.socket = s
            self.connected = True
            while not self.kill:
                try:
                    data = self.socket.recv(4096)
                    if len(data):
                        self.deserialize(data)
                except socket.timeout:
                    pass
                time.sleep(0.001)

    def connect_online(self):
        threading.Thread(target=self.run_listener).start()