from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# ------------------- FLASH CARDS SETUP ------------------- #

df = pandas.read_csv("data/1000-esp-en-words.csv")
df = df.to_dict(orient="records")

selected_word = {}
unknown_words_list = {}
known_words_list = []




def random_card():

    global selected_word, flip_timer
    window.after_cancel(flip_timer)

    try:
        unknown_words = pandas.read_csv("unknown_words.csv")
        unknown_words = unknown_words.to_dict(orient="records")
        selected_word = random.choice(unknown_words)
        spanish_word = selected_word["Spanish"]

    except FileNotFoundError:
        selected_word = random.choice(df)
        spanish_word = selected_word["Spanish"]

    canvas.itemconfig(card_lang, fill="black", text="Spanish")
    canvas.itemconfig(card_word, fill="black", text=spanish_word)
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(3000, func=flip_card)


def flip_card():

    global selected_word
    english_word = selected_word["English"]

    canvas.itemconfig(card_lang, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=english_word)
    canvas.itemconfig(card_background, image=card_back_img)


def remove_word():
    global unknown_words_list
    df.remove(selected_word)
    unknown_words_list = df
    unknown_words = pandas.DataFrame(unknown_words_list)
    unknown_words.to_csv("unknown_words.csv", index=False)

    global known_words_list
    known_words_list.append(selected_word)
    known_words = pandas.DataFrame(known_words_list)
    known_words.to_csv("known_words.csv", index=False)

    random_card()



# ------------------- UI SETUP ------------------- #
window = Tk()
window.title("Spanish Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=500, height=350, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="images/card_front.gif")
card_back_img = PhotoImage(file="images/card_back.gif")
card_background = canvas.create_image(250, 175, image=card_front_img)
card_lang = canvas.create_text(250, 100, text="", fill="black", font=("Ariel", 25, "italic"))
card_word = canvas.create_text(250, 200, text="", fill="black", font=("Ariel", 35, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

#Buttons

wrong_img = PhotoImage(file="images/wrong.gif")
wrong_button = Button(image=wrong_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR,
                      highlightcolor=BACKGROUND_COLOR, bd=0, command=random_card)

wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.gif")
right_button = Button(image=right_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, bd=0,
                      command=remove_word)
right_button.grid(column=1, row=1)

random_card()

window.mainloop()