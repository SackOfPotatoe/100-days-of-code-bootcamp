from turtle import Turtle,Screen
import json
import random
import sys
import os
high_score = 0
user_name = "Users name"
# Determine the base path
if getattr(sys, 'frozen', False):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
else:
    base_path = os.path.abspath(".")

# Construct the full path to the game_data.json file
game_data_path = os.path.join(base_path, "game_data.json")

# Read the game_data.json file with error handling
try:
    with open(game_data_path, "r") as game_data:
        data = json.load(game_data)
        user_name = data.get("user_name", user_name)
        high_score = data.get("high_score", str (high_score))
except FileNotFoundError:
    print(f"Error: {game_data_path} not found.")
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from {game_data_path}.")



screen = Screen()
class FoodMaker:
    def __init__(self):
        self.user_name_input = user_name
        self.food_maker = Turtle("square")
        self.food_maker.penup()
        self.food_maker.color("white")
        self.food = 3
        self.no_food = True
        self.x_pos = list(range(-300, 301, 20))
        self.y_pos = list(range(-300, 301, 20))
        self.random = random
        self.score = 0
        self.level_up = 300
        self.score_display = Turtle()
        self.score_display.hideturtle()
        self.score_display.pencolor("White")
        self.score_display.teleport(0,320)
        self.score_display.write(f"Score : {self.score}\nHigh Score: {user_name} {high_score}", False, "center",
                                 font=("Arial", 22, "bold"))
    def check_for_new_user(self):
        global user_name
        self.user_name_input = screen.textinput(title="User name", prompt="Please type your name or UserName\nto save your high score")


    def add_score(self, input_score):
        self.score += input_score
        self.score_display.clear()
        self.score_display.write(f"Score : {self.score}\nHigh Score: {user_name} {high_score}",False,"center",font=("Arial", 22 ,"bold"))

    def check_score_level_up(self):
        if self.score > self.level_up:
            self.level_up *= 1.6
            return True
    def clear_score(self):
        global high_score
        global user_name
        if self.score > int(high_score):
            user_name = self.user_name_input
            high_score = self.score
            with open("game_data.json", "w") as save_game:
                json.dump({"user_name": str(user_name), "high_score": str(high_score)}, save_game)

        self.score = 0

    def food_check(self, snake, snake_body):

        while True:

            if self.no_food:
                self.food_maker.goto(self.random.choice(self.x_pos), self.random.choice(self.y_pos))
                self.no_food = False
            if (abs(snake.xcor() - self.food_maker.xcor()) < 18
                    and
                    abs(snake.ycor() - self.food_maker.ycor()) < 18):
                self.add_score(100)
                self.food += 1
                self.no_food = True
            if self.food > 0:
                for _ in range(self.food):
                    body_part = Turtle(shape="square")
                    body_part.penup()
                    body_part.color("white")
                    snake_body.append(body_part)
                    self.food -= 1

            return