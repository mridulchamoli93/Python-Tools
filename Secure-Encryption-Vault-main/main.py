from tkinter import *
from tkinter import messagebox
import mysql.connector
import os
import base64 

def reset():   
        code.set("")
        entry1.delete(1.0,END)

def encrypt_text():
        password=code.get()
        if password=="mridul":
               screen2=Toplevel(screen1)
               screen2.title("Encryption")
               screen2.geometry("400x200")
               screen2.configure(bg="#fff")


               message=entry1.get(1.0,END)
               encode_message=message.encode("ascii")
               base64_bytes=base64.b64encode(encode_message)
               encrypt=base64_bytes.decode("ascii")


               Label(screen2,text="ENCRYPT",font="arial",fg="white",bg="#ed3833").place(x=10,y=0)
               text1=Text(screen2,font="Rpbote 10",bg="white",relief=GROOVE,wrap=WORD,bd=0)
               text1.place(x=10,y=40,width=380,height=150)

               text1.insert(END,encrypt)
        elif password=="":
               messagebox.showerror("encryption","enter passcode")
        elif password  !="Mridul":
               messagebox.showerror("encryption","enter valid passcode")
        


def decrypt_text():
        password=code.get()
        if password=="Mridul":
               screen3=Toplevel(screen1)
               screen3.title("Encryption")
               screen3.geometry("400x200")
               screen3.configure(bg="#fff")


               message=entry1.get(1.0,END)
               decode_message=message.encode("ascii")
               base64_bytes=base64.b64decode(decode_message)
               decrypt=base64_bytes.decode("ascii")


               Label(screen3,text="DECRYPT",font="arial",fg="white",bg="#00bd56").place(x=10,y=0)
               text1=Text(screen3,font="Rpbote 10",bg="white",relief=GROOVE,wrap=WORD,bd=0)
               text1.place(x=10,y=40,width=380,height=150)

               text1.insert(END,decrypt)

def main_screen():

    global screen1
    global code
    global entry1

   

    


    screen1=Tk()
    screen1.title("encryption system")
    screen1.geometry("400x400")
    screen1.resizable(False,False)

    lable1=Label(text="Enter the text for Encription and Decription",font=("Arial ",13))
    lable1.place(x=5,y=15)
    entry1=Text(screen1,width=18,fg="#000",border=0,bg='#fff',font=('Arial Bold',15))
    entry1.place(x=10,y=45,width=380,height=100)

    lable2=Label(text="Enter the secret key ",font=("Arial ",13))
    lable2.place(x=5,y=160)

    code=StringVar()

    entry2=Entry(textvariable=code,width=18,fg="#000",border=0,bg='#fff',font=('Arial Bold',15),show="*")
    entry2.place(x=10,y=190,width=380,height=30)

    Button1=Button(text="Encryption",bg="#E61919",fg="#fff",command=encrypt_text,font=('Arial Bold',12),bd=0)
    Button1.place(x=20,y=240,height=50,width=170)

    Button2=Button(text="Decryption",bg="#17E00E",fg="#fff",command=decrypt_text,font=('Arial Bold',12),bd=0)
    Button2.place(x=200,y=240,height=50,width=170)

    Button2=Button(text="Reset",bg="#0667FF",fg="#fff",command=reset,font=('Arial Bold',12),bd=0)
    Button2.place(x=115,y=300,height=50,width=170)

    screen1.mainloop()


main_screen()