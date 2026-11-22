#Exercise 1 - Maths Quiz


#Importing the modules Tkinter, messagebox, Pillow and random
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random

#Sets the window size, title, and icon
root = Tk()
root.geometry('500x500')
root.title('Maths Quiz')
root.resizable(0,0)
root.iconbitmap('math.ico')

#Sets an image as the background through usage of label
Bg_Original = Image.open('bg1.jpg')
Bg_Resized = Bg_Original.resize((500, 500))
Bg_Image = ImageTk.PhotoImage(Bg_Resized)

#Tracking the quiz by usage of dictionary
Quiz_Tracker = {
    'level': 1,      # 1 = Easy, 2 = Moderate, 3 = Advanced
    'score': 0,      # points earned
    'question': 0,   # question counter
    'attempt': 1,    # 1st / 2nd attempt logger
    'answer': 0      # correct answer given
}


#Shows the main menu
def Main_Menu():
    #Resets the quiz every time the menu is shown
    Quiz_Tracker['score'] = 0
    Quiz_Tracker['question'] = 0
    Quiz_Tracker['attempt'] = 1

    #Main Frame
    Menu_Frame = Frame(root)
    Menu_Frame.place(x=0, y=0, width=500, height=500)
    Menu_Bg = Label(Menu_Frame, image=Bg_Image)
    Menu_Bg.place(x=0, y=0)

    #Main Text
    Menu_Title = Label(Menu_Frame, text='Maths Quiz!', fg="#e63286", bg="#ffd6d6", font=('Arial', 40))
    Menu_Title.pack(fill=BOTH, ipady=10)

    #Sub-Text
    Menu_Subtitle = Label(Menu_Frame, text="Choose your difficulty:", fg="#ffd6d6", bg="#e63286", font=('Arial', 25))
    Menu_Subtitle.pack(fill=BOTH, ipady=10)

    #Buttons for the difficulties
    Easy_Button = Button(Menu_Frame, text='Easy', fg="#d84987", bg="#ffc5e0", font=('Arial', 28), width=10, command=lambda: startQuiz(1))
    Easy_Button.place(x=250, y=220, anchor=CENTER)
    Moderate_Button = Button(Menu_Frame, text='Moderate', fg="#f8e6ef", bg="#e25a99", font=('Arial', 28), width=10, command=lambda: startQuiz(2))
    Moderate_Button.place(x=250, y=320, anchor=CENTER)
    Advanced_Button = Button(Menu_Frame, text='Advanced', fg="#fceef5", bg="#e7388a", font=('Arial', 28), width=10, command=lambda: startQuiz(3))
    Advanced_Button.place(x=250, y=420, anchor=CENTER)


#Starts when a difficulty is chosen
def startQuiz(level):
    Quiz_Tracker['level'] = level
    Quiz_Tracker['score'] = 0
    Quiz_Tracker['question'] = 0

    #Change the title according to the difficulty
    if level == 1:
        Quiz_Title.config(text='Easy Mode:')
    elif level == 2:
        Quiz_Title.config(text='Moderate Mode:')
    else:
        Quiz_Title.config(text='Advanced Mode:')

    Quiz_Frame.tkraise()
    Give_Question()


#Generates random numbers, single digit for easy, double digit for moderate, quadruple digits for advanced
def Randomized_Number(level):
    if level == 1:
        return random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)

#Randomly chooses addition or subtraction
def Randomized_Operation():
    if random.randint(1, 2) == 1:
        return '+'
    else:
        return '-'


#Displays next question and waits for answer
def Give_Question():
    #After doing 10 questions > show results
    if Quiz_Tracker['question'] == 10:
        Show_Results(Quiz_Tracker['score'])
        return
    Quiz_Tracker['question'] += 1
    Quiz_Tracker['attempt'] = 1
    num1 = Randomized_Number(Quiz_Tracker['level'])
    num2 = Randomized_Number(Quiz_Tracker['level'])
    op = Randomized_Operation()

    #Looks for right answer and keeps it stored
    if op == '+':
        Quiz_Tracker['answer'] = num1 + num2
    else:
        Quiz_Tracker['answer'] = num1 - num2

    #Updates label according to score and clears entry box for next question
    qNumber = Quiz_Tracker['question']
    currentScore = Quiz_Tracker['score']
    Quiz_Counter.config(text=f'Question {qNumber}/10')
    Quiz_Score.config(text=f'Score: {currentScore}/100')
    Quiz_Problem.config(text=f'{num1} {op} {num2} =')
    Quiz_Entry.delete(0, END)


#Checks answer, tells if true or false
def Correct_Answer(userAnswer):
    if userAnswer == Quiz_Tracker['answer']:
        if Quiz_Tracker['attempt'] == 1:
            Quiz_Tracker['score'] += 10
            messagebox.showinfo('Correct!', 'Good Job! +10 points')
        else:
            Quiz_Tracker['score'] += 5
            messagebox.showinfo('Correct!', 'Not Bad! +5 points')
        return True
    else:
        if Quiz_Tracker['attempt'] == 1:
            messagebox.showerror('Incorrect', 'Try one more time!')
        else:
            correct = Quiz_Tracker['answer']
            messagebox.showerror('Incorrect', f'The correct answer was {correct} :()')
        return False


