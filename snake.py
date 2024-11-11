from turtle import Turtle, Screen
from tkinter import messagebox
from food_maker import FoodMaker
from time import sleep



class Snake:
    def __init__(self):
        self.messagebox = messagebox
        self.sleep = sleep
        self.screen = Screen()
        self.screen.bgcolor("black")
        self.screen.tracer(False)
        self.screen.setup(width=800, height=800)
        self.snake = Turtle(shape="square")
        self.snake.color("white")
        self.snake.penup()
        self.snake_body = [self.snake]
        self.x_pos = list(range(-300, 301, 20))
        self.y_pos = list(range(-300, 301, 20))
        self.food_maker = FoodMaker()
        self.screen.title("Bob's Snake Game!")

    def is_out_of_bounds(self):
        half_width = self.screen.window_width() / 2
        half_height = self.screen.window_height() / 2
        x, y = self.snake.xcor(), self.snake.ycor()
        return x < -half_width or x > half_width or y < -half_height or y > half_height

    def check_tail(self):
        tail_len = len(self.snake_body)
        for check in self.snake_body[3:tail_len]:
            if abs(self.snake.xcor() - check.xcor()) < 1 and abs(self.snake.ycor() - check.ycor()) < 1:
                messagebox.showinfo("GAME OVER!", f"You hit your tail.\nYour score: {self.food_maker.score}")
                return True



    def turn_up(self):
        if self.snake.heading() != 270:
            self.snake.setheading(90)


    def turn_down(self):
        if self.snake.heading() != 90:
            self.snake.setheading(270)


    def turn_right(self):
        if self.snake.heading() != 180:
            self.snake.setheading(0)


    def turn_left(self):
        if self.snake.heading() != 0:
            self.snake.setheading(180)
    def refresh(self):
        self.screen.clear()
        self.screen.bgcolor("black")
        self.screen.tracer(False)
        self.screen.setup(width=800, height=800)
        self.snake_body = [self.snake]
        self.snake.goto(0, 0)
        self.snake.setheading(0)
        self.food_maker.__init__()
        self.screen.title("Bob's Snake Game!")


    def run(self):
        self.food_maker.check_for_new_user()
        current_speed = 0.2
        self.snake.speed(current_speed)
        self.food_maker.add_score(0)
            # Position the initial snake body parts
        for index, body_part in enumerate(self.snake_body):
            body_part.goto(-20 * index, 0)

        self.screen.listen()
        self.screen.onkey(fun=self.turn_up, key="w")
        self.screen.onkey(fun=self.turn_down, key="s")
        self.screen.onkey(fun=self.turn_right, key="d")
        self.screen.onkey(fun=self.turn_left, key="a")

        while True:
            self.food_maker.food_check(snake=self.snake_body[0],snake_body=self.snake_body)
            if self.food_maker.check_score_level_up():
                if current_speed >= 0.01:
                    current_speed -= 0.025
                elif current_speed <= 0.01:
                    current_speed = 0.01

            self.sleep(current_speed)
            # Move the snake body parts in reverse order
            for i in range(len(self.snake_body) - 1, 0, -1):

                new_x = self.snake_body[i - 1].xcor()
                new_y = self.snake_body[i - 1].ycor()
                self.snake_body[i].goto(new_x, new_y)

            # Move the head of the snake
            self.snake_body[0].forward(20)

            self.screen.update()

            if self.is_out_of_bounds():
                self.messagebox.showinfo("Game OVER!",
                    f"You went out of bounds!\nYour total score : {self.food_maker.score}")
                self.food_maker.clear_score()
                self.food_maker.level_up = self.snake_body
                self.refresh()
                break
            if self.check_tail():
                self.food_maker.clear_score()
                self.food_maker.level_up = self.snake_body
                self.refresh()
                break

