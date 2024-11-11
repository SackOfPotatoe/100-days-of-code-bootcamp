from filecmp import clear_cache
import sys
from snake import Snake
from tkinter import messagebox

snake_game = Snake()


def start_game():
    snake_game.run()
    clear_cache()
while True:
    option = messagebox.askquestion(title="Snake Game",message="Would you like to play Snake?\n"
                                                               "            up = W,\n"
                                                               "left = A, down = S, right = D")
    if option == "yes":
        start_game()
    elif option == "no":
        sys.exit()
