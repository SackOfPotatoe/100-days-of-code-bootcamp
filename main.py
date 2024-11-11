from time import sleep
from turtle import Screen
from tkinter import messagebox
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
car_list = [CarManager()]
player_1 = Player()
loop = 0
spawn_speed = 8
drive_speed = 0.1
scoreboard = Scoreboard()

def spawn_cars():
    global loop
    if loop % spawn_speed == 0:
        car_list.append(CarManager())
        loop = 0


def cars_go():
    for car in car_list:
        car.car_move()
game_is_on = True


def check_for_despawn():
    for index, cars in enumerate(car_list):
        if cars.xcor() < -300:
            cars.reset()
            cars.clear()
            cars.despawn_car()
            car_list.remove(car_list[index])

def check_for_collision():
    for car in car_list:
        if car.distance(player_1) < 20:
            player_1.player_hit()
            return True

def exit_game():
    global game_is_on
    if messagebox.askyesno(title="Pause Menu", message="Would you like to \nexit the game?"):
        game_is_on = False
        quit()

screen.listen()
scoreboard.draw_score_on_screen()
while game_is_on:
    sleep(0.1)
    screen.onkey(fun=player_1.move_forward,key="w")
    screen.onkey(fun=player_1.move_backwards,key="s")
    screen.onkey(fun=exit_game,key="Escape")
    screen.update()
    cars_go()
    spawn_cars()
    check_for_despawn()
    loop += 1
    if check_for_collision():
        scoreboard.score = 1
        spawn_speed = 8
        scoreboard.draw_score_on_screen()

    if player_1.check_if_finished():
        scoreboard.score += 1
        scoreboard.draw_score_on_screen()
        if scoreboard.score % 2 == 0 and spawn_speed > 0:
            spawn_speed -= 1
            if drive_speed > 0.001: drive_speed *= 0.9
screen.exitonclick()