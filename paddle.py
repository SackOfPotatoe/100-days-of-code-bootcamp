from time import sleep
from turtle import Turtle, Screen


class Paddle:


    def __init__(self):
        self.sleep = sleep
        self.center_line = Turtle()
        self.screen = Screen()
        self.left_paddle = []
        self.right_paddle = []



    def make_center_line(self):
        self.screen.tracer(False)
        self.center_line.pencolor("white")
        self.center_line.pensize(5)
        self.center_line.hideturtle()
        self.center_line.teleport(0,-400)
        self.center_line.setheading(90)
        while self.center_line.ycor() < 350:
            self.center_line.pendown()
            self.center_line.forward(20)
            self.center_line.penup()
            self.center_line.forward(20)
            self.screen.update()



    def make_paddles(self):
        right_y_pos = 40
        for _ in range(5):
            paddle_piece = Turtle(shape="square")
            paddle_piece.color("white")
            paddle_piece.penup()
            paddle_piece.goto(400,right_y_pos)
            self.right_paddle.append(paddle_piece)
            right_y_pos -= 20
        left_y_pos = 40
        for _ in range(5):
            paddle_piece = Turtle(shape="square")
            paddle_piece.color("white")
            paddle_piece.penup()
            paddle_piece.goto(-400,left_y_pos)
            self.left_paddle.append(paddle_piece)
            left_y_pos -= 20


    def right_paddle_up(self):
        if self.right_paddle[0].ycor() < 250:
            for part in range(len(self.right_paddle)-1, 0, -1):
                new_x = self.right_paddle[part - 1].xcor()
                new_y = self.right_paddle[part - 1].ycor()
                self.right_paddle[part].goto(new_x, new_y)
            self.right_paddle[0].setheading(90)
            self.right_paddle[0].forward(20)

    def right_paddle_down(self):
        if self.right_paddle[0].ycor() > -160:
            for part in range(len(self.right_paddle) -1):
                new_x = self.right_paddle[part + 1].xcor()
                new_y = self.right_paddle[part + 1].ycor()
                self.right_paddle[part].goto(new_x, new_y)
            self.right_paddle[-1].setheading(270)
            self.right_paddle[-1].forward(20)

    def controller(self):
        while True:
            print("wtf how")
            self.screen.listen()
            self.screen.onkeypress(fun=self.right_paddle_up, key="w")

    def left_paddle_up(self):
        if self.left_paddle[0].ycor() < 250:
            for part in range(len(self.right_paddle) - 1, 0, -1):
                new_x = self.left_paddle[part - 1].xcor()
                new_y = self.left_paddle[part - 1].ycor()
                self.left_paddle[part].goto(new_x, new_y)
            self.left_paddle[0].setheading(90)
            self.left_paddle[0].forward(20)

    def left_paddle_down(self):
        if self.left_paddle[0].ycor() > -160:
            for part in range(len(self.left_paddle) - 1):
                new_x = self.left_paddle[part + 1].xcor()
                new_y = self.left_paddle[part + 1].ycor()
                self.left_paddle[part].goto(new_x, new_y)
            self.left_paddle[-1].setheading(270)
            self.left_paddle[-1].forward(20)

    def check_right_paddle_cor(self):
        y_positions = [piece.ycor() for piece in self.right_paddle]
        return min(y_positions) -5, max(y_positions) +5
    def check_left_paddle_cor(self):
        y_positions = [piece.ycor() for piece in self.left_paddle]
        return min(y_positions), max(y_positions)
