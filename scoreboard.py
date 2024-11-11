from turtle import Screen, Turtle

FONT = ("Courier", 24, "bold")


class Scoreboard:
    def __init__(self):
        self.screen = Screen()
        self.score = 1
        self.draw_score = Turtle()
        self.screen.tracer(0)

    def draw_score_on_screen(self):
        self.draw_score.clear()
        self.draw_score.penup()
        self.draw_score.hideturtle()
        self.draw_score.goto(-200,250)
        self.draw_score.write(arg=f"Level :{self.score}",move=False, align="center",font=FONT)
        self.screen.update()

    pass
