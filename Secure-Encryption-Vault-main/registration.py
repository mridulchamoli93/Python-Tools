from tkinter import *
from tkinter import messagebox
import mysql.connector
background='#06283D'
framebg='#EDEDED'
framefg='#06283D'



root = Tk()
root.title("Login System")
root.geometry("1250x700+210+100")
root.config(bg=background)
root.resizable(False,False)


def login():
    root.destroy()
    import login
    



def register():
    Username = user_1.get()
    password = passcode_1.get()
    passcode = adminascess.get()

    
    if (Username == "" or Username == "UserId") or (password == "" or password == "Password"):
            messagebox.showerror("Wrong Entry", "Type username or password!!!")
    else:
            try:
                mydb = mysql.connector.connect(
                    host='localhost',
                    port='3306',
                    user='root',
                    password='mridul',
                    database='registration'
                )
                mycursor = mydb.cursor()
                print("Connected to the database!")

            except mysql.connector.Error as err:
                if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                    # Create the database if it doesn't exist
                    mydb = mysql.connector.connect(
                        host='localhost',
                        port='3306',
                        user='root',
                        password='mridul'
                    )
                    mycursor = mydb.cursor()
                    mycursor.execute("CREATE DATABASE registration")
                    mycursor.execute("USE registration")

                    # Create the 'login' table
                    mycursor.execute("CREATE TABLE login (user INT AUTO_INCREMENT PRIMARY KEY, Username VARCHAR(100), Password VARCHAR(100),passcode varchar(100))")
                else:
                    messagebox.showerror("Connection", "Database connection not established")
                    return

            try:
                command = "INSERT INTO login (Username, Password, key_column) VALUES (%s, %s, %s)"
                values = (Username, password, passcode)
                mycursor.execute(command, values)

                mydb.commit()
                mydb.close()
                messagebox.showinfo("Register", "Successfully created account")


            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to insert data: {err}")

        
               


#for icon image
image_icon=PhotoImage(file='image/icon.png')
root.iconphoto(False,image_icon)

#for background image
frame=Frame(root,bg="red")
frame.pack()

backgroundimage=PhotoImage(file='image/register.png')
background_label = Label(frame, image=backgroundimage)
background_label.pack()

adminascess=Entry(frame,width=15,fg="#000",border=0,bg='#e8ecf7',font=("Arial Bold",20),show="*")
adminascess.focus()
adminascess.place(x=550,y=280)

Label(root,text="enter your secret key",bg="#e8ecf7").place(x=550,y=260)

#user entry
def user_enter(e):
    user_1.delete(0,"end")
def user_out(e):
    name=user_1.get()
    if name=='':
        user_1.insert('UserID')
user_1=Entry(frame,width=15,fg="#fff",border=0,bg='#375174',font=("Arial Bold",20))
user_1.insert(0,"UserID")
user_1.bind("<FocusIn>",user_enter)
user_1.bind("<FocusOut>",user_out)
user_1.place(x=500,y=380)

#password entry

def passcode_enter(e):
    passcode_1.delete(0,"end")
def passcode_out(e):
    name=passcode_1.get()
    if name=="":
        passcode_1.insert('Password')
passcode_1=Entry(frame,width=15,fg="#fff",border=0,bg='#375174',font=("Arial Bold",20),)
passcode_1.insert(0,'Password')
passcode_1.bind("<FocusIn>",passcode_enter)
passcode_1.bind("<FocusOut>",passcode_out)
passcode_1.place(x=500,y=470)

button_1=True

def hide():
    global button_1
    if button_1:
        eye_button.config(image=close_eye,activebackground="white")
        passcode_1.config(show="*")
        button_1=False
    else:
        eye_button.config(image=openeye,activebackground="white")
        passcode_1.config(show="")
        button_1=True
openeye=PhotoImage(file="images/openeye.png")
close_eye=PhotoImage(file="images/closeeye.png")
eye_button=Button(root,image=openeye,bg="#375174",command=hide)
eye_button.place(x=780,y=470)

register_button=Button(root,text="Add New User",bg='#486387',cursor='hand2',fg="white",width=13,height=1,font=("Arial",16,"bold"),bd=0,command=register)
register_button.place(x=530,y=600)

back_buttonimg=PhotoImage(fil="image/backbutton.png")
back_button=Button(root,imag=back_buttonimg,fg='#deeefb',command=login)
back_button.place(x=20,y=15)


root.mainloop()