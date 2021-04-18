"""Contains all the classes for this game."""

import sys
import os
import argparse
import random
from logger import log, LogLevel


def split(string):
    return [char for char in string]


class Level:
    """A level. It auto parses itself when initialized, so no need to call its `parse` method."""
    # TODO: add spike tile that turns on/off
    name = "level_1"
    generic = {
        "air": "0",
        "wall": "1",
        "score": "$",
        "player": "2",
        "exit": "E"
    }
    player = {
        "x": 4,
        "y": 2,
        "prev_x": 4,
        "prev_y": 3
    }
    score_appear_interval = 3
    unlock_exit_score = score_appear_interval * 3

    def __init__(self, name="level"):
        self.name = name
        self.area = []
        self.parse()

    def parse(self):
        with open(os.path.join("levels\\" + self.name + ".lvl"), "r") as lvl:
            self.area = [split(line) for line in lvl]
            for line in self.area:
                for tile in line:
                    if tile not in self.generic.values():
                        line.remove("\n") if tile == "\n" else print("Unknown tile found: '{}'".format(tile))


class Game:
    score = 0
    turn = 1
    lvl = Level("level_1")
    exit_in_lvl = False
    prev_playerX = 0
    prev_playerY = 0
    direction = ""
    win = False

    def __init__(self):
        argparse.ArgumentParser(
            description="A basic console game with some extra features.")
        try:
            y, x = self.get_first_block("2")
        except TypeError as e:
            log(LogLevel.Error, "Could not find player, please add a 2 in your level.")
            print(e.args[0])
            sys.exit(0)
        self.lvl.player["x"], self.lvl.player["y"] = x, y

    def findall(self, block):
        indices = []
        for i, v in enumerate(self.lvl.area):
            for i1, v1 in v:
                if block == v1:
                    indices.append([i, i1])
        return indices

    def get_first_block(self, block):
        print(self.lvl.area)
        for i, v in enumerate(self.lvl.area):
            for tile in v:
                if tile == block:
                    return i, v.index(block)
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
        if direction == "a":
            next_coord = self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"] - 1]
            if next_coord != self.lvl.generic["wall"]:
                if next_coord == self.lvl.generic["score"]:
                    self.score += 1
                elif next_coord == self.lvl.generic["exit"]:
                    self.win = True
                self.turn += 1
                self.lvl.player["prev_x"] = self.lvl.player["x"]
                self.lvl.player["prev_y"] = self.lvl.player["y"]
                self.lvl.player["x"] -= 1
                self.lvl.area[self.lvl.player["prev_y"]
                              ][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]
                              ][self.lvl.player["x"]] = self.lvl.generic["player"]
        elif direction == "d":
            next_coord = self.lvl.area[self.lvl.player["y"]][self.lvl.player["x"] + 1]
            if next_coord != self.lvl.generic["wall"]:
                if next_coord == self.lvl.generic["score"]:
                    self.score += 1
                elif next_coord == self.lvl.generic["exit"]:
                    self.win = True
                self.turn += 1
                self.lvl.player["prev_y"] = self.lvl.player["y"]
                self.lvl.player["prev_x"] = self.lvl.player["x"]
                self.lvl.player["x"] += 1
                self.lvl.area[self.lvl.player["prev_y"]
                              ][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]
                              ][self.lvl.player["x"]] = self.lvl.generic["player"]
        elif direction == "w":
            next_coord = self.lvl.area[self.lvl.player["y"] - 1][self.lvl.player["x"]]
            if next_coord != self.lvl.generic["wall"]:
                if next_coord == self.lvl.generic["score"]:
                    self.score += 1
                elif next_coord == self.lvl.generic["exit"]:
                    self.win = True
                self.turn += 1
                self.lvl.player["prev_y"] = self.lvl.player["y"]
                self.lvl.player["prev_x"] = self.lvl.player["x"]
                self.lvl.player["y"] -= 1
                self.lvl.area[self.lvl.player["prev_y"]
                              ][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]
                              ][self.lvl.player["x"]] = self.lvl.generic["player"]
        elif direction == "s":
            next_coord = self.lvl.area[self.lvl.player["y"] + 1][self.lvl.player["x"]]
            if next_coord != self.lvl.generic["wall"]:
                if next_coord == self.lvl.generic["score"]:
                    self.score += 1
                elif next_coord == self.lvl.generic["exit"]:
                    self.win = True
                self.turn += 1
                self.lvl.player["prev_y"] = self.lvl.player["y"]
                self.lvl.player["prev_x"] = self.lvl.player["x"]
                self.lvl.player["y"] += 1
                self.lvl.area[self.lvl.player["prev_y"]
                              ][self.lvl.player["prev_x"]] = self.lvl.generic["air"]
                self.lvl.area[self.lvl.player["y"]
                              ][self.lvl.player["x"]] = self.lvl.generic["player"]

    def loop(self):
        while True:
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
            direction = input(
                "Enter a direction to move (w, a, s, or d) or 'q' to quit: ")
            if direction == 'q':
                sys.exit(0)
            print("\nScore: " + str(self.score) + "\n")
            if self.win:
                print("Congrats! You win!")
                sys.exit(0)
            self.move(direction)
