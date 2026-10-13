import pyxel

class Button:
    def __init__(self, x, y, u, v, w, h):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.IMG = 0
        self.W = w
        self.H = h
        self.COLKEY = pyxel.COLOR_BROWN
        self.clicked = False

    def draw(self):
        pyxel.blt(self.x, self.y, self.IMG, self.u, self.v, self.W, self.H, self.COLKEY)

class Info:
    def __init__(self, bombs, dif, style):
        self.bombs = bombs
        self.dif = dif
        self.style = style
        self.time = 0
        self.end = ""
        self.show = False
        self.set = False
        self.btn_info = [
            Button(32 + ((pyxel.width - 4) / 4 - 13) / 2, 6, 32, 24, 13, 13),
            Button(62 + ((pyxel.width - 4) / 4 - 13) // 2, 6, 64, 24, 13, 13)
        ]
        self.btn_conf = [
            Button(39, 105, 96, 24, 31, 13),
            Button(72, 105, 128, 24, 13, 13)
        ]
        self.stars = [
            Button(64, 66, 0, 40, 8, 8),
            Button(73, 66, 0, 40, 8, 8),
            Button(82, 66, 0, 40, 8, 8),
        ]
        self.styles = [
            Button(35, 75, 0, 56, 24, 24),
            Button(65, 75, 24, 56, 24, 24)
        ]

    def show_info(self):
        txt_time = f"{self.time//60:02d}:{self.time%60:02d}"
        pyxel.rect(2, 2, pyxel.width - 4, 21, 6)
        pyxel.rectb(2, 2, pyxel.width - 4, 21, 1)
        y_all = 2 + (21 - pyxel.FONT_HEIGHT) / 2
        w_all = pyxel.FONT_WIDTH * len(str(txt_time)) + 3
        x_time = 10
        x_rbomb = 83 + ((pyxel.width - 4) / 4 - pyxel.FONT_WIDTH * len(txt_time))
        x_tbomb = x_rbomb + (w_all - pyxel.FONT_WIDTH * len(str(self.bombs))) / 2
        pyxel.rect(x_time - 2, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 12)
        pyxel.rect(x_rbomb, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 12)
        pyxel.rectb(x_time - 2, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 1)
        pyxel.rectb(x_rbomb, y_all - 2, w_all, pyxel.FONT_HEIGHT + 3, 1)
        pyxel.text(x_time, y_all, txt_time, 1, font=None)
        pyxel.text(x_tbomb, y_all, f"{self.bombs}", 1, font=None)
        for btn in self.btn_info: btn.draw()

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
        pyxel.rect(29, 53, 25, 8, 6)
        pyxel.rectb(29, 53, 25, 8, 1)
        pyxel.rect(29, 61, 66, 42, 6)
        pyxel.rectb(29, 61, 66, 42, 1)
        pyxel.rect(30, 54, 23, 9, 6)
        self.general_tab()

    def general_tab(self):
        txt_time = f"{self.time//60:02d}:{self.time%60:02d}"
        x_tall = 34
        x_tset = 29 + (25 - pyxel.FONT_WIDTH * 5) / 2
        x_ttime = 34 + (28 - pyxel.FONT_WIDTH * 5) / 2
        x_tbomb = 62 + (28 - pyxel.FONT_WIDTH * 6) / 2
        x_cbomb = 62 + (28 - pyxel.FONT_WIDTH * len(str(self.bombs))) / 2
        pyxel.text(x_tset, 55, "GERAL", 5, font=None)
        pyxel.text(x_tall, 67, "MODO:", 5, font=None)
        self.stars_display(self.dif)
        self.styles_display(self.style)
        for btn in self.btn_conf: btn.draw()

    def stars_display(self, dif):
        for i in range(len(self.stars)):
            if i < dif: self.stars[i].u = 8 * dif
            else: self.stars[i].u = 0
            self.stars[i].draw()

    def styles_display(self, style):
        for i in range(len(self.styles)):
            if i == style:
                pyxel.rectb(self.styles[i].x-1, self.styles[i].y-1, self.styles[i].W+2, self.styles[i].H+2, 5)
            self.styles[i].draw()

    def draw(self):
        if pyxel.mouse_wheel < 0: self.show = True
        elif pyxel.mouse_wheel > 0: 
            self.show = False
            self.set = False
            self.btn_info[0].clicked = False

        if not self.end:
            if self.show:
                self.show_info()
                self.set = True if self.btn_info[0].clicked else False
                if self.set: self.settings()
        else:
            self.results()
