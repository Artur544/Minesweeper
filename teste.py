import pyxel
import random
from math import sqrt

pyxel.init(160, 120)

RADIUS = 5
COLOR = pyxel.COLOR_DARK_BLUE
STEP = 2
pyxel.x1 = random.uniform(20, 140)
pyxel.y1 = random.uniform(20, 140)
pyxel.sleep1 = False
pyxel.x2 = random.uniform(20, 140)
pyxel.y2 = random.uniform(20, 140)
pyxel.sleep2 = False
pyxel.x3 = random.uniform(20, 140)
pyxel.y3 = random.uniform(20, 140)
pyxel.sleep3 = False

def in_circle(x, y, cx, cy):
    dist = sqrt((x - cx) ** 2 + (y - cy) ** 2)
    return dist <= RADIUS

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        if in_circle(pyxel.mouse_x, pyxel.mouse_y, pyxel.x1, pyxel.y1):
            pyxel.sleep1 = not pyxel.sleep1
        if in_circle(pyxel.mouse_x, pyxel.mouse_y, pyxel.x2, pyxel.y2):
            pyxel.sleep2 = not pyxel.sleep2
        if in_circle(pyxel.mouse_x, pyxel.mouse_y, pyxel.x3, pyxel.y3):
            pyxel.sleep3 = not pyxel.sleep3


    if not pyxel.sleep1:
        pyxel.x1 += random.uniform(-STEP, STEP)
        pyxel.y1 += random.uniform(-STEP, STEP)
    if not pyxel.sleep2:
        pyxel.x2 += random.uniform(-STEP, STEP)
        pyxel.y2 += random.uniform(-STEP, STEP)
    if not pyxel.sleep3:
        pyxel.x3 += random.uniform(-STEP, STEP)
        pyxel.y3 += random.uniform(-STEP, STEP)

def draw():
    pyxel.cls(pyxel.COLOR_BLACK)
    pyxel.circ(pyxel.x1, pyxel.y1, RADIUS, COLOR)
    pyxel.circ(pyxel.x2, pyxel.y2, RADIUS, COLOR)
    pyxel.circ(pyxel.x3, pyxel.y3, RADIUS, COLOR)

pyxel.mouse(True)
pyxel.run(update, draw)