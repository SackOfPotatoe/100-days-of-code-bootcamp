from turtle import Turtle,Screen
class ScoreBored:


    def __init__(self):
        self.game_started = True
        self.screen = Screen()
        self.score_left = Turtle()
        self.score_left.hideturtle()
        self.score_left.penup()
        self.score_right = Turtle()
        self.score_right.hideturtle()
        self.score_right.penup()
        self.left_score_count = 0
        self.right_score_count = 0

    def draw_score(self):
        self.screen.tracer(False)
        self.score_right.color("white")
        self.score_left.color("white")
        self.score_right.shape("square")
        self.score_left.goto(-100,220)
        self.score_right.goto(100,220)
        self.score_right.write(arg=self.right_score_count,move=False,align="center",font=("Courier",45,"bold"))
        self.score_left.write(arg=self.left_score_count,move=False,align="center",font=("Courier",45,"bold"))
        self.screen.update()
    def refresh_score(self):
        self.score_right.clear()
        self.score_left.clear()
        self.draw_score()
    def add_score(self, right_true, left_true,ball):
        if right_true:
            self.left_score_count += 1
            ball.ball_reset()
        elif left_true:
            self.right_score_count += 1
            ball.ball_reset()
        self.refresh_score()






