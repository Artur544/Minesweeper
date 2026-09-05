import pyxel
import random

# Grade 15 x 20

class Block:
    def __init__(self, x, y, is_bomb, area_bombs = None):
        self.x = x
        self.y = y
        self.is_bomb = is_bomb
        self.area_bombs = area_bombs
        self.IMG, self.W, self.H = 0, 8, 8
        self.COLKEY = pyxel.COLOR_BROWN
        self.clicked, self.marked = False, False

    def draw(self):
        # pyxel.rect(self.x, self.y, 8, 8, 12)
        # pyxel.rect(self.x + 1, self.y + 1, 6, 6, 10)
        # self.u = ((pyxel.frame_count//4) % 23) * 8
        if self.marked:
            self.u = 88; self.v = 8
        elif not self.clicked:
            self.u = 80; self.v = 0
        elif self.is_bomb:
            self.u = 72; self.v = 8
        else:
            self.u = self.area_bombs * 8; self.v = 8
        pyxel.blt(self.x, self.y, self.IMG, self.u, self.v, self.W, self.H, self.COLKEY)

class Minesweeper:
    def __init__(self, dif):
        self.bombs = 12 * (2 ** dif)
        self.L, self.C = 20, 15
        self.GAP = 2
        self.map = []
        self.bombs_pos = random.sample(range(self.L * self.C), self.bombs)
        print(self.bombs_pos)
        pos = 0

        for l in range(self.L):
            self.map.append([])
            for c in range(self.C):
                if pos in self.bombs_pos:
                    self.map[l].append(Block(self.GAP + (8*c), self.GAP + (8*l), True))
                else:
                    self.map[l].append(Block(self.GAP + (8*c), self.GAP + (8*l), False))
                pos += 1

        for l in range(self.L):
            for c in range(self.C):
                if not self.map[l][c].is_bomb:
                    self.map[l][c] = Block(self.GAP + (8*c), self.GAP + (8*l), False, self.count_bombs(l, c))

    def count_bombs(self, bl, bc):
        count = 0
        min_bl = 0 if bl - 1 < 0 else bl - 1
        min_bc = 0 if bc - 1 < 0 else bc - 1
        max_bl = 20 if bl + 2 > 19 else bl + 2
        max_bc = 15 if bc + 2 > 14 else bc + 2
        for l in range(min_bl, max_bl):
            for c in range(min_bc, max_bc):
                if self.map[l][c].is_bomb:
                    count += 1
        return count

class Window:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class Game:
    def __init__(self):
        self.window = Window(124, 164)
        self.minesweeper = Minesweeper(2)
        self.GAP = self.minesweeper.GAP
        self.marks, self.defeat = 0, False
        
        pyxel.init(self.window.w, self.window.h, title = "Minesweeper", fps = 60, display_scale = 5)
        pyxel.mouse(True)
        pyxel.load("game_art.pyxres")
        pyxel.run(self.update, self.draw)

    # def collide(self, mx, my):
        # if (mx >= self.GAP and mx <= self.window.w - self.GAP) and (my >= self.GAP and my <= self.window.h - self.GAP):
        #     print(f"mx: {mx}, my: {my}")
        #     print(f"GAP: {self.GAP}")
        #     return self.minesweeper.map[(my - self.GAP - 1) // 8][(mx - self.GAP - 1) // 8]
        # else: 
        #     return False

    def collide(self, block):
        return (pyxel.mouse_x - block.x >= 0 and pyxel.mouse_x - block.x < block.W) and (pyxel.mouse_y - block.y >= 0 and pyxel.mouse_y - block.y < block.H)

    def get_area(self, bl, bc):
        min_bl = 0 if bl - 1 < 0 else bl - 1
        min_bc = 0 if bc - 1 < 0 else bc - 1
        max_bl = 20 if bl + 2 > 19 else bl + 2
        max_bc = 15 if bc + 2 > 14 else bc + 2
        return [[min_bl, max_bl], [min_bc, max_bc]]

    def show_empty(self, bl, bc, array_b = []):
        area = self.get_area(bl, bc)
        for l in range(area[0][0], area[0][1]):
            for c in range(area[1][0], area[1][1]):
                if not self.minesweeper.map[l][c].marked:
                    if not self.minesweeper.map[l][c].area_bombs:
                        if not self.minesweeper.map[l][c].clicked: array_b.append([l, c])
                    self.minesweeper.map[l][c].clicked = True
        if array_b:
            self.show_empty(array_b[0][0], array_b[0][1], array_b[1:])

    def show_unmarked(self, bl, bc):
        area = self.get_area(bl, bc); b_marked = 0
        for l in range(area[0][0], area[0][1]):
            for c in range(area[1][0], area[1][1]):
                if self.minesweeper.map[l][c].marked: b_marked += 1 
        if self.minesweeper.map[bl][bc].area_bombs == b_marked:
            for l in range(area[0][0], area[0][1]):
                    for c in range(area[1][0], area[1][1]):
                        if not self.minesweeper.map[l][c].marked: 
                            self.minesweeper.map[l][c].clicked = True

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            pyxel.reset()

        # if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # block = self.collide(pyxel.mouse_x, pyxel.mouse_y)
            # if block:
            #     l, c = block.y // block.H, block.x // block.W
            #     if not block.marked:
            #         if not block.area_bombs: self.show_empty(l, c)
            #         else: block.clicked = True
            #     print(f"l: {l}, c: {c}")
            #     print(pyxel.mouse_x, pyxel.mouse_y)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for l in range(self.minesweeper.L):
                for c in range(self.minesweeper.C):
                    if not self.minesweeper.map[l][c].marked:
                        if self.collide(self.minesweeper.map[l][c]):
                            if self.minesweeper.map[l][c].is_bomb: self.defeat = True
                            else:
                                if not self.minesweeper.map[l][c].area_bombs: 
                                    self.show_empty(l, c)
                                elif self.minesweeper.map[l][c].clicked:
                                    self.show_unmarked(l, c)
                                else: self.minesweeper.map[l][c].clicked = True

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            for line in self.minesweeper.map:
                for block in line:
                    if not block.clicked:
                        if self.collide(block):
                            block.marked = not block.marked
                            self.marks += 1 if block.marked else -1
                            print(self.marks)

    def draw(self):
        pyxel.cls(6)
        for line in self.minesweeper.map:
            for block in line:
                block.draw()

        if self.defeat:
            pos = 0
            for line in self.minesweeper.map:
                for block in line:
                    if pos in self.minesweeper.bombs_pos:
                        block.clicked = True
                    pos += 1
        else:
            if self.marks == self.minesweeper.bombs:
                ver = True
                for line in self.minesweeper.map:
                    for block in line:
                        if not (block.marked or block.is_bomb): ver = False
                if ver: pyxel.text(62, 82, "Venceu", 5, font=None)

Game()