#Functions when the submit button is pressed or enter in keyboard
def Answer_Checker():
    text = Quiz_Entry.get().strip()

    #Ensures something is typed in the field
    if text == '':
        messagebox.showwarning('Warning', 'Please type your answer first')
        return

    correct = Correct_Answer(int(text))
    if correct:
        Give_Question()                  # next question
    elif Quiz_Tracker['attempt'] == 1:
        Quiz_Tracker['attempt'] = 2         # one more chance
        Quiz_Entry.delete(0, END)
    else:
        Give_Question()                  # out of chances, next question


#Gives final score of x/100 and the computed rank
def Show_Results(finalScore):
    if finalScore > 90:
        rank = 'A+'
    elif finalScore >= 80:
        rank = 'A'
    elif finalScore >= 70:
        rank = 'B'
    elif finalScore >= 60:
        rank = 'C'
    elif finalScore >= 50:
        rank = 'D'
    else:
        rank = 'F'
    Results_Score.config(text=f'Your score: {finalScore} / 100')
    Results_Rank.config(text=f'Rank: {rank}')
    Results_Frame.tkraise()



#Frame for Quiz
Quiz_Frame = Frame(root)
Quiz_Frame.place(x=0, y=0, width=500, height=500)
Quiz_Bg = Label(Quiz_Frame, image=Bg_Image)
Quiz_Bg.place(x=0, y=0)

#Main Text (changes to Easy / Moderate / Advanced Mode)
Quiz_Title = Label(Quiz_Frame, text='', fg="#e63286", bg="#ffd6d6", font=('Arial', 40))
Quiz_Title.pack(fill=BOTH, ipady=10)

#Sub-Text (score out of 100)
Quiz_Score = Label(Quiz_Frame, text='Score: 0/100', fg="#ffd6d6", bg="#e63286", font=('Arial', 30))
Quiz_Score.pack(fill=BOTH, ipady=10)

#Question box
Quiz_Problem = Label(Quiz_Frame, text='', fg="#e63286", bg="#ffd6d6", font=('Arial', 36))
Quiz_Problem.place(x=60, y=205, width=380, height=130)

#Question counter
Quiz_Counter = Label(Quiz_Frame, text='', fg="#ffd6d6", bg="#e63286", font=('Arial', 10))
Quiz_Counter.place(x=60, y=335, width=380, height=30)

#Entry box for the answer
Quiz_Entry = Entry(Quiz_Frame, font=('Arial', 24), justify=CENTER)
Quiz_Entry.place(x=60, y=380, width=245, height=60)
Quiz_Entry.bind('<Return>', lambda event: Answer_Checker())   # Enter = Submit

#Submit button
Quiz_Submit = Button(Quiz_Frame, text='Submit', fg="#ffd6d6", bg="#e63286", font=('Arial', 18, 'bold'), command=Answer_Checker)
Quiz_Submit.place(x=320, y=380, width=120, height=60)


#Results Frame
Results_Frame = Frame(root)
Results_Frame.place(x=0, y=0, width=500, height=500)
Results_Bg = Label(Results_Frame, image=Bg_Image)
Results_Bg.place(x=0, y=0)

#Main Text
Results_Title = Label(Results_Frame, text='Quiz Over!', fg="#e63286", bg="#ffd6d6", font=('Arial', 40))
Results_Title.pack(fill=BOTH, ipady=10)

#Sub-Text (final score out of 100)
Results_Score = Label(Results_Frame, text='', fg="#ffd6d6", bg="#e63286", font=('Arial', 25))
Results_Score.pack(fill=BOTH, ipady=10)

#Rank
Results_Rank = Label(Results_Frame, text='', fg="#e63286", bg="#ffd6d6", font=('Arial', 40))
Results_Rank.place(x=250, y=230, anchor=CENTER)

#Play again prompt and buttons
Results_Prompt = Label(Results_Frame, text='Do you want to play again?', fg="#e63286", bg="#ffd6d6", font=('Arial', 22))
Results_Prompt.place(x=250, y=330, anchor=CENTER)

Play_Button = Button(Results_Frame, text='Play Again', fg="#d84987", bg="#ffc5e0", font=('Arial', 18), width=10, command=Main_Menu)
Play_Button.place(x=135, y=410, anchor=CENTER)
Quit_Button = Button(Results_Frame, text='Quit', fg="#fceef5", bg="#e7388a", font=('Arial', 18), width=10, command=root.destroy)
Quit_Button.place(x=365, y=410, anchor=CENTER)


#Show the menu at the start of the quiz
Main_Menu()

#Allows the application to continously run
root.mainloop()