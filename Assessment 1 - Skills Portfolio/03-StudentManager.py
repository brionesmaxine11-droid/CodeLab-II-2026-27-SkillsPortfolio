#Exercise 3 - Student Manager

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

#Creation of the root window, size and title
root = Tk()
root.geometry('900x600')
root.title('Student Manager')
root.resizable(0,0)
root.iconbitmap('student.ico')

#List that has all students, each student is a dictionary
Students = []

#Dictionary for remembering which student is being updated
Update_State = {'student': None}

#Record boxes size
Record_Width = 66
Record_Height = 16
Record_Tabs = ('124p', '188p', '274p', '337p', '399p')


#Reads studentMarks.txt into the Students list
def Load_Students():
    with open('studentMarks.txt') as file_handler:
        lines = file_handler.readlines()

    #The first line is the student count, so start from the second line
    for line in lines[1:]:
        line = line.strip()
        if line != '':
            parts = line.split(',')
            student = {
                'code': int(parts[0]),
                'name': parts[1],
                'c1': int(parts[2]),
                'c2': int(parts[3]),
                'c3': int(parts[4]),
                'exam': int(parts[5])
            }
            Students.append(student)


#Writes the Students list back to studentMarks.txt
def Save_Students():
    with open('studentMarks.txt', 'w') as file_handler:
        file_handler.write(str(len(Students)) + '\n')
        for student in Students:
            file_handler.write(f"{student['code']},{student['name']},{student['c1']},{student['c2']},{student['c3']},{student['exam']}\n")


#Total of the 3 coursework marks, out of 60
def Coursework_Total(student):
    return student['c1'] + student['c2'] + student['c3']


#Overall percentage, coursework + exam out of 160 marks
def Give_Percentage(student):
    return (Coursework_Total(student) + student['exam']) / 160 * 100


#Grade based on percentage
def Give_Grades(percent):
    if percent >= 70:
        return 'A'
    elif percent >= 60:
        return 'B'
    elif percent >= 50:
        return 'C'
    elif percent >= 40:
        return 'D'
    else:
        return 'F'


#Heading line of the table
def Record_Header():
    return 'Name\tNumber\tCoursework\tExam\tPercent\tGrade'


#One line of the table for one student
def Student_Record(student):
    percent = Give_Percentage(student)
    coursework = f"{Coursework_Total(student)}/60"
    exam = f"{student['exam']}/100"
    percentText = f"{percent:.1f}%"
    return f"{student['name']}\t{student['code']}\t{coursework}\t{exam}\t{percentText}\t{Give_Grades(percent)}"


#Puts text into a read-only box: unlock it, change the text, lock it again
def Record_Box(textBox, text):
    textBox.config(state=NORMAL)
    textBox.delete('1.0', END)
    textBox.insert(END, text)
    textBox.config(state=DISABLED)


#Shows a list of students in a record box, with a summary if asked
def Show_Student_Records(textBox, studentList, showSummary):
    if len(studentList) == 0:
        output = 'No student records can be seen.'
    else:
        output = Record_Header() + '\n' + '_' * (Record_Width - 1) + '\n'
        for student in studentList:
            output += Student_Record(student) + '\n'

        if showSummary:
            total = 0
            for student in studentList:
                total += Give_Percentage(student)
            average = total / len(studentList)
            output += '\n'
            output += f'Number of students: {len(studentList)}\n'
            output += f'Average: {average:.1f}%'
        else:
            output = output.strip()
    Record_Box(textBox, output)


#Finds a student by number or name
def Find_Student(text):
    text = text.strip().lower()
    if text == '':
        return None

    for student in Students:
        if text == str(student['code']) or text == student['name'].lower():
            return student

    for student in Students:
        if text in student['name'].lower():
            return student

    return None


#Checks details of a student, returns an error message ('' means OK)
def Check_Input(name, codeText, c1, c2, c3, exam, oldCode):
    if name == '':
        return 'Please enter a name.'

    #A comma would break the file, because the file is split on commas
    if ',' in name:
        return 'The name cannot contain a comma.'

    if not codeText.isdigit():
        return 'The student number must be a whole number.'

    code = int(codeText)
    if code < 1000 or code > 9999:
        return 'The student number must be between 1000 and 9999.'

    for student in Students:
        if student['code'] == code and code != oldCode:
            return 'That student number is already used.'

    for mark in [c1, c2, c3]:
        if not mark.isdigit() or int(mark) > 20:
            return 'Each coursework score must be a whole number from 0 to 20.'

    if not exam.isdigit() or int(exam) > 100:
        return 'The exam score must be a whole number from 0 to 100.'

    return ''



