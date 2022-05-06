import tkinter as tk
from time import time, sleep
from random import choice, uniform, randint
from math import sin, cos, radians

GRAVITY = 0.05
colors = ['red', 'blue', 'yellow', 'white', 'green', 'orange', 'purple', 'pink']

class fireworks:
    def __init__(self, cv,mycan, idx, total, explosion_speed, x=0., y=0., vx=0., vy=0., size=2., color='red', lifespan=2):
        cv = tk.Tk()
        self.id = idx
        self.x = x
        self.y = y
        self.initial_speed = explosion_speed
        self.vx = vx
        self.vy = vy
        self.total = total
        self.age = 0
        self.color = color
        self.mycan = mycan
        self.cid = self.mycan.create_oval(
            x - size, y - size, x + size,
            y + size, fill=self.color)
        self.lifespan = lifespan

    def alive(self):
        return self.age <= self.lifespan

    def expand(self):
        return self.age <= 1.2

    def update(self, dt):
        self.age += dt

        if self.alive() and self.expand():
            move_x = cos(radians(self.id * 360 / self.total)) * self.initial_speed
            move_y = sin(radians(self.id * 360 / self.total)) * self.initial_speed
            self.mycan.move(self.cid, move_x, move_y)
            self.vx = move_x / (float(dt) * 1000)

        elif self.alive():
            move_x = cos(radians(self.id * 360 / self.total))
            self.mycan.move(self.cid, self.vx + move_x, self.vy + GRAVITY * dt)
            self.vy += GRAVITY * dt

        elif self.cid is not None:
            self.mycan.delete(self.cid)
            self.cid = None


def runner(mycan, cv):
    t = time()
    explode_points = []
    wait_time = randint(10, 100)
    numb_explode = randint(6, 10)
    for point in range(numb_explode):
        objects = []
        x_cordi = randint(50, 1000)
        y_cordi = randint(50, 550)
        speed = uniform(0.5, 1.5)
        size = uniform(0.5, 3)
        color = choice(colors)
        explosion_speed = uniform(0.2, 1)
        total_particles = randint(10, 50)
        for i in range(1, total_particles):
            r = fireworks(mycan, idx=i, total=total_particles, explosion_speed=explosion_speed, x=x_cordi, y=y_cordi,
                     vx=speed, vy=speed, color=color, size=size, lifespan=uniform(0.6, 1.75))
            objects.append(r)
        explode_points.append(objects)

    total_time = .0
    while total_time < 1.8:
        sleep(0.01)
        tnew = time()
        t, dt = tnew, tnew - t
        for point in explode_points:
            for item in point:
                item.update(dt)
        mycan.update()
        total_time += dt
    cv.after(wait_time, runner, mycan)

def main(self):
    cv = tk.Tk()
    mycan = tk.Canvas(cv, height=600, width=1024)
    mycan.create_rectangle(0, 0, 1024, 1024, fill="black")
    mycan.pack()
    cv.after(100, runner(cv), mycan)
    cv.after(8000, lambda: cv.destroy())
    cv.mainloop()