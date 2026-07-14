import socket
import threading
import time
import struct
import json
host = "0.0.0.0"
port = 5000
class Player:
    def __init__(self, conn):
        self.conn = conn
        self.username = "User"
        self.room = None
        self.ready = False

class Room:
    def __init__(self, player, maxPlayers, roomID):
        self.roomID = roomID
        self.players = []
        self.host = player
        self.maxPlayers = maxPlayers
        self.playing = False



class Server:
    def __init__(self, host = "127.0.0.1", port = 62743):
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0
        self.players = []
        self.rooms = {"asacs":Room(Player("a"), 2, "asacs"), "aa":Room(Player("a"), 3, "aa")}

        self.manager = {
            1: self.get_rooms,
            2: self.create_room
        }

    def serialize(self):
        return struct.pack("BB9s", 0, ord("w"), b'abcdefghi')

    def get_rooms(self, player, data):
        conn = player
        roomList = []
        for room in self.rooms.values():
            roomList.append({
                "code": room.roomID,
                "host": room.host.username,
                "players": len(room.players),
                "maxPlayers": room.maxPlayers,
                "started": room.playing
            })

        rooms = json.dumps({
            "rooms": roomList
        }).encode("utf-8")
        # send operation and amount of data in rooms + rooms
        packet = struct.pack("BI", 1, len(rooms)) + rooms
        conn.sendall(packet)

    def create_room(self, player, data):
        conn = player


    def run_listener(self, player):
        self.thread_count += 1
        conn = player.conn
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        conn.settimeout(1)
        with conn:
            while not self.kill:
                try:
                    data = conn.recv(4096)
                    if len(data):
                        data_received = struct.unpack_from("B", data, 0)[0]
                        print(data_received)
                        '''
                        1 = Get Rooms
                        2 = Create Room
                        3 = Join Room
                        4 = Leave Room
                        5 = Get Map
                        6 = Ready toggle
                        7 = Start Match
                        8 = Send Data
                        9 = Final Data
                        '''
                        operation = self.manager.get(data_received)
                        if operation:
                            operation(conn, data)
                except socket.timeout:
                    pass

    def connection_listen_loop(self):
        self.thread_count += 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            # setup listener
            s.bind((self.host, self.port))

            # receive connection
            while not self.kill:
                s.settimeout(1)
                s.listen()
                try:
                    # connection object and address
                    conn, addr = s.accept()
                    print("new connection:", conn, addr)
                    player = Player(conn)
                    self.players.append(player)
                    threading.Thread(target=self.run_listener, args=(player,)).start()
                except socket.timeout:
                    continue
                time.sleep(0.01)
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("killed")

    def run(self):
        threading.Thread(target=self.connection_listen_loop).start()
        try:
            while True:
                time.sleep(0.05)
        except KeyboardInterrupt:
            self.await_kill()


Server().run()