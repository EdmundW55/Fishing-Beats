import socket
import struct
import time
import threading

class NetworkManager:
    def __init__(self, game, host="127.0.0.1", port=62743):
        self.connected = False
        self.host = host
        self.port = port
        self.socket = None
        self.kill = False
        # (unsigned) char + integer
        self.headerFormat = b'BI'
        self.headerSize = struct.calcsize(self.headerFormat)
        self.game = game

    def send_data(self, data):
        if self.socket:
            self.socket.sendall(struct.pack("b", data))

    def deserialize(self, operation, data):
        self.game.states[-1].online(operation, data)

    # receive exact data needed based on size of packets
    def recv_exact(self, size):
        data = b""

        while len(data) < size:
            packet = self.socket.recv(size - len(data))

            if not packet:
                return None

            data += packet
        return data

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
                    header = self.recv_exact(self.headerSize)
                    if header is None:
                        break

                    operation, size = struct.unpack(self.headerFormat, header)
                    payload = self.recv_exact(size)

                    if payload is None:
                        break

                    self.deserialize(operation, payload)
                except socket.timeout:
                    pass
                time.sleep(0.001)

    def connect_online(self):
        threading.Thread(target=self.run_listener).start()