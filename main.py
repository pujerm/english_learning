import random
from tkinter import *
import pandas

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/eng_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}
learned_words = []


def saving_learned_words():
    global current_card

    learned_words.append(current_card)
    data_learned_words = pandas.DataFrame(learned_words)
    data_learned_words.columns = "English", "Polish"
    data_learned_words.to_csv("data/know_words.csv", index=False)
    to_learn.remove(current_card)
    data_to_learn = pandas.DataFrame(to_learn)
    data_to_learn.columns = "English", "Polish"
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)


def next_card_ok():
    global current_card, time_sleep
    saving_learned_words()
    windows.after_cancel(time_sleep)

    current_card = random.choice(to_learn)
    canvas.itemconfig(card_photo, image=card_front)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")

    time_sleep = windows.after(3000, func=flip_card)


def next_card_nok():
    global current_card, time_sleep

    windows.after_cancel(time_sleep)

    current_card = random.choice(to_learn)
    canvas.itemconfig(card_photo, image=card_front)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")

    time_sleep = windows.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_photo, image=card_back)
    canvas.itemconfig(card_title, text="Polish", fill="white")
    canvas.itemconfig(card_word, text=current_card["Polish"], fill="white")


# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"

windows = Tk()
windows.title("Flashy")
windows.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

time_sleep = windows.after(3000, func=flip_card)

canvas_width = 800
canvas_height = 526
canvas = Canvas(width=canvas_width, height=canvas_height, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_photo = canvas.create_image(400, 263, image=card_front)

card_title = canvas.create_text(canvas_width / 2, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(canvas_width / 2, 263, text="", font=("Ariel", 60, "bold"))
next_card_nok()
canvas.grid(row=0, column=0, columnspan=2)
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

right_button = Button(image=right_image, highlightthickness=0, command=next_card_ok)
right_button.grid(row=1, column=1)
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card_nok)
wrong_button.grid(row=1, column=0)

windows.mainloop()
