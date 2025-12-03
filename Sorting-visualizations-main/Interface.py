from tkinter import *
from tkinter.messagebox import showinfo
from Main import main

#==========================program for information======================================#
def info():
    def backA():
        about_program.destroy()

    about_program= Toplevel(root)
    about_program.geometry('700x150')
    about_program.title("ABOUT_PROGRAM")
    about_program.resizable(False,False)

    lbl= Label(about_program, text = '''This Program does the following-
                 1)- Showing How Various Sorting Algorithim Functions                 
               2)- Comparision Between Various Algorithim                        
        ''',font="time 15 bold",bg="light blue",fg="black")
    lbl.pack(side=TOP)

    backbutton1=Button(about_program,text="back",command=backA,bg ="red", fg ="white", height = 8, width = 20)
    backbutton1.pack(side=TOP)    
#==========================================================================================#

#===================program for start button on main screen================================#
def StartProgram():
    page1 = Toplevel(root)
    page1.geometry('400x350')
    page1.title("Chose any One ")
    page1.resizable(False,False)
    bgImage1=PhotoImage(file ="E.png")
    label1=Label(page1,image=bgImage).place(relwidth=1,relheight=1)




    def see_working():
        
        page2 = Toplevel(page1)
        page2.geometry('500x300')
        page2.title("working of sorting algorithim ")
        page2.resizable(False,False)
        bgImage2=PhotoImage(file ="E.png")
        labelw=Label(page2,image=bgImage).place(relwidth=1,relheight=1)


        entry1 = Entry(page2,width =20)
        entry1.pack(anchor=NE)
       

        def Quick_Sort():
            main(6)

        def Insertion_Sort():
            main(7)
        def bubble_Sort():
            main(8)

        def backC():
            page2.destroy()
        

        button_quicksort = Button(page2, text = "Quick Sort", bg ="red", fg ="black", command =Quick_Sort,height = 4, width = 20) 
        button_quicksort.pack(side=TOP, anchor=NW)
    
        button_insertionsort = Button(page2, text = "Insertion sort", bg ="green", fg ="black", command =Insertion_Sort ,height = 4, width = 20) 
        button_insertionsort.pack(side=TOP, anchor=NW)

        button_Bubblesort = Button(page2, text = "Bubble Sort", bg ="orange", fg ="black", command =bubble_Sort ,height = 4, width = 20) 
        button_Bubblesort.pack(side=TOP, anchor=NW)

        backC = Button(page2, text = "back", bg ="yellow", fg ="black", command = backC,height = 4, width = 20) 
        backC.pack(side=TOP, anchor=NW)

        
       

            


    def comparision():
        page3 = Toplevel(page1)
        page3.geometry('400x300')
        page3.title("working of Sorting algorithims ")
        page3.resizable(False,False)
        bgImage3=PhotoImage(file ="E.png")
        label3=Label(page3,image=bgImage).place(relwidth=1,relheight=1)

        def ascending_order():
            main(2)

        def shuffel():
            main(4)

        def decending_order():
            main(3)

        

        def backD():
            page3.destroy()

        button_ascending= Button(page3, text = "Ascending Order", bg ="red", fg ="black", command =ascending_order ,height = 4, width = 20) 
        button_ascending.pack(side=TOP, anchor=NW)
    
        button_shuffel = Button(page3, text = "Shuffel", bg ="green", fg ="black", command =shuffel ,height = 4, width = 20) 
        button_shuffel.pack(side=TOP, anchor=NW)

        button_decending = Button(page3, text = "Dscending Orders", bg ="orange", fg ="black", command =decending_order,height = 4, width = 20) 
        button_decending.pack(side=TOP, anchor=NW)
        
        backD = Button(page3, text = "back", bg ="white", fg ="black", command =backD,height = 4, width = 20) 
        backD.pack(side=TOP, anchor=NW)


    def backB():
        page1.destroy()



    button_working = Button(page1, text = "See Working", bg ="red", fg ="black", command =see_working,height = 4, width = 20) 
    button_working.pack(padx=12,pady=13)
    
    button_comparision = Button(page1, text = "comparision", bg ="green", fg ="black", command = comparision,height = 4, width = 20) 
    button_comparision.pack(padx=13,pady=13)

    backB = Button(page1, text = "back", bg ="yellow", fg ="black", command = backB,height = 4, width = 20) 
    backB.pack(padx=14,pady=13)    

#=========================DESTROY THE BASIC WINDOW==========================================#
def quitApp():
    root.destroy()
#===========================================================================================#


#=========================for showing devloper info=======================================#
def about():
    showinfo("Code Devloped By-","Mridul")
#==========================================================================================#


#========================mainwindow=======================================================#
if __name__ == '__main__':
    #Basic tkinter setup
    root = Tk()
    root.title("Comparision Program")

    bgImage=PhotoImage(file ="happy.png")
    label=Label(root,image=bgImage).place(relwidth=1,relheight=1)
   
    

    root.geometry("400x300")
    root.resizable(False,False)



    #=========================Lets create a menuba======================================#
    MenuBar = Menu(root)
    #===================================================================================#


    #====================================Help Menu Starts================================#
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label = "About Program", command=about)
    MenuBar.add_cascade(label="HELP", menu=HelpMenu)


    
    button1 = Button(root, text = "Start", bg ="red", fg ="white", command = StartProgram,height = 4, width = 20) 
    button1.pack(side=TOP)


    button2 = Button(root, text = "info", bg ="green", fg ="white", command =info ,height = 4, width = 20) 
    button2.pack(side=TOP)


    button3 = Button(root, text = "Exit", bg ="light blue", fg ="black", command = quitApp,height = 4, width = 20) 
    button3.pack(side=TOP)

    root.config(menu=MenuBar)

    

    root.mainloop()
