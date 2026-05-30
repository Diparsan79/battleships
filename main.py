import copy
import random
import time

class GameBoard(object):

    def __init__(self, battleships, width, height):
        self.battleships = battleships
        self.shots = []
        self.width = width
        self.height = height

    def take_shot(self, shot_location):
        hit_battleship = None
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:
                is_hit = True
                b.hits[idx] = True
                hit_battleship = b
                break

        self.shots.append(Shot(shot_location, is_hit))
        return hit_battleship

    def is_game_over(self):
        return all([b.is_destroyed() for b in self.battleships])


class Shot(object):

    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit


class Battleship(object):

    @staticmethod
    def build(head, length, direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i)
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "W":
                el = (head[0] - i, head[1])
            elif direction == "E":
                el = (head[0] + i, head[1])

            body.append(el)

        return Battleship(body, direction)

    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
        self.hits = [False] * len(body)

    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None

    def is_destroyed(self):
        return all(self.hits)


class Player(object):

    def __init__(self, name, shot_f):
        self.name = name
        self.shot_f = shot_f

def render_basic(game_board, show_battleships=False):
    header = "+" + "-" * game_board.width + "+"
    print(header)

# an empty board
    board = []
    for _ in range(game_board.width):
        board.append([None for _ in range(game_board.height)])

    if show_battleships:
        for b in game_board.battleships:
            for i, (x, y) in enumerate(b.body):
                if b.direction == "N":
                    chs = ("v", "|", "^")
                elif b.direction == "S":
                    chs = ("^", "|", "v")
                elif b.direction == "W":
                    chs = (">", "=", "<")
                elif b.direction == "E":
                    chs = ("<", "=", ">")
                else:
                    raise "Unknown direction"

                if i == 0:
                    ch = chs[0]
                elif i == len(b.body) - 1:
                    ch = chs[2]
                else:
                    ch = chs[1]
                board[x][y] = ch
    

    for sh in game_board.shots:
        x,y = sh.location
        if sh.is_hit:
            ch = "X"
        else:
            ch ="@"
        board[x][y] = ch

    for y in range(game_board.height):
        row = []
        for x in  range(game_board.width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(header)


