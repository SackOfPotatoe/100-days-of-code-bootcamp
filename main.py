from os.path import split
from turtle import Screen,Turtle
from tkinter import messagebox
from time import sleep

import pandas
draw = Turtle()
draw.hideturtle()
draw.penup()
screen = Screen()
screen.title("U.S States Game")
screen.setup(width=725,height=491)
screen.bgpic("blank_states_IMG.gif")
states_dict = pandas.read_csv("50_states.csv").set_index("state")[["x","y"]].T.to_dict("list")
game_is_on = True
guessed_states = []

while game_is_on:
    user_input = screen.textinput(f"States Guessed {len(guessed_states)}/{len(states_dict)}",
                                  "See if you can guess all the states!").title()

    if user_input in states_dict:
        draw.goto(states_dict[user_input])
        draw.write(user_input,move=True,align="center",font=("Arial",12,"bold"))
        guessed_states.append(user_input)
    elif user_input not in states_dict:
        draw.goto(0,0)
        draw.write(f"{user_input} was a wrong guess!\nBetter luck next time.",align="center"
                   ,font=("Arial",18,"bold"))

        sleep(5)
        if messagebox.askyesno(title="Game Over",message="Would you like to try again?"):
            game_is_on = True
        else:
            game_is_on = False
pandas.DataFrame(guessed_states).to_csv("guessed_states.csv",index=False,header=False)
quit()

