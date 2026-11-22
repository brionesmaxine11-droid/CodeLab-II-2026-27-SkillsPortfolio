#Exercise 2 - Alexa tell me a Joke

#Importing the modules Tkinter, and random
from tkinter import *
from PIL import ImageTk, Image
import random

root = Tk()
root.geometry('500x500')
root.title('Alexa Joke Assisstant')
root.resizable(0,0)
root.iconbitmap('joke.ico')

#Setting an image as the background
Bg_Original = Image.open('bg2.jpg')
Bg_Resized = Bg_Original.resize((500, 500))
Bg_Image = ImageTk.PhotoImage(Bg_Resized)
Bg_Label = Label(root, image=Bg_Image)
Bg_Label.place(x=0, y=0)

#Getting jokes from the given file
with open('randomJokes.txt', encoding='utf-8') as file_handler: Joke_List = file_handler.readlines()

#Dictionary that remembers the punchline of the current joke
Joke_State = {'punchline': ''}

Hidden_X = 800



#Tells the joke
def Tell_Joke():
    number = random.randint(0, len(Joke_List) - 1)
    joke = Joke_List[number].strip()

    #The text and punchline are separated by a question mark
    parts = joke.split('?')

    Joke_Text.config(text=parts[0] + '?')     #puts back question mark
    Joke_State['punchline'] = parts[1]        #stores punchline for later button

    Joke_Button.place(x=Hidden_X, y=165, anchor=CENTER)                         #hides Alexa button
    Joke_Text.place(x=250, y=165, width=320, height=96, anchor=CENTER)          #shows the joke
    Punchline_Button.place(x=250, y=265, anchor=CENTER)                         #reveals Punchline button


#Tells the Punchline
def Tell_Punchline():
    Punchline_Text.config(text=Joke_State['punchline'])

    Punchline_Button.place(x=Hidden_X, y=265, anchor=CENTER)                    #hides Punchline button
    Punchline_Text.place(x=250, y=265, width=320, height=96, anchor=CENTER)     #shows the punchline
    Next_Button.place(x=135, y=350, anchor=CENTER)                              #shows Next Joke Button
    Quit_Button.place(x=365, y=350, anchor=CENTER)                              #shows Quit Button


#Repeats Process
def Next_Joke():
    Joke_Text.place(x=Hidden_X, y=165, width=320, height=96, anchor=CENTER)          #hides the joke
    Punchline_Text.place(x=Hidden_X, y=265, width=320, height=96, anchor=CENTER)     #hides the punchline
    Next_Button.place(x=Hidden_X, y=350, anchor=CENTER)                              #hides Next Joke
    Quit_Button.place(x=Hidden_X, y=350, anchor=CENTER)                              #hides Quit Button
    Joke_Button.place(x=250, y=165, anchor=CENTER)                                   #shows Alexa button



#Tell me a Joke Button
Joke_Button = Button(root, text='Alexa, tell me a joke', fg="#CEA0A2", bg="#F6F3DF", font=('Arial', 20), command=Tell_Joke)
Joke_Button.place(x=250, y=165, anchor=CENTER)

#Joke Text
Joke_Text = Label(root, text='', fg="#CEA0A2", bg="#F6F3DF", font=('Arial', 20), wraplength=300)
Joke_Text.place(x=Hidden_X, y=165, width=320, height=96, anchor=CENTER)

#Punchline Button
Punchline_Button = Button(root, text='Show Punchline', fg="#F6F3DF", bg="#CEA0A2", font=('Arial', 17), command=Tell_Punchline)
Punchline_Button.place(x=Hidden_X, y=265, anchor=CENTER)

#Punchline Text
Punchline_Text = Label(root, text='', fg="#F6F3DF", bg="#CEA0A2", font=('Arial', 20), wraplength=300)
Punchline_Text.place(x=Hidden_X, y=265, width=320, height=96, anchor=CENTER)

#Next Button + Quit Button
Next_Button = Button(root, text='Next Joke', fg="#CEA0A2", bg="#F6F3DF", font=('Arial', 18), width=10, command=Next_Joke)
Next_Button.place(x=Hidden_X, y=350, anchor=CENTER)
Quit_Button = Button(root, text='Quit', fg="#F6F3DF", bg="#CEA0A2", font=('Arial', 18), width=10, command=root.destroy)
Quit_Button.place(x=Hidden_X, y=350, anchor=CENTER)

root.mainloop()