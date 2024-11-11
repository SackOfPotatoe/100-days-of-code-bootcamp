from turtle import Turtle
from time import sleep
import random

from player import MOVE_DISTANCE

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 10
MOVE_INCREMENT = 10


class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.random = random
        self.shape("square")
        self.color(random.choice(COLORS))
        self.penup()
        self.rand_pos = [i for i in range(-160,261,20)]
        self.teleport(x=300,y=self.random.choice(self.rand_pos))
        self.setheading(180)
        self.shapesize(stretch_wid=1,stretch_len=2)

    def despawn_car(self):
        self.reset()
        self.clear()
        self.hideturtle()

    def car_move(self):
        self.forward(STARTING_MOVE_DISTANCE)

