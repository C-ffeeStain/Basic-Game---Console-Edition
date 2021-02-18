import json

def split(string):
    return [char for char in string]

class Level:
    name = "level_1"
    tiles = ["air", "wall", "score", "player", "exit"]
    generic = {
    "air": "0",
    "wall": "1",
    "score": "3",
    "player": "2",
    "exit": "E"
    }
    player = {
        "x": 4,
        "y": 2,
        "prev_x": 4,
        "prev_y": 2
    }
    score_appear_interval = 3
    unlock_exit_score = score_appear_interval * 3
    def __init__(self, name = "level"):
        self.name = name

    def set_vars(self):
        with open("levels\\" + self.name + ".json") as raw:
            level_json = json.loads(raw.read())
        self.score_appear_interval = level_json["score_appear_interval"]
        self.unlock_exit_score = level_json["unlock_exit_score"]
        for tile in self.tiles:
            self.generic[tile] = level_json["generic"][tile]
        
    def parse(self):
        self.area = []
        with open("levels\\" +self.name + ".lvl", "r") as lvl:
            self.area = [split(line) for line in lvl]
            for line in self.area:
                for tile in line:
                    if tile == "\n":
                        line.remove("\n")