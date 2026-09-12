import json
import os
import hashlib

class FileManager:
    def __init__(self, game):
        self.game = game
        self.files_dir = "Maps"
        self.uploadFile = None
        self.uploadFilename = None
        self.sha256 = hashlib.sha256()
        self.gotTxt = False
        self.gotMp3 = False

    def Start_File(self, data):
        metaData = json.loads(data.decode("utf-8"))

        filename = metaData["fileName"]
        folderName = metaData["folderName"]
        filename = os.path.basename(filename)

        mapPath = os.path.join("Maps", folderName)

        os.makedirs(mapPath, exist_ok=True)

        filepath = os.path.join(mapPath, filename)

        self.uploadFile = open(filepath, "wb")
        self.uploadFilename = filename

    def Get_Chunk(self, data):
        if self.uploadFile is None:
            return

        self.uploadFile.write(data)

    def End_File(self, room):
        if self.uploadFile is not None:
            self.uploadFile.close()

            print(f"Finished uploading {self.uploadFilename}")
            if self.uploadFilename.endswith(".txt"):
                self.gotTxt = True
            elif self.uploadFilename.endswith(".mp3"):
                self.gotMp3 = True

        if self.gotTxt and self.gotMp3:
            self.gotTxt = False
            self.gotMp3 = False
            room.downloaded()
        self.uploadFile = None
        self.uploadFilename = None

    def Check_File(self, dir):
        mapDir = os.path.isdir("Maps/"+dir)
        if mapDir:
            name = dir.split("-", 1)[1]
            mapPath = os.path.join("Maps", dir, name+".txt")
            Chunk_Size = 64 * 1024
            self.sha256 = hashlib.sha256()
            with open(mapPath, "rb") as f:
                while True:
                    chunk = f.read(Chunk_Size)
                    if not chunk:
                        break
                    self.sha256.update(chunk)
            digest = self.sha256.hexdigest()
            digest = digest.encode("utf-8")
            print("sending check")
            self.game.network.send_data(14, digest)
            return True
        else:
            return False

