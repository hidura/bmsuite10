import json

import css2json


class Modules:

    def __init__(self, static_file_dir):
        self.icons=[]
        self.static_file_dir=static_file_dir



    def loadInfo(self):

        with open(self.static_file_dir+"/font-awesome/css/font-awesome.css", "r") as file:
            css = css2json.css2json(file.read().replace(":before",""))
            self.icons= json.loads(css)
