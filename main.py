from turtle import Screen
from tkinter import messagebox
from score_bored import ScoreBored
from paddle import Paddle
from ball import Ball
from time import sleep

game_started = True
game_over = False
screen = Screen()
score_bored = ScoreBored()
paddle = Paddle()
ball = Ball()
ball_st_speed = 0.07
ball_speed = 0

def start_screen():
    global game_started
    global ball_speed
    if game_started:
        screen.bgcolor("black")
        screen.setup(width=900,height=600)
        score_bored.draw_score()
        paddle.make_paddles()
        paddle.make_center_line()
        game_started = False
        ball_speed = ball_st_speed
    return
def close_game():
    if messagebox.askyesno(title="Exit game", message="Would you like to exit?\n "):
        global game_over
        game_over = True
        quit()

def run():
    global ball_speed
    global ball_st_speed
    ball_speed = 0.07

    start_screen()
    screen.listen()


    while True:

        screen.onkey(fun=paddle.right_paddle_up,key="o")
        screen.onkey(fun=paddle.right_paddle_down, key="l")
        screen.onkey(fun=paddle.left_paddle_up, key="w")
        screen.onkey(fun=paddle.left_paddle_down, key="s")
        screen.onkey(fun=close_game, key="Escape")
        screen.update()
        sleep(ball_speed)
        ball.move()
        if ball.ycor() >= 250 or ball.ycor() <= -250:
            ball.bounce(False,True)

        r_pad_min, r_pad_max = paddle.check_right_paddle_cor()
        l_pad_min, l_pad_max = paddle.check_left_paddle_cor()
        if ball.xcor() >= 380 and r_pad_min <= ball.ycor() <= r_pad_max:
            # This is for the right side checks.
            if ball.xcor() < 400:
                ball.bounce(True,False)
                if ball_speed > 0.001:
                    ball_speed -= 0.008
            elif ball.xcor() > 401:
                ball_speed = ball_st_speed
                score_bored.add_score(True,False,ball)

        if ball.xcor() <= -380 and l_pad_min <= ball.ycor() <= l_pad_max:
            # This is for the left side checks. # This is for the right side checks.
            if ball.xcor() > -400:
                ball.bounce(True,False)
                if ball_speed > 0.001:
                    ball_speed -= 0.008
            elif ball.xcor() < -401:
                ball_speed = ball_st_speed
                score_bored.add_score(False,True, ball)

        if game_over:
            break
run()
screen.exitonclick()



