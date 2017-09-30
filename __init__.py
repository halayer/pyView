"""
pyView - python 3D engine

A 3D engine that works in a tkinter.Canvas
widget without pygame.
Bases on the python standard library.
"""

import os
import mapsOpener
import tkinter as tk
import tkinter.messagebox as msgBox
import threading
import json
import math


root = tk.Tk()

with open("./objects/cube.obj") as file:
    data = file.read()
    data = json.loads(data)

    verts = data["verts"]

    edges = data["edges"]

def rotate2D(pos, rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)

    return x * c - y * s, y * c + x * s


class cam:
    """ Game camera. """

    def __init__(self, pos=(0, 0 ,0), rot=(0, 0)):
        self.pos = list(pos)
        self.startPos = list(pos)
        self.rot = list(rot)
        self.startRot = list(rot)
        
    def update(self, key):
        global radian
        
        s = dt * 10

        if key.keysym == "Left": self.rot[1] += radian
        if key.keysym == "Right": self.rot[1] -= radian
        if key.keysym == "Up": self.rot[0] += radian
        if key.keysym == "Down": self.rot[0] -= radian
        
        if key.keysym == "q": self.pos[1] += s
        if key.keysym == "e": self.pos[1] -= s

        x, y = s * math.sin(self.rot[1]), s * math.cos(self.rot[1])

        if key.keysym == "w": self.pos[0] += x; self.pos[2] += y
        if key.keysym == "s": self.pos[0] -= x; self.pos[2] -= y
        if key.keysym == "a": self.pos[0] -= y; self.pos[2] += x
        if key.keysym == "d": self.pos[0] += y; self.pos[2] -= x

        if key.keysym == "r":
            self.pos = self.startPos.copy()
            self.rot = self.startRot.copy()

        if key.keysym == "h": self._help()

        render()

    def _help(self):
        msgBox.showinfo("pyView", """
Controls:

Q/E                 Move object up/down
WASD                Move object
Up/Down/Left/Right  Rotate object
R                   Reset
H                   Help
Esc                 Exit fullscreen
F11                 Fullscreen
""")


class cube:
    edges = edges

    verticies = verts

    def __init__(self, pos=(0, 0, 0)):
        x, y, z = pos

        self.verts = [(x + X, y + Y, z + Z) for X, Y, Z in self.verticies]


def render():
    can.delete("all")

    for obj in cubes:
    
        for edge in obj.edges:
            points = list()
            
            for x, y, z in (obj.verts[edge[0]], obj.verts[edge[1]]):
                x -= Cam.pos[0]
                y -= Cam.pos[1]
                z -= Cam.pos[2]

                x, z = rotate2D((x, z), Cam.rot[1])
                y, z = rotate2D((y, z), Cam.rot[0])
                
                z += 5

                f = 200 / z

                x, y = x * f, y * f

                points += [(cX + int(x), cY + int(y))]

            can.create_line(points[0], points[1])
        

def rbg(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def fullScreen(event=None): # Event is unused
    global fS
    
    if fS:
        root.attributes("-fullscreen", False)

        fS = False
    elif fS == False:
        root.attributes("-fullscreen", True)

        fS = True

cubes = list()

with open(mapsOpener.openMap(), "r") as file:
    data = file.read()
    data = json.loads(data)

    for dat in data:
        cubes.append(cube((dat[0], dat[1], dat[2])))

WIDTH, HEIGHT = 1680, 1050; cX, cY = WIDTH // 2, HEIGHT // 2
        

radian = 0

dt = 0.06

fS = True

radian += dt

Cam = cam((0, 0, -5))

root.title("pyView - 3D engine")

root.attributes("-fullscreen", True)

root.bind("<Key>", Cam.update)
root.bind("<Escape>", lambda event: root.destroy())
root.bind("<F11>", lambda event: fullScreen())

can = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=rbg(255, 255, 255))
can.pack()

render()

root.mainloop()
