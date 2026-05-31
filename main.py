import random

WIDTH = 10
HEIGHT = 10

class Battleship:
    @staticmethod
    def build(head, length , direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1]-i)
            elif direction == "S":
                el = (head[0], head[1]+ i)
            elif direction == "W":
                el = (head[0]- i, head[1])
            elif direction =="E":
                el = (head[0]+ i , head[1])
            body.append(el)
        return Battleship(body, direction)
    
    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
        self.hits = [False] * len(body)

    def body_index(self, lcoation):
        try:
            return self.body.index(location)
        except ValueError:
            return None
        
    def is_destroyed(self):
        return all(self.hits)
    
    def __repr__(self):
        status = "SUNK" if self.is_destroyed() else f" {sum(self.hits)}/{len(self.body)} hit"
        return f"<Ship dir = {self.direction} len={len(self.body)} [{status}]>"
    
class Shot:
    def __init__(self, battleships, width=WIDTH, height=HEIGHT):
        self.battleships = battleships
        self.shots = []
        self.width = width
        self.height = height

    def aleady_shot(self, location):
        return any(s.location == location for s in self.shots)
    
    def take_shot(self, location):
        hit_ship = None
        was_destroyed = False
        is_hit = False

        for ship in self.battleships:
            idx = ship.body_index(location)
            if idx is not None:
                is_hit = True
                ship.hits[idx] = True
                hit_ship = ship
                was_destroyed = ship.is_destroyed()
                break
        
        self.shots.append(Shot(location, is_hit))
        return hit_ship, was_destroyed
    def is_game_over(self):
        return all(ship.is_destryoed() for ship in self.battleships)
    

def render(board, show_ships=False, label=""):
    if label:
        print(f"\n {label}")

    print("  " + " ".join(str(x) for x in range(board.width)))
    print("  " + "-" * (board.width * 2 -1) + "+")

    grid = [["." for _ in range(board.width)] for _ in range(board.height)]

    if show_ships:
        for ship in board.battleships:
            for i, (x, y) in enumerate(ship.body):
                # Pick character based on direction and position in body
                if ship.direction == "N":
                    chs = ("v", "|", "^")
                elif ship.direction == "S":
                    chs = ("^", "|", "v")
                elif ship.direction == "W":
                    chs = (">", "=", "<")
                else:  # E
                    chs = ("<", "=", ">")
 
                if i == 0:
                    ch = chs[0]
                elif i == len(ship.body) - 1:
                    ch = chs[2]
                else:
                    ch = chs[1]
 
                grid[y][x] = "X" if ship.hits[i] else ch

    for shot in board.shots:
        x,y = shot.location
        if shot.is_hit:
            grid[y][x] = "X"
        else:
            grid[y][x] = "o"

    for y in range(board.height):
        row = " ".join(grid[y])
        print(f" {y} | {row}")

    print("  +" + "-" * (board.width * 2 -1) + "+")
    

def announce(event, player=" "):
    if event == "new_turn":
        print(f"\n{'-'*40}\n {player}'s turn")
    elif event == "miss":
        print(f"  {player} missed")
    elif event == "hit":
        print(f"  {player} HIT a ship!!")
    elif event == "destroyed":
        print(f" {player} SANK a ship!!")
    elif event == "game_over":
        print(f"\n *** {player} WINS!!! *** \n")
    elif event == "duplicate":
        print("  Already shot there - skipping.")


# ai player ( js random shot taking btw lol)

def ai_random_shot(board):
    while True:
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        if not board.already_shot((x,y)):
            return (x,y)
        


#some hardcoded fleet

def build_demo_fleet():
    return [
        Battleship.build((1,1), 2, "E"),
        Battleship.build((5,3), 4 , "S"),
        Battleship.build((2,7), 3, "E"),
        Battleship.build((7,0), 5, "N")
    ]


# main loopy
def main():
    print("BATLESHIPS")
    print(" for now RANDOM AI FIRING AT A FLEET.\n")

    board = GameBoard(build_demo_fleet())

    print("Starting board (ships revealed):")
    render(board, show_ships= True, label = "Fleet positions: ")

    input("/n Press ENTER to start...\n")

    turn = 1
    while not board.is_game_over():
        announce("new_turn", playe=f"AI (turn{turn})")

        shot = ai_random_shot(board)
        print(f" Firing at {shot}")

        hit_ship, was_destroyed = board.take_shot(shot)

        if hit_ship is None:
            announce("miss", player = "AI")
        elif was_destroyed:
            announce("destroyed", player = "AI")
        else:
            announce("hit", player = "AI")

        render(board, show_tips = True)
        turn += 1

        input(" (press ENTER for next turn)")

    announce("game_over", player = "AI")
    print(f" Finished in {turn - 1} turns.")

if __name__ == "__main__":
    main()