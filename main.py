from tkinter import *
import os
import sys
if getattr(sys, 'frozen', False):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
else:
    base_path = os.path.abspath(".")
game_data_path = os.path.join(base_path, "tomato.png")

# ---------------------------- CONSTANTS ------------------------------- #
class PT:
    PINK = "#e2979c"
    RED = "#e7305b"
    GREEN = "#9bdeac"
    YELLOW = "#f7f5dd"
    FONT_NAME = "Courier"
    WORK_MIN = 25
    SHORT_BREAK_MIN = 5
    LONG_BREAK_MIN = 20
    WORK_TOTAL = 4
    TIMER = None

    total_checks = 0
    green_check = "✅"
    mins = WORK_MIN
    seconds = 0
    already_worked = False
    RUNNING = False
# ---------------------------- TIMER RESET ------------------------------- #
def restart_timer():
    global text_item,label
    window.after_cancel(PT.TIMER)
    PT.RUNNING = False
    canvas.itemconfig(text_item,text=f"0:00")
    start_button.configure(state=NORMAL)
    PT.WORK_TOTAL = 4
    PT.total_checks = 0
    PT.already_worked = False
    label = Label(text="Timer", font=(PT.FONT_NAME, 46, "bold"), fg=PT.GREEN, bg=PT.YELLOW, pady=10)

# ---------------------------- TIMER MECHANISM ------------------------------- #


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def start_clicked():
    global label
    if not PT.RUNNING:
        if PT.WORK_TOTAL <= 0 and PT.already_worked:
            label.configure(text="Long\n Break!", font=(PT.FONT_NAME,42,"bold"),fg=PT.RED,bg=PT.YELLOW,pady=10)
            PT.mins = PT.LONG_BREAK_MIN
            PT.WORK_TOTAL = 4
            PT.already_worked = False
        elif PT.WORK_TOTAL > 0 and not PT.already_worked:
            label.configure(text="Work!", font=(PT.FONT_NAME, 42, "bold"), fg=PT.GREEN, bg=PT.YELLOW, pady=10)
            PT.mins = PT.WORK_MIN
            PT.already_worked = True
            PT.WORK_TOTAL -= 1
        elif PT.already_worked:
            label.configure(text="Short\n Break!", font=(PT.FONT_NAME, 42, "bold"), fg=PT.PINK, bg=PT.YELLOW, pady=10)
            PT.mins = PT.SHORT_BREAK_MIN
            PT.already_worked = False
        PT.seconds = 0
        PT.RUNNING = True
        count_down()


def count_down():
    if not PT.RUNNING:
        return
    global text_item
    start_button.configure(state=DISABLED)
    if PT.mins > 0 or PT.seconds > 0:
        if PT.RUNNING:
            PT.TIMER = window.after(1000, count_down)
        if PT.seconds == 0:
            PT.mins -= 1
            PT.seconds = 59
        else:
            PT.seconds -= 1
        canvas.itemconfig(text_item, text=f"{PT.mins:2d}:{PT.seconds:02d}")
    elif PT.mins <= 0 and PT.seconds <=0:
        PT.RUNNING = False
        add_green_check(1)
        start_clicked()


def add_green_check(add_check):
    PT.total_checks += add_check
    add_checks = [PT.green_check for _ in range(PT.total_checks)]
    label_checks = Label(text=f"{''.join(add_checks)}", bg=PT.YELLOW, highlightthickness=0, fg=PT.GREEN)
    label_checks.grid(column=1, row=2)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.configure(bg=PT.YELLOW,highlightthickness=0)

# Canvas
canvas = Canvas(window,bg=PT.YELLOW,width=200,height=224,highlightthickness=0)
bg_image = PhotoImage(file=game_data_path)
canvas.create_image(100,112, image=bg_image)
text_item = canvas.create_text(100,140, text=f"00:00", font=(PT.FONT_NAME,24,"bold"), fill="white")
canvas.grid(column=1,row=1)

#Labels
label=Label(text="Timer",font=(PT.FONT_NAME,42,"bold"),fg=PT.GREEN,bg=PT.YELLOW,pady=10,width=8,height=2)
label.grid(column=1,row=0)

# Buttons
start_button = Button(padx=10,text="Start",font=(PT.FONT_NAME,12,"bold"),bg=PT.GREEN,fg=PT.RED,command=start_clicked,highlightthickness=0)
start_button.grid(column=2,row=2,padx=10,pady=50)

reset_button = Button(padx=5,text="Restart",font=(PT.FONT_NAME,12,"bold"),bg=PT.GREEN,fg=PT.RED,command=restart_timer,highlightthickness=0)
reset_button.grid(column=0,row=2,padx=10,pady=50)


window.mainloop()