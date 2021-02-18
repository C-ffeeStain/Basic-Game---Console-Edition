import sys
import random
import levelparser
import argparse
import json

class Game:
    score = 0
    turn = 1
    lvl = levelparser.Level("level_1")
    exit_in_lvl = False
    prev_playerX = 0
    prev_playerY = 0
    direction = ""
    win = False
    def __init__(self, argv):
        cmdparser = argparse.ArgumentParser(description="A basic console game with some extra features.")
        cmdparser.add_argument("--key", type=str, action="store", metavar="[level]", help="Shows the key of a level file. For [level], put the name of the level w/o .lvl.")
        args = cmdparser.parse_args()
        if args.key != None:
            with open(args.key  + ".json", "r") as f:
                data = json.loads(f.read())
                print(json.dumps(data['generic'], sort_keys=True, indent=4))
            sys.exit(0)
        self.lvl.parse()
        self.lvl.set_vars()

    def get_first_block(self, block):
        for i, v in enumerate(self.lvl.area):
            if block in v:
                return (i, v.index(block))
            return None
    def get_rnd_block(self, block) -> tuple:
            row = random.randint(0, len(self.lvl.area) - 1)
            tile = random.randint(0, len(self.lvl.area[0]) - 1)
            random_area = self.lvl.area[row][tile]
            if random_area == block:
                return tile, row
            else:
                    return self.get_rnd_block(block)
             
    def move(self, direction):
        direction = direction.lower()
        if direction == "a":
            nextcoord = self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"] - 1]
            if nextcoord != self.lvl.generic["wall"]:
                if nextcoord == self.lvl.generic["score"]:
                    self.score += 1
                elif nextcoord == self.lvl.generic["exit"]:
                    self.win = True
                self.turn += 1
                self.lvl.player["prev_x"] = self.lvl.player["x"]
                self.lvl.player["x"] -= 1
                self.lvl.area[self.lvl.player["prev_y"]][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"]] = self.lvl.generic["player"]
        elif direction == "d":
            nextcoord = self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"] + 1]
            if nextcoord != self.lvl.generic["wall"]:
                if nextcoord == self.lvl.generic["score"]:
                    self.score += 1
                elif nextcoord == self.lvl.generic["exit"]:
                    self.win = True
                self.turn += 1
                self.lvl.player["prev_x"] = self.lvl.player["x"]
                self.lvl.player["x"] += 1
                self.lvl.area[self.lvl.player["prev_y"]][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"]] = self.lvl.generic["player"]
        elif direction == "w":
            nextcoord = self.lvl.area[self.lvl.player["y"] - 1][self.lvl.player["x"]]
            if nextcoord != self.lvl.generic["wall"]:
                if nextcoord == self.lvl.generic["score"]:
                    self.score += 1
                elif nextcoord == self.lvl.generic["exit"]:
                    self.win = True
                self.turn += 1
                self.lvl.player["prev_y"] = self.lvl.player["y"]
                self.lvl.player["y"] -= 1
                self.lvl.area[self.lvl.player["prev_y"]][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"]] = self.lvl.generic["player"]
        elif direction == "s":
            nextcoord = self.lvl.area[self.lvl.player["y"] + 1][self.lvl.player["x"]]
            if nextcoord != self.lvl.generic["wall"]:
                if nextcoord == self.lvl.generic["score"]:
                    self.score += 1
                elif nextcoord == self.lvl.generic["exit"]:
                    self.win = True
                self.lvl.player["prev_y"] = self.lvl.player["y"]
                self.turn += 1
                self.lvl.player["y"] += 1
                self.lvl.area[self.lvl.player["prev_y"]][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"]] = self.lvl.generic["player"]
                
    def loop(self):
        while (True):
            if self.turn % self.lvl.score_appear_interval == 0:
                try:
                    tile, row = self.get_rnd_block(self.lvl.generic["air"])
                    self.lvl.area[row][tile] = self.lvl.generic["score"]
                except RecursionError: 
                    print("Could not find block, skipping...")
            if self.score == self.lvl.unlock_exit_score and not self.exit_in_lvl:
                try:
                    self.exit_in_lvl = True
                    tile, row = self.get_rnd_block(self.lvl.generic["wall"])
                    self.lvl.area[row][tile] = self.lvl.generic["exit"]
                except RecursionError:
                    print("Could not find block, skipping")
            count = 1
            max_len = len(self.lvl.area[0])
            for row in self.lvl.area:
                for tile in row:
                    if count < max_len:
                        print(tile, sep="", end="")
                        count += 1
                    else:
                        count = 1
                        print(tile)
            
            print("\nScore: " + str(self.score) + "\n")
            if self.win == True:
                print("Congrats! You win!")
                sys.exit(0)
            direction = input(
                "\nEnter a direction (w, a, s, or d), or type 'q' to quit: ")
            if (direction == 'q'):
                sys.exit(0)
            self.move(direction)

Game(sys.argv[1:]).loop()