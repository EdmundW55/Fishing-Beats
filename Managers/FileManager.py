import json
import os

class FileManager:
    def __init__(self, game):
        self.game = game
        self.files_dir = "Maps"
        self.uploadFile = None
        self.uploadFilename = None

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

    def End_File(self, data):
        if self.uploadFile is not None:
            self.uploadFile.close()

            print(f"Finished uploading {self.uploadFilename}")

        self.uploadFile = None
        self.uploadFilename = None