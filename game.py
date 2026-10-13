import pyxel
from table import Table
# Grade 15 x 20

class Game:
    def __init__(self):
        pyxel.init(124, 164, title = "Minesweeper", fps = 60, display_scale = 5)
        self.dif = 1
        self.style = 0
        self.table = Table(self.dif, self.style)
        
        pyxel.mouse(True)
        pyxel.load("game_art.pyxres")
        pyxel.run(self.update, self.draw)

    def save_preferences(self, dif, style):
        self.dif = dif
        self.style = style
        self.table = Table(self.dif, self.style)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.table = Table(self.dif, self.style, True)

        if pyxel.btnp(pyxel.KEY_R):
            pyxel.reset()

        if pyxel.btnp(pyxel.KEY_T) or self.table.info.btn_info[1].clicked:
            self.table = Table(self.dif, self.style)

        if self.table.arr_draw:
            self.table.arr_draw = self.table.show_empty(self.table.arr_draw[0], self.table.arr_draw[1], self.table.arr_draw[2])

        if not self.table.info.end:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                for btn in self.table.info.btn_info:
                    if self.table.info.show and self.table.collide(btn): 
                        btn.clicked = not btn.clicked
                        return
                if self.table.info.set:
                    for i in range(len(self.table.info.stars)):
                        if self.table.collide(self.table.info.stars[i]):
                            self.table.info.dif = i + 1
                            return
                    for i in range(len(self.table.info.styles)):
                        if self.table.collide(self.table.info.styles[i]):
                            self.table.info.style = i
                            return
                    for i in range(len(self.table.info.btn_conf)):
                        if self.table.collide(self.table.info.btn_conf[i]):
                            if not i: self.save_preferences(self.table.info.dif, self.table.info.style)
                            else: 
                                self.table.info.btn_info[0].clicked = False
                                self.table.info.dif = self.dif
                                self.table.info.style = self.style

                else:
                    for l in range(self.table.mine.L):
                        for c in range(self.table.mine.C):
                            if not self.table.mine.map[l][c].marked:
                                if self.table.collide(self.table.mine.map[l][c]):
                                    if not self.table.first_ck: self.table.first_ck = True; self.table.mine.init_bombs(l, c)
                                    
                                    if self.table.mine.map[l][c].clicked:
                                        self.table.show_unmarked(l, c)
                                    else:
                                        self.table.mine.map[l][c].clicked = True
                                        if not (self.table.mine.map[l][c].area_bombs or self.table.mine.map[l][c].is_bomb):
                                            self.table.arr_draw = self.table.show_empty(l, c, [])

            if self.table.first_ck and not self.table.info.set:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                    for line in self.table.mine.map:
                        for block in line:
                            if not block.clicked:
                                if self.table.collide(block):
                                    block.marked = not block.marked
                                    self.table.marks += 1 if block.marked else -1
                                    
                self.table.frame += 1
                self.table.info.time = self.table.frame//60

        self.table.info.bombs = self.table.mine.bombs - self.table.marks

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