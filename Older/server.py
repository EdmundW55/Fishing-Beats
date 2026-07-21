import time
import struct
import socket
import threading
import json


def send_message(conn, data_bytes):
    try:
        length = len(data_bytes)
        conn.sendall(length.to_bytes(4, 'big') + data_bytes)
    except (BrokenPipeError, ConnectionResetError, OSError):
        print(f"Failed to send to {conn}, connection probably closed.")

class Server:
    def __init__(self, host='127.0.0.1', port=62087):
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0

        self.players = {}
        self.winner = None
        self.rooms = {}#2:[[1, 3], "song"]
        self.room_counter = 0

    def serialized(self, score, combo, maxcombo = 0):
        return struct.pack('>IH', score, combo)

    def recv_all(self, conn, length):
        data = b''
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                raise ConnectionResetError("Connection closed while receiving data")
            data += packet
        return data

    def recv_message(self, conn):
        raw_length = self.recv_all(conn, 4)
        message_length = struct.unpack('>I', raw_length)[0]
        return self.recv_all(conn, message_length)

    def create_room(self, conn):
        self.rooms[self.room_counter] = [[conn], {}, conn] # players, song, leader
        self.players[conn][0] = self.room_counter
        self.players[conn][2] = "unready"
        self.room_counter += 1
        send_message(conn, b'CREATED ROOM')

    def join_room(self, conn, room_id):
        if room_id not in self.rooms:
            # add room if it's not available
            if room_id > self.room_counter:
                self.room_counter = room_id
            self.rooms[room_id] = [[], {}, conn]
            self.players[conn][0] = room_id
            if room_id >= self.room_counter:
                self.room_counter += 1
        else:
            self.rooms[room_id][0].append(conn)
            self.players[conn][0] = room_id
            message = f'JOINED {room_id}'
            data = message.encode("utf-8")
            send_message(conn, data)

            notify = f"PLAYER JOINED:{self.players[conn][1]}"
            notify_data = notify.encode("utf-8")
            for player in self.rooms[room_id][0]:
                if player != conn:
                    send_message(player, notify_data)


    def leave_room(self, conn, disconnect = False):
        print(conn, "room:", self.players[conn])
        if self.players[conn][0] is not None:
            leader = False
            if self.rooms[self.players[conn][0]][2] == conn:
                leader = True
            self.rooms[self.players[conn][0]][0].remove(conn)

            # if the room is empty
            if not self.rooms[self.players[conn][0]][0]:
                del self.rooms[self.players[conn][0]]
                print(f"Room {self.players[conn][0]} deleted because it is empty.")
            else:
                message = f'PLAYER LEFT:{self.players[conn][1]}'
                data = message.encode("utf-8")
                for player in self.rooms[self.players[conn][0]][0]:
                    print(player)
                    send_message(player, data)
                if leader:
                    self.rooms[self.players[conn][0]][2] = self.rooms[self.players[conn][0]][0][0]

            self.players[conn][0] = None
            print("leaving?")

            if not disconnect:
                self.send_room_info(conn)
                print("aaa")
            self.players[conn][2] = "select"

    def set_room_map(self, conn, mapInfo):
        if self.players[conn][0] is not None:
            self.rooms[self.players[conn][0]][1] = mapInfo
            room = self.players[conn][0]
            room_info = {"map": [self.rooms[room][1]["name"], self.rooms[room][1]["content"]]}
            room_info_json = json.dumps(room_info).encode()
            print(f"Sending map info to room {room}")
            for player in self.rooms[self.players[conn][0]][0]:
                if player != conn:
                    send_message(player, room_info_json)

    def send_map(self, conn):
        map_info = self.rooms[self.players[conn][0]][1]
        if map_info:
            map_info_json = json.dumps(map_info).encode()
            send_message(conn, map_info_json)
            print(f"Sent map info to {conn}")

    def send_room_info(self, conn, room = None):
        if room is None:
            room_info = {room_id: len(items[0]) for room_id, items in self.rooms.items()}

            # Convert keys to strings for JSON compatibility
            room_info_json = json.dumps(room_info).encode()
            send_message(conn, room_info_json)
            print(f"Sent room info to {conn}:", room_info)
        else:
            print(type(room), self.rooms)
            self.players[conn][2] = "unready"
            leader = self.rooms[self.players[conn][0]][2]
            if self.rooms[room][1] == {}:
                room_info = {"players": [self.players[player][1] for player in self.rooms[room][0]], "map": "",
                             "leader": self.rooms[self.players[conn][0]][0].index(leader)}
            else:
                room_info = {"players": [self.players[player][1] for player in self.rooms[room][0]],
                             "map": [self.rooms[room][1]["name"], self.rooms[room][1]["content"]],
                             "leader": self.rooms[self.players[conn][0]][0].index(leader)}

            room_info_json = json.dumps(room_info).encode()
            send_message(conn, room_info_json)

    def ready_up(self, conn, status):
        if status:
            self.players[conn][2] = "ready"
        else:
            self.players[conn][2] = "unready"

        message = {"READY": [self.players[conn][1], self.rooms[self.players[conn][0]][0].index(conn), status]}

        data = json.dumps(message).encode()

        for player in self.rooms[self.players[conn][0]][0]:
            send_message(player, data)


    def run_listener(self, conn):
        self.thread_count += 1
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        conn.settimeout(1)
        with conn:
            while not self.kill:
                try:
                    data = self.recv_message(conn)
                    # leave multiplayer
                    if data == b'LEAVE':
                        print("Client requested to leave.")
                        if conn in self.players:
                            self.leave_room(conn, True)
                            self.players.pop(conn)
                            print("a player disconnected from server", len(self.players))
                        break  # exit listener loop
                    # get rooms
                    elif data == b'GET ROOMS':
                        print("Client requested rooms.")
                        if conn in self.players:
                            try:
                                self.send_room_info(conn)
                            except Exception as e:
                                print("Error sending room info:", e)

                    # set name of player
                    elif data.startswith(b'NAME:'):
                        print("Client sent a name.")
                        if conn in self.players:
                            try:
                                name = data.decode().split(":", 1)
                                self.players[conn][1] = name[1]
                            except Exception as e:
                                print("Error setting name:", e)

                    # create room
                    elif data == b'CREATE ROOM':
                        try:
                            print("Client requested to Create room.")
                            if conn in self.players:
                                self.create_room(conn)
                                print(f"Created room {self.players[conn][0]}")
                        except Exception as e:
                            print("Error creating room:", e)
                    # join room update to send data to users in room
                    elif data == b'GET MAP':
                        print("Client requested map.")
                        if conn in self.players:
                            try:
                                self.send_map(conn)
                            except Exception as e:
                                print("Error sending map:", e)
                    # ready up in room
                    elif data == b'READY':
                        print("Client ready up.")
                        if conn in self.players:
                            self.ready_up(conn, True)
                            # ready up in room
                    elif data == b'UNREADY':
                        print("Client ready up.")
                        if conn in self.players:
                            self.ready_up(conn, False)
                    # start game
                    elif data == b'START':
                        print("starting match")
                        if conn in self.players and self.players[conn][0] is not None:
                            for player in self.rooms[self.players[conn][0]][0]:
                                self.players[conn][2] = "Alive"
                                send_message(player, b'START MATCH')
                    # player alive
                    elif data == b'ALIVE':
                        if conn in self.players:
                            self.players[conn][2] = "Alive"
                    # player died
                    elif data == b'DEAD':
                        if conn in self.players:
                            self.players[conn][2] = "Dead"
                    # join room update to send data to users in room
                    elif data.startswith(b'JOIN '):
                        try:
                            print("Client requested to Join room.")
                            if conn in self.players:
                                room_id = data[5:].decode().strip()
                                self.join_room(conn, int(room_id))
                                print(f"sent data of {room_id}")
                        except Exception as e:
                            print("Error sending joined room:", e)


                    elif data.startswith(b'ROOM '):
                        try:
                            print("Client requested data of a room")
                            if conn in self.players:
                                room_id = data[5:].decode().strip()
                                print(f"room_id: {room_id}")
                                self.send_room_info(conn, int(room_id))
                                print(f"sent data of {room_id} to {conn}")
                        except Exception as e:
                            print("Error sending joined:", e)
                    # leave room
                    elif data == b'LEAVE ROOM':
                        print("Client requested to leave room.")
                        try:
                            if conn in self.players:
                                self.leave_room(conn)
                        except Exception as e:
                            print("Client failed to leave room:", e)

                            print("a player disconnected from a room")
                    elif len(data):
                        if data.startswith(b'score'):
                            payload = data[5:]
                            score = f'{self.rooms[self.players[conn][0]][0].index(conn)}:'.encode("utf-8") + payload
                            if self.players[conn][0] is not None:
                                for other_conn in self.rooms[self.players[conn][0]][0]:
                                    if other_conn != conn:
                                        try:
                                            send_message(other_conn, score)
                                        except OSError:
                                            self.leave_room(other_conn)
                                            self.players.pop(other_conn)
                                            print("other person disconnect", len(self.players))
                        elif data.startswith(b'final score'):
                            self.players[conn][2] = "unready"
                            payload = data[11:]
                            score = f'final{self.rooms[self.players[conn][0]][0].index(conn)}:'.encode("utf-8") + payload
                            if self.players[conn][0] is not None:
                                for other_conn in self.rooms[self.players[conn][0]][0]:
                                    if other_conn != conn:
                                        try:
                                            send_message(other_conn, score)
                                        except OSError:
                                            self.leave_room(other_conn)
                                            self.players.pop(other_conn)
                                            print("other person disconnect", len(self.players))
                        else:
                            try:
                                # set map
                                decoded = data.decode()
                                mapInfo = json.loads(decoded)
                                if conn in self.players:
                                    self.set_room_map(conn, mapInfo)
                            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                                # scores and combo of other players
                                print(e)

                except socket.timeout:
                    pass
                except (ConnectionResetError, BrokenPipeError):
                    if conn in self.players:
                        self.leave_room(conn)
                        self.players.pop(conn)
                        print("this player disconnect", len(self.players))
                    break
        if conn in self.players:
            self.leave_room(conn)
            self.players.pop(conn)
            print("Removed player. Remaining:", len(self.players))
        self.thread_count -= 1

    def connection_listen_loop(self):
        self.thread_count += 1
        # create socket dgram for udp tcp sock_Stream
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.bind((self.host, self.port))

            # not stuck in call for socket kill =true exit reasonable time
            while not self.kill:
                s.settimeout(1)
                s.listen()
                try:
                    conn, addr = s.accept()
                    print("new connection:", conn, addr)
                    self.players[conn] = [None, "", "select"]
                    self.send_room_info(conn)
                    # spawn listener task
                    print("now:", len(self.players))
                    threading.Thread(target=self.run_listener, args=(conn,)).start()
                # when no one connecting
                except socket.timeout:
                    continue
                time.sleep(0.01)
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("killed")

    def command_listener(self):
        while True:
            try:
                cmd = input("Enter command (r = rooms, p = players): ").strip().lower()
                if cmd == 'r':
                    rooms = {k: [[self.players[player][1] for player in v[0]], {key: value for key, value in v[1].items() if key not in {"content", "song"}}, v[2]]
                             for k, v in self.rooms.items()}
                    print("rooms:", rooms)
                elif cmd == 'p':
                    print("players:", self.players)
            except EOFError:
                break  # Handles Ctrl+D gracefully

    def run(self):
        threading.Thread(target=self.connection_listen_loop).start()
        threading.Thread(target=self.command_listener, daemon=True).start()
        try:
            while True:
                self.winner = None
                for player_conn in self.players:
                    try:
                        player_conn.send(b'')
                    except OSError:
                        pass
                time.sleep(0.05)
        # change this depending on how you exit the game
        except KeyboardInterrupt:
            self.await_kill()

Server().run()