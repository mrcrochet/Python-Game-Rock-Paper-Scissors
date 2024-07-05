from tkinter import *
from PIL import Image, ImageTk
from random import choice
import time
import tkinter.messagebox as messagebox


root = Tk()
root.title("Rock Scissor Paper")
root.configure(background="#7c92c6")


# Function to resize images
def resize_image(image, max_size):
   ratio = min(max_size[0] / image.size[0], max_size[1] / image.size[1])
   new_size = int(image.size[0] * ratio), int(image.size[1] * ratio)
   return image.resize(new_size, Image.Resampling.LANCZOS)


# Modified load_image function with resizing
def load_image(image_path, max_size=(100, 100)):
   try:
       img = Image.open(image_path)
       img_resized = resize_image(img, max_size)
       return ImageTk.PhotoImage(img_resized)
   except IOError:
       print(f"Impossible D'Afficher l'image: {image_path}")
       return None


# Loading and resizing images
rock_img = load_image("image/Rock-user.png", (100, 100))
paper_img = load_image("image/Paper-user.png", (100, 100))
scissor_img = load_image("image/Scissor-user.png", (100, 100))
rock_img_comp = load_image("image/Rock-user.png", (100, 100))
paper_img_comp = load_image("image/Paper-user.png", (100, 100))
scissor_img_comp = load_image("image/Scissor-user.png", (100, 100))


# Initialisation des variables
start_time = None
player_points = 0
computer_points = 0


def start_timer():
   """Start the timer if it's not already running."""
   global start_time
   if not start_time:
       start_time = time.time()
       update_time()


def reset_game():
   #nouveau match
   global player_points, computer_points, start_time
   player_points = 0
   computer_points = 0
   start_time = None
   playerScore["text"] = "0"
   computerScore["text"] = "0"
   msg["text"] = ""
   time_label.config(text="DEPECHE TOI ! PLUS QUE : 60 "+"secondes")


# function pour le temps 
def update_time():
   global start_time
   if start_time:
       elapsed_time = int(time.time() - start_time)
       time_left = 60 - elapsed_time


       if time_left >= 0:
           time_label.config(text=f"DEPECHE TOI ! PLUS QUE : {time_left}")
           root.after(1000, update_time)
       else:
           determine_winner()


# Fonction pour definir le gagnant apres 60 secs
def determine_winner():
   global player_points, computer_points
   result_text = ""
   if player_points > computer_points:
       result_text = "You win! Game over W in the chat "
   elif computer_points > player_points:
       result_text = "Tu as perdu ! Game over, Bonne chance la prochaine fois "
   else:
       result_text = "Match nulle ! Game over (Tu devrais re-jouer)"


   update_message(result_text)
   if messagebox.askyesno("Game Over", f"{result_text}\n Votre score : {player_points}\n IA score : {computer_points}\n Tu veux perdre encore?"):
       reset_game()
   else:
       root.quit()


# Update functions
def update_message(x):
   msg["text"] = x


def update_user_score():
   global player_points
   player_points += 1
   playerScore["text"] = str(player_points)


def update_comp_score():
   global computer_points
   computer_points += 1
   computerScore["text"] = str(computer_points)


# Check Notre winner
def check_win(player, computer):
   if player == computer:
       update_message("It's a tie!")
   elif (player == "rock" and computer == "scissor") or (player == "paper" and computer == "rock") or (player == "scissor" and computer == "paper"):
       update_message("You win")
       update_user_score()
   else:
       update_message("You lose")
       update_comp_score()


# Update le choix faites par les jouer
choices = ["rock", "paper", "scissor"]
images = {
   "rock": rock_img,
   "paper": paper_img,
   "scissor": scissor_img,
   "rock_comp": rock_img_comp,
   "paper_comp": paper_img_comp,
   "scissor_comp": scissor_img_comp,
}


def update_choice(x):
   global start_time
   start_timer()  # Start the timer au premier choix faites par le joueur
   comp_choice = choice(choices)


   user_label.configure(image=images[x])
   comp_label.configure(image=images[f"{comp_choice}_comp"])


   check_win(x, comp_choice)


# Inserting images
user_label = Label(root, image=scissor_img, bg="#7c92c6")
comp_label = Label(root, image=scissor_img_comp, bg="#7c92c6")
comp_label.grid(row=1, column=0)
user_label.grid(row=1, column=4)


# Score
playerScore = Label(root, text="0", font=("Helvetica", 16), bg="#7c92c6", fg="white")
computerScore = Label(root, text="0", font=("Helvetica", 16), bg="#7c92c6", fg="white")
computerScore.grid(row=1, column=1)
playerScore.grid(row=1, column=3)


# Indicateur
user_indicator = Label(root, font=("Helvetica", 16), text=" JOUEUR ", bg="#7c92c6", fg="white")
comp_indicator = Label(root, font=("Helvetica", 16), text=" IA ", bg="#7c92c6", fg="white")
user_indicator.grid(row=0, column=3)
comp_indicator.grid(row=0, column=1)


# Messages
msg = Label(root, font=("Helvetica", 16), bg="#7c92c6", fg="Black")
msg.grid(row=3, column=2)


# Chrono
time_label = Label(root, text="DEPECHEZ VOUS ! PLUS QUE: 60", font=("Helvetica", 16), bg="#7c92c6", fg="Red")
time_label.grid(row=0, column=2)


# Buttons
rock = Button(root, width=25, height=3, text="ROCK", bg="#ff8000", fg="Orange", command=lambda: update_choice("rock"))
rock.grid(row=2, column=1)

paper = Button(root, width=25, height=3, text="PAPER", bg="#FF3E4D", fg="Black", command=lambda: update_choice("paper"))
paper.grid(row=2, column=2)

scissor = Button(root, width=25, height=3, text="SCISSOR", bg="#ffffff", fg="Green", command=lambda: update_choice("scissor"))
scissor.grid(row=2, column=3)


root.mainloop()
