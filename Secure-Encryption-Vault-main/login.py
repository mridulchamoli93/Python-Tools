import pandora_gui
from tkinter import *
from tkinter import messagebox
import mysql.connector
background='#06283D'
framebg='#EDEDED'
framefg='#06283D'


def login():
    USername=user.get()
    password=code.get()
    
    if (USername=="" or USername=="UserId")or (password=="" or password=="Password"):
        messagebox.showerror("wrong entery","Type username or password!!!")
    else:
        try:
            mydb=mysql.connector.connect(host='localhost',port='3306',user='root',password='mridul',database='registration')
            mycursor=mydb.cursor()
            print("connected to database !!!")

        except:
            messagebox.showerror("connection","database connection not stablished")


        command="use registration"
        mycursor.execute(command)


        command="select * from login where Username=%s and Password=%s"
        mycursor.execute(command,(USername,password))
        myresult=mycursor.fetchone()
        print(myresult)

        if myresult==None:
            messagebox.showerror("invalid","please check username/password!!")
        
            trial()
            
        
        else:
            messagebox.showinfo("login","login sucessful !!!")
            root.destroy()
            import main

def register():
    while True:
         root.destroy()
         import registration

   



global trial_num
trial_num=0
def trial():
    global trial_num
    trial_num +=1
    if trial_num==4:
        messagebox.showwarning("Limit warning","you have tried more then limit !!!")
        root.destroy()
        


root = Tk()
root.title("Login System")
root.geometry("600x500")
root.config(bg=background)
root.resizable(False,False)

#for icon image
image_icon=PhotoImage(file='images/icon.png')
root.iconphoto(False,image_icon)

#for background image
frame=Frame(root,bg="red")
frame.pack()

backgroundimage=PhotoImage(file='images/LOGIN.png')
background_label = Label(frame, image=backgroundimage)
background_label.pack()

#for user entry
def user_enter(e):
    user.delete(0,'end')

def user_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'UserID')
user=Entry(frame,width=18,fg="#fff",border=0,bg='#0d151f',font=('Arial Bold',15))
user.insert(0,'UserID')
user.bind("<FocusIn>",user_enter)
user.bind("<FocusOut>",user_leave)
user.place(x=155,y=188)


#for password  entry
def password_enter(e):
    code.delete(0,'end')

def password_leave(e):
    if code.get()=='':
        code.insert(0,'Password')   
code=Entry(frame,width=18,fg="#fff",border=0,bg='#0e1622',font=('Arial Bold',15))
code.insert(0,'Password')
code.bind("<FocusIn>",password_enter)
code.bind("<FocusOut>",password_leave)
code.place(x=155,y=250)

#hide and show button
button_1=True

def hide():
    global button_1
    if button_1:
        eye_button.config(image=close_eye,activebackground="white")
        code.config(show="*")
        button_1=False
    else:
        eye_button.config(image=openeye,activebackground="white")
        code.config(show="")
        button_1=True
openeye=PhotoImage(file="images/openeye.png")
close_eye=PhotoImage(file="images/closeeye.png")
eye_button=Button(frame,image=openeye,bg="#21354e",command=hide)
eye_button.place(x=435,y=245)

#login butoon



login_button=Button(root,text="S U B M I T",fg="#2ae5e5",bg="#0f1823",bd=0,font=(30),command=login)
login_button.place(x=167,y=362)

Label_2=Label(root,text="dont have a account ?",fg="#fff",bg="#0f1823",font=("microsoft yahei ui light",9))
Label_2.place(x=150,y=295)

register_button=Button(text="add new user",bd=0,bg='#0e1622',cursor='hand2',fg="#2ae5e5",command=register)
register_button.place(x=290,y=296)

root.mainloop()











