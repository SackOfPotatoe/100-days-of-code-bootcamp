from turtle import Turtle
from tkinter import messagebox

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.setheading(90)
        self.penup()
        self.goto(STARTING_POSITION)

    def player_hit(self):
        self.goto(STARTING_POSITION)
        if messagebox.askyesnocancel(title="Game Over",message="You've been hit by a Car!\n would you like to try again?"):
            return True
        else:
            quit()


    def move_forward(self):
        self.forward(MOVE_DISTANCE)

    def move_backwards(self):
        self.backward(MOVE_DISTANCE)

    def check_if_finished(self):
        if self.ycor() >= FINISH_LINE_Y:
            self.goto(STARTING_POSITION)
            return True


