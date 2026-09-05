import socket
import struct
import time
import threading
import os
import json

class NetworkManager:
    def __init__(self, game, host="127.0.0.1", port=62743):
        self.connected = False
        self.host = host
        self.port = port
        self.socket = None
        self.kill = False
        # (unsigned) char + integer
        self.headerFormat = b'!BI'
        self.headerSize = struct.calcsize(self.headerFormat)
        self.game = game

    def send_data(self, operation, message=b""):
        # send operation + message/data to server
        packet = struct.pack("!BI", operation, len(message)) + message
        self.socket.sendall(packet)

    def send_file(self, path, folderName):
        fileName = os.path.basename(path)
        fileSize = os.path.getsize(path)

        metadata = {
            "fileName": fileName,
            "folderName": folderName,
            "size": fileSize
        }

        meta_json = json.dumps(metadata).encode("utf-8")
        # send meta data
        self.send_data(11, meta_json)

        # 64 kb chunks sent
        Chunk_Size = 64 * 1024

        with open(path, "rb") as f:
            while True:

                chunk = f.read(Chunk_Size)
                if not chunk:
                    break

                self.send_data(12, chunk)
        # send end of file
        self.send_data(13)
        print(f"Finished sending {fileName} to server")

    def send_map(self):
        songPath = os.path.join(self.game.songStore[0], self.game.songStore[1] + ".mp3")
        mapPath = os.path.join(self.game.songStore[0], self.game.songStore[1] + ".txt")
        folderName = os.path.basename(self.game.songStore[0])
        if os.path.isfile(mapPath):
            self.send_file(mapPath, folderName)

        if os.path.isfile(songPath):
            self.send_file(songPath, folderName)

    def decode_data(self, format, data):
        decoded = struct.unpack(format, data)
        return decoded

    def deserialize(self, operation, data):
        # make states do the work
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
