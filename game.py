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
        pyxel.blt(self.x, self.y, self.IMG, self.u, self.v, self.W, self.H)

class Minesweeper:
    def __init__(self, dif, debug):
        self.bombs = 12 * (2 ** dif)
        self.L, self.C = 20, 15
        self.GAP = 2
        self.map = []
        if not debug:
            self.bombs_pos = random.sample(range(self.L * self.C), self.bombs)
        else: 
            self.bombs_pos = [148, 265, 255, 45, 225, 261, 21, 172, 206, 103, 202, 253, 131, 130, 19, 183, 86, 38, 123, 134, 282, 143, 263, 119, 163, 26, 17, 201, 241, 230, 113, 275, 114, 224, 124, 132, 11, 127, 14, 36, 285, 194, 178, 39, 126, 2, 156, 212]
        print(f"\n\nBombas Array: {self.bombs_pos}\n\n")
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

class Button:
    def __init__(self, x, y, u, v):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.IMG = 0
        self.W, self.H = 13, 13
        self.COLKEY = pyxel.COLOR_BLACK
        self.clicked = False

    def draw(self):
        pyxel.blt(self.x, self.y, self.IMG, self.u, self.v, self.W, self.H, self.COLKEY)

class Info:
    def __init__(self, bombs, dif):
        self.bombs = bombs
        self.dif = dif
        self.time = 0
        self.end = ""
        self.show = False
        self.mode = 1
        self.buttons = [
            Button(32 + ((pyxel.width - 4) / 4 - 13) / 2, 6, 32, 24),
            Button(62 + ((pyxel.width - 4) / 4 - 13) // 2, 6, 64, 24)
        ]
        print(pyxel.FONT_WIDTH)

    def show_info(self):
        txt_time = f"{self.time//60:02d}:{self.time%60:02d}"
        pyxel.rect(2, 2, pyxel.width - 4, 21, 6)
        pyxel.rectb(2, 2, pyxel.width - 4, 21, 1)
        y_all = 2 + (21 - pyxel.FONT_HEIGHT) / 2
        w_all = pyxel.FONT_WIDTH * len(str(txt_time)) + 3
        x_tit = 34 + (56 - pyxel.FONT_WIDTH * 7) / 2
        x_time = 10
        # x_time = 2 + ((pyxel.width - 4) / 4 - pyxel.FONT_WIDTH * len(str(txt_time))) / 2
        # x_bomb = 92 + ((pyxel.width - 4) / 4 - pyxel.FONT_WIDTH * len(str(self.bombs))) / 2
        x_rbomb = 83 + ((pyxel.width - 4) / 4 - pyxel.FONT_WIDTH * len(txt_time))
        x_tbomb = x_rbomb + (w_all - pyxel.FONT_WIDTH * len(str(self.bombs))) / 2
        pyxel.rect(x_time - 2, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 12)
        pyxel.rect(x_rbomb, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 12)
        pyxel.rectb(x_time - 2, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 1)
        pyxel.rectb(x_rbomb, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 1)
        pyxel.text(x_time, y_all, txt_time, 1, font=None)
        pyxel.text(x_tbomb, y_all, f"{self.bombs}", 1, font=None)
        for button in self.buttons: button.draw()

    def results(self):
        txt_time = f"{self.time//60:02d}:{self.time%60:02d}"
        if self.dif <= 1: txt_dif = "FACIL"
        elif self.dif == 2: txt_dif = "MEDIO"
        else: txt_dif = "DIFICIL"
        pyxel.rect(29, 61, 66, 42, 6)
        pyxel.rectb(29, 61, 66, 42, 1)
        x_tit = 30 + (66 - pyxel.FONT_WIDTH * 7) / 2
        x_tall = 34
        x_ctime = 59 + (32 - pyxel.FONT_WIDTH * len(txt_time))
        x_cbomb = 59 + (32 - pyxel.FONT_WIDTH * len(str(self.bombs)))
        x_cdif = 59 + (32 - pyxel.FONT_WIDTH * len(txt_dif))
        pyxel.text(x_tall, 77, "TEMPO:", 5, font=None)
        pyxel.text(x_ctime, 77, txt_time, 5, font=None)
        pyxel.text(x_tall, 85, "BOMBAS:", 5, font=None)
        pyxel.text(x_cbomb, 85, f"{self.bombs}", 5, font=None)
        pyxel.text(x_tall, 93, "MODO:", 5, font=None)
        pyxel.text(x_cdif, 93, txt_dif, 5, font=None)
        if self.end == "V":
            pyxel.text(x_tit, 66, "VITORIA", 11, font=None)
        elif self.end == "D":
            pyxel.text(x_tit, 66, "DERROTA", 8, font=None)

    def settings(self):
        txt_time = f"{self.time//60:02d}:{self.time%60:02d}"
        pyxel.rect(34, 62, 56, 40, 6)
        pyxel.rectb(34, 62, 56, 40, 1)
        x_tit = 34 + (56 - pyxel.FONT_WIDTH * 7) / 2
        x_ttime = 34 + (28 - pyxel.FONT_WIDTH * 5) / 2
        x_tbomb = 62 + (28 - pyxel.FONT_WIDTH * 6) / 2
        x_ctime = 34 + (28 - pyxel.FONT_WIDTH * len(txt_time)) / 2
        x_cbomb = 62 + (28 - pyxel.FONT_WIDTH * len(str(self.bombs))) / 2
        pyxel.text(x_ttime, 82, "TEMPO", 5, font=None)
        pyxel.text(x_tbomb, 82, "BOMBAS", 5, font=None)
        pyxel.text(x_ctime, 90, txt_time, 5, font=None)
        pyxel.text(x_cbomb, 90, f"{self.bombs}", 5, font=None)
        if self.end == "V":
            pyxel.text(x_tit, 70, "VITORIA", 11, font=None)
        elif self.end == "D":
            pyxel.text(x_tit, 70, "DERROTA", 8, font=None)

    def draw(self):
        if pyxel.mouse_wheel < 0: self.show = True
        elif pyxel.mouse_wheel > 0: self.show = False

        if not self.end:
            if self.show:
                self.show_info()
                if self.buttons[0].clicked: self.settings()
        else:
            self.results()

class Table:
    def __init__(self, debug = False):
        self.mine = Minesweeper(1, debug)
        self.info = Info(self.mine.bombs, 1)
        self.GAP = self.mine.GAP
        self.first_ck, self.defeat = False, False
        self.marks, self.frame = 0, 0

    def collide(self, block):
        return (pyxel.mouse_x - block.x >= 0 and pyxel.mouse_x - block.x < block.W) and (pyxel.mouse_y - block.y >= 0 and pyxel.mouse_y - block.y < block.H)

    # def ver_empty_unmarked(self, bl, bc, ver = False):
    #     if ver:
    #         if not (self.minesweeper.map[bl][bc].area_bombs or self.minesweeper.map[bl][bc].is_bomb):
    #             self.show_empty(bl, bc)
    #         elif self.minesweeper.map[bl][bc].clicked:
    #             self.show_unmarked(bl, bc)
    #         else: self.minesweeper.map[bl][bc].clicked = True
    #     else: self.minesweeper.map[bl][bc].clicked = True

    def get_area(self, bl, bc):
        min_bl = 0 if bl - 1 < 0 else bl - 1
        min_bc = 0 if bc - 1 < 0 else bc - 1
        max_bl = 20 if bl + 2 > 19 else bl + 2
        max_bc = 15 if bc + 2 > 14 else bc + 2
        return [[min_bl, max_bl], [min_bc, max_bc]]

    def show_empty(self, bl, bc, array_b):
        area = self.get_area(bl, bc)
        for l in range(area[0][0], area[0][1]):
            for c in range(area[1][0], area[1][1]):
                if not self.mine.map[l][c].marked:
                    if not self.mine.map[l][c].area_bombs:
                        if not self.mine.map[l][c].clicked: 
                            array_b.append([l, c])
                    self.mine.map[l][c].clicked = True
        if array_b:
            return self.show_empty(array_b[0][0], array_b[0][1], array_b[1:])

    def show_unmarked(self, bl, bc):
        area = self.get_area(bl, bc); b_marked = 0
        for l in range(area[0][0], area[0][1]):
            for c in range(area[1][0], area[1][1]):
                if self.mine.map[l][c].marked: b_marked += 1 
        if self.mine.map[bl][bc].area_bombs == b_marked:
            for l in range(area[0][0], area[0][1]):
                for c in range(area[1][0], area[1][1]):
                    if not self.mine.map[l][c].marked:
                        if not self.mine.map[l][c].area_bombs: self.show_empty(l, c, [])
                        else: self.mine.map[l][c].clicked = True

class Game:
    def __init__(self):
        pyxel.init(124, 164, title = "Minesweeper", fps = 60, display_scale = 5)

        self.table = Table()
        pyxel.mouse(True)
        pyxel.load("game_art.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.table = Table(True)

        if pyxel.btnp(pyxel.KEY_R):
            pyxel.reset()

        if pyxel.btnp(pyxel.KEY_T) or self.table.info.buttons[1].clicked:
            self.table = Table()

        if not self.table.info.end:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                for btn in self.table.info.buttons:
                    if self.table.collide(btn): 
                        btn.clicked = not btn.clicked
                        return
                for l in range(self.table.mine.L):
                    for c in range(self.table.mine.C):
                        if not self.table.mine.map[l][c].marked:
                            if self.table.collide(self.table.mine.map[l][c]):
                                self.table.first_ck = True
                                # self.ver_empty_unmarked(l, c)
                                if self.table.mine.map[l][c].clicked:
                                    self.table.show_unmarked(l, c)
                                else: 
                                    self.table.mine.map[l][c].clicked = True
                                    if not (self.table.mine.map[l][c].area_bombs or self.table.mine.map[l][c].is_bomb):
                                        self.table.show_empty(l, c, [])

            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                for line in self.table.mine.map:
                    for block in line:
                        if not block.clicked:
                            if self.table.collide(block):
                                block.marked = not block.marked
                                self.table.marks += 1 if block.marked else -1

        self.table.info.bombs = self.table.mine.bombs - self.table.marks

        if self.table.first_ck and not self.table.info.end: 
            self.table.frame += 1
            self.table.info.time = self.table.frame//60

    def draw(self):
        pyxel.cls(6)

        for line in self.table.mine.map:
            for block in line:
                if block.is_bomb and block.clicked: self.table.defeat = True
                block.draw()

        self.table.info.draw()

        count = 0
        if self.table.defeat:
            for line in self.table.mine.map:
                for block in line:
                    if count in self.table.mine.bombs_pos:
                        block.clicked = True
                    count += 1
            self.table.info.end = "D"
        else:
            ver = True
            for line in self.table.mine.map:
                for block in line:
                    if self.table.info.bombs: ver = False
                    elif block.marked and not block.is_bomb: ver = False
                    if block.clicked: count += 1
            if count == 300 - self.table.mine.bombs: ver = True
            if ver: 
                self.table.info.end = "V"

Game()