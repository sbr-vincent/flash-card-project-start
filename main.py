from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
language_dict = []
new_word = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
finally:
    language_dict = data.to_dict(orient="records")


def next_word():
    global new_word, flip_timer
    window.after_cancel(flip_timer)
    new_word = random.choice(language_dict)
    canvas.itemconfig(canvas_image, image=flashcard_image_front)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=new_word["French"], fill="black")
    flip_timer = window.after(3000, translate)


def translate():
    canvas.itemconfig(canvas_image, image=flashcard_image_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=new_word["English"], fill="white")


def known_word():
    global language_dict
    updated_list = [dict_word for dict_word in language_dict if not(dict_word["French"] == new_word["French"])]
    df = pandas.DataFrame(updated_list)
    df.to_csv("data/words_to_learn.csv", index=False)
    data = pandas.read_csv("data/words_to_learn.csv")
    language_dict = data.to_dict(orient="records")
    next_word()
# res = key, val = random.choice(language_dict.items())
# print(str(res))


flashcard_image_front = PhotoImage(file="./images/card_front.png")
flashcard_image_back = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 263, image=flashcard_image_front)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 300, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

flip_timer = window.after(3000, translate)

incorrect_image = PhotoImage(file="./images/wrong.png")
incorrect_button = Button(image=incorrect_image, highlightthickness=0, command=next_word)
incorrect_button.grid(column=0, row=1)

correct_image = PhotoImage(file="./images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=known_word)
correct_button.grid(column=1, row=1)

next_word()

window.mainloop()

