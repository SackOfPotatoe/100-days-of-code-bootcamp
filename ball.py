import random
from time import sleep
from turtle import Turtle
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.rand_direction_y = [10,-10]
        self.rand_direction_x = [10, -10]
        self.x_direction = random.choice(self.rand_direction_x)
        self.y_direction = random.choice(self.rand_direction_y)

    def move(self):
        new_x = self.xcor() + self.x_direction
        new_y = self.ycor() + self.y_direction
        self.goto(new_x, new_y)

    def bounce(self, x_is_true_or_false, y_is_true_or_false):
        if y_is_true_or_false:
            self.y_direction *= -1
        if x_is_true_or_false:
            self.x_direction *= -1
    def ball_reset(self):
        self.reset()
        sleep(0.5)
        self.__init__()