#1. View all student records
def All_Student_Records():
    All_Frame.tkraise()
    Show_Student_Records(All_Text, Students, True)


#2. View individual student record
def One_Student_Record():
    Single_Frame.tkraise()
    Single_Entry.delete(0, END)
    Record_Box(Single_Text, '')


#Search button: shows the student that has the same name or student number
def Search_Student():
    student = Find_Student(Single_Entry.get())
    if student == None:
        messagebox.showwarning('Not found', 'No student matches that name or number.')
    else:
        Show_Student_Records(Single_Text, [student], False)


#3. Student with the highest total score
def Give_Highest_Score():
    Highest_Frame.tkraise()
    if len(Students) == 0:
        Show_Student_Records(Highest_Text, Students, False)
    else:
        best = max(Students, key=Give_Percentage)
        Show_Student_Records(Highest_Text, [best], False)


#4. Student with the lowest total score
def Give_Lowest_Score():
    Lowest_Frame.tkraise()
    if len(Students) == 0:
        Show_Student_Records(Lowest_Text, Students, False)
    else:
        worst = min(Students, key=Give_Percentage)
        Show_Student_Records(Lowest_Text, [worst], False)


#5. Sort student records by overall percentage
def Show_Sort_Frame():
    Sort_Frame.tkraise()
    Record_Box(Sort_Text, '')


#Ascending or descending button: sorts and shows the records
def Sort_Records(descending):
    sortedList = sorted(Students, key=Give_Percentage, reverse=descending)
    Show_Student_Records(Sort_Text, sortedList, False)


#6. Add a student record
def Add_Student_Record():
    Add_Frame.tkraise()
    Clear_Entry()


def Clear_Entry():
    Add_Name.delete(0, END)
    Add_Code.delete(0, END)
    Add_C1.delete(0, END)
    Add_C2.delete(0, END)
    Add_C3.delete(0, END)
    Add_Exam.delete(0, END)


def Add_Student():
    name = Add_Name.get().strip()
    codeText = Add_Code.get().strip()
    c1 = Add_C1.get().strip()
    c2 = Add_C2.get().strip()
    c3 = Add_C3.get().strip()
    exam = Add_Exam.get().strip()

    error = Check_Input(name, codeText, c1, c2, c3, exam, 0)
    if error != '':
        messagebox.showwarning('Invalid input', error)
        return

    student = {
        'code': int(codeText),
        'name': name,
        'c1': int(c1),
        'c2': int(c2),
        'c3': int(c3),
        'exam': int(exam)
    }
    Students.append(student)
    Save_Students()
    messagebox.showinfo('Added', f'{name} was added and saved to the file.')
    Clear_Entry()


#7. Delete a student record
def Delete_Student_Record():
    Delete_Frame.tkraise()
    Delete_Entry.delete(0, END)


def Delete_Student():
    student = Find_Student(Delete_Entry.get())
    if student == None:
        messagebox.showwarning('Not found', 'No student matches that name or number.')
        return

    name = student['name']
    code = student['code']
    answer = messagebox.askyesno('Delete', f'Delete {name} ({code})?')
    if answer:
        Students.remove(student)
        Save_Students()
        messagebox.showinfo('Deleted', f'{name} was deleted from the file.')
        Delete_Entry.delete(0, END)


#8. Update a student record
def Update_Student_Record():
    Update_Frame.tkraise()
    Update_State['student'] = None
    Update_Search.delete(0, END)
    Clear_Update_Entry()


def Clear_Update_Entry():
    Update_Name.delete(0, END)
    Update_Code.delete(0, END)
    Update_C1.delete(0, END)
    Update_C2.delete(0, END)
    Update_C3.delete(0, END)
    Update_Exam.delete(0, END)


#Finds the student and fills the boxes with their current details
def Update_Student_Details():
    student = Find_Student(Update_Search.get())
    if student == None:
        messagebox.showwarning('Not found', 'No student matches that name or number.')
        return

    Update_State['student'] = student
    Clear_Update_Entry()
    Update_Name.insert(0, student['name'])
    Update_Code.insert(0, student['code'])
    Update_C1.insert(0, student['c1'])
    Update_C2.insert(0, student['c2'])
    Update_C3.insert(0, student['c3'])
    Update_Exam.insert(0, student['exam'])


#Saves the changes made in the boxes
def Save_Update():
    student = Update_State['student']
    if student == None:
        messagebox.showwarning('No student', 'Find a student first.')
        return

    name = Update_Name.get().strip()
    codeText = Update_Code.get().strip()
    c1 = Update_C1.get().strip()
    c2 = Update_C2.get().strip()
    c3 = Update_C3.get().strip()
    exam = Update_Exam.get().strip()

    error = Check_Input(name, codeText, c1, c2, c3, exam, student['code'])
    if error != '':
        messagebox.showwarning('Invalid input', error)
        return

    student['name'] = name
    student['code'] = int(codeText)
    student['c1'] = int(c1)
    student['c2'] = int(c2)
    student['c3'] = int(c3)
    student['exam'] = int(exam)
    Save_Students()
    messagebox.showinfo('Updated', f'{name} was updated and saved to the file.')
    Update_State['student'] = None
    Update_Search.delete(0, END)
    Clear_Update_Entry()


#Welcome Frame
Welcome_Frame = Frame(root, bg="#BCCAA8")
Welcome_Frame.place(x=230, y=0, width=670, height=600)
Welcome_Title = Label(Welcome_Frame, text='Student Manager', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Welcome_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Welcome_Text = Label(Welcome_Frame, text='Choose an option from \n the left to get started.', fg="#1E2427", bg="#BCCAA8", font=('Arial', 20))
Welcome_Text.place(x=335, y=250, anchor=CENTER)

#View All Records Frame
All_Frame = Frame(root, bg="#BCCAA8")
All_Frame.place(x=230, y=0, width=670, height=600)
All_Title = Label(All_Frame, text='All Student Records', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
All_Title.place(x=0, y=68, width=670, height=46, anchor=W)
All_Text = Text(All_Frame, width=Record_Width, height=Record_Height, fg="#273338", bg="#DDE4D4", font=('Arial', 13), padx=10, pady=6, tabs=Record_Tabs, state=DISABLED)
All_Text.place(x=25, y=350, anchor=W)

#View Individual Frame
Single_Frame = Frame(root, bg="#BCCAA8")
Single_Frame.place(x=230, y=0, width=670, height=600)
Single_Title = Label(Single_Frame, text='Individual Student Record', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Single_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Single_Label = Label(Single_Frame, text='Enter the student name or number:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Single_Label.place(x=25, y=100)
Single_Entry = Entry(Single_Frame, font=('Arial', 14))
Single_Entry.place(x=25, y=130, width=300, height=35)
Single_Button = Button(Single_Frame, text='Search', fg="#BCCAA8", bg="#273338", font=('Arial', 14, 'bold'), command=Search_Student)
Single_Button.place(x=340, y=130, width=130, height=35)
Single_Text = Text(Single_Frame, width=Record_Width, height=Record_Height, fg="#273338", bg="#DDE4D4", font=('Arial', 13), padx=10, pady=6, tabs=Record_Tabs, state=DISABLED)
Single_Text.place(x=25, y=350, anchor=W)

#Highest Score Frame
Highest_Frame = Frame(root, bg="#BCCAA8")
Highest_Frame.place(x=230, y=0, width=670, height=600)
Highest_Title = Label(Highest_Frame, text='Highest Total Score', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Highest_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Highest_Text = Text(Highest_Frame, width=Record_Width, height=Record_Height, fg="#273338", bg="#DDE4D4", font=('Arial', 13), padx=10, pady=6, tabs=Record_Tabs, state=DISABLED)
Highest_Text.place(x=25, y=350, anchor=W)

#Lowest Score Frame
Lowest_Frame = Frame(root, bg="#BCCAA8")
Lowest_Frame.place(x=230, y=0, width=670, height=600)
Lowest_Title = Label(Lowest_Frame, text='Lowest Total Score', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Lowest_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Lowest_Text = Text(Lowest_Frame, width=Record_Width, height=Record_Height, fg="#273338", bg="#DDE4D4", font=('Arial', 13), padx=10, pady=6, tabs=Record_Tabs, state=DISABLED)
Lowest_Text.place(x=25, y=350, anchor=W)

#Sort Frame
Sort_Frame = Frame(root, bg="#BCCAA8")
Sort_Frame.place(x=230, y=0, width=670, height=600)
Sort_Title = Label(Sort_Frame, text='Sort Student Records', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Sort_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Sort_Ascending = Button(Sort_Frame, text='Ascending (low to high)', fg="#BCCAA8", bg="#273338", font=('Arial', 12, 'bold'), command=lambda: Sort_Records(False))
Sort_Ascending.place(x=25, y=110, width=230, height=40)
Sort_Descending = Button(Sort_Frame, text='Descending (high to low)', fg="#BCCAA8", bg="#273338", font=('Arial', 12, 'bold'), command=lambda: Sort_Records(True))
Sort_Descending.place(x=270, y=110, width=230, height=40)
Sort_Text = Text(Sort_Frame, width=Record_Width, height=Record_Height, fg="#273338", bg="#DDE4D4", font=('Arial', 13), padx=10, pady=6, tabs=Record_Tabs, state=DISABLED)
Sort_Text.place(x=25, y=350, anchor=W)

#Add Frame
Add_Frame = Frame(root, bg="#BCCAA8")
Add_Frame.place(x=230, y=0, width=670, height=600)
Add_Title = Label(Add_Frame, text='Add a Student', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Add_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Add_Label1 = Label(Add_Frame, text='Student name:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Add_Label1.place(x=25, y=115)
Add_Name = Entry(Add_Frame, font=('Arial', 14))
Add_Name.place(x=230, y=110, width=250, height=34)
Add_Label2 = Label(Add_Frame, text='Student number:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Add_Label2.place(x=25, y=165)
Add_Code = Entry(Add_Frame, font=('Arial', 14))
Add_Code.place(x=230, y=160, width=250, height=34)
Add_Label3 = Label(Add_Frame, text='Coursework mark 1:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Add_Label3.place(x=25, y=215)
Add_C1 = Entry(Add_Frame, font=('Arial', 14))
Add_C1.place(x=230, y=210, width=250, height=34)
Add_Label4 = Label(Add_Frame, text='Coursework mark 2:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Add_Label4.place(x=25, y=265)
Add_C2 = Entry(Add_Frame, font=('Arial', 14))
Add_C2.place(x=230, y=260, width=250, height=34)
Add_Label5 = Label(Add_Frame, text='Coursework mark 3:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Add_Label5.place(x=25, y=315)
Add_C3 = Entry(Add_Frame, font=('Arial', 14))
Add_C3.place(x=230, y=310, width=250, height=34)
Add_Label6 = Label(Add_Frame, text='Exam mark:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Add_Label6.place(x=25, y=365)
Add_Exam = Entry(Add_Frame, font=('Arial', 14))
Add_Exam.place(x=230, y=360, width=250, height=34)
Add_Button = Button(Add_Frame, text='Add Student', fg="#BCCAA8", bg="#273338", font=('Arial', 14, 'bold'), command=Add_Student)
Add_Button.place(x=230, y=425, width=250, height=45)

#Delete Frame
Delete_Frame = Frame(root, bg="#BCCAA8")
Delete_Frame.place(x=230, y=0, width=670, height=600)
Delete_Title = Label(Delete_Frame, text='Delete a Student', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Delete_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Delete_Label = Label(Delete_Frame, text='Enter the student name or number:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Delete_Label.place(x=25, y=100)
Delete_Entry = Entry(Delete_Frame, font=('Arial', 14))
Delete_Entry.place(x=25, y=135, width=300, height=35)
Delete_Button = Button(Delete_Frame, text='Delete Student', fg="#BCCAA8", bg="#273338", font=('Arial', 14, 'bold'), command=Delete_Student)
Delete_Button.place(x=340, y=135, width=170, height=35)

#Update Frame
Update_Frame = Frame(root, bg="#BCCAA8")
Update_Frame.place(x=230, y=0, width=670, height=600)
Update_Title = Label(Update_Frame, text='Update a Student', fg="#BCCAA8", bg="#273338", font=('Arial', 26))
Update_Title.place(x=0, y=68, width=670, height=46, anchor=W)
Update_Label = Label(Update_Frame, text='Enter the student name or number:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Update_Label.place(x=25, y=100)
Update_Search = Entry(Update_Frame, font=('Arial', 14))
Update_Search.place(x=25, y=135, width=300, height=35)
Update_Find = Button(Update_Frame, text='Find Student', fg="#BCCAA8", bg="#273338", font=('Arial', 14, 'bold'), command=Update_Student_Details)
Update_Find.place(x=340, y=135, width=170, height=35)
Update_Label1 = Label(Update_Frame, text='Student name:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Update_Label1.place(x=25, y=195)
Update_Name = Entry(Update_Frame, font=('Arial', 14))
Update_Name.place(x=230, y=190, width=250, height=34)
Update_Label2 = Label(Update_Frame, text='Student number:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Update_Label2.place(x=25, y=240)
Update_Code = Entry(Update_Frame, font=('Arial', 14))
Update_Code.place(x=230, y=235, width=250, height=34)
Update_Label3 = Label(Update_Frame, text='Coursework mark 1:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Update_Label3.place(x=25, y=285)
Update_C1 = Entry(Update_Frame, font=('Arial', 14))
Update_C1.place(x=230, y=280, width=250, height=34)
Update_Label4 = Label(Update_Frame, text='Coursework mark 2:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Update_Label4.place(x=25, y=330)
Update_C2 = Entry(Update_Frame, font=('Arial', 14))
Update_C2.place(x=230, y=325, width=250, height=34)
Update_Label5 = Label(Update_Frame, text='Coursework mark 3:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Update_Label5.place(x=25, y=375)
Update_C3 = Entry(Update_Frame, font=('Arial', 14))
Update_C3.place(x=230, y=370, width=250, height=34)
Update_Label6 = Label(Update_Frame, text='Exam mark:', fg="#273338", bg="#BCCAA8", font=('Arial', 14))
Update_Label6.place(x=25, y=420)
Update_Exam = Entry(Update_Frame, font=('Arial', 14))
Update_Exam.place(x=230, y=415, width=250, height=34)
Update_Save = Button(Update_Frame, text='Save Changes', fg="#BCCAA8", bg="#273338", font=('Arial', 14, 'bold'), command=Save_Update)
Update_Save.place(x=230, y=470, width=250, height=45)

#Sidebar Frame
Sidebar_Frame = Frame(root)
Sidebar_Frame.place(x=0, y=0, width=230, height=600)

#Setting an image as the background of the sidebar
Side_Original = Image.open('bg3.jpg')
Side_Resized = Side_Original.resize((230, 600))
Side_Image = ImageTk.PhotoImage(Side_Resized)
Side_Canvas = Canvas(Sidebar_Frame, width=230, height=600, highlightthickness=0)
Side_Canvas.place(x=0, y=0)
Side_Canvas.create_image(0, 0, anchor="nw", image=Side_Image)
Side_Canvas.create_text(115, 54, text='Student\nManager', font=('Arial', 25, 'bold'), fill="#1C2325", justify=CENTER)

Menu_Button1 = Button(Sidebar_Frame, text='View All Records', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=All_Student_Records)
Menu_Button1.place(x=12, y=154, width=206, height=42)
Menu_Button2 = Button(Sidebar_Frame, text='View Individual Record', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=One_Student_Record)
Menu_Button2.place(x=12, y=204, width=206, height=42)
Menu_Button3 = Button(Sidebar_Frame, text='Highest Total Score', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=Give_Highest_Score)
Menu_Button3.place(x=12, y=254, width=206, height=42)
Menu_Button4 = Button(Sidebar_Frame, text='Lowest Total Score', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=Give_Lowest_Score)
Menu_Button4.place(x=12, y=304, width=206, height=42)
Menu_Button5 = Button(Sidebar_Frame, text='Sort Records', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=Show_Sort_Frame)
Menu_Button5.place(x=12, y=354, width=206, height=42)
Menu_Button6 = Button(Sidebar_Frame, text='Add a Student', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=Add_Student_Record)
Menu_Button6.place(x=12, y=404, width=206, height=42)
Menu_Button7 = Button(Sidebar_Frame, text='Delete a Student', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=Delete_Student_Record)
Menu_Button7.place(x=12, y=454, width=206, height=42)
Menu_Button8 = Button(Sidebar_Frame, text='Update a Student', fg="#BCCAA8", bg="#273338", font=('Arial', 11, 'bold'), anchor=W, padx=12, command=Update_Student_Record)
Menu_Button8.place(x=12, y=504, width=206, height=42)


#Load the file, then show welcome frame
Load_Students()
Welcome_Frame.tkraise()


root.mainloop()