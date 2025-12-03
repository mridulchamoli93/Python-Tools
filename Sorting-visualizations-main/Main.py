def Entry_widger(a):
    import sys 
    import tkinter as tk
    from tkinter import simpledialog
    root = tk.Tk() # needed to prevent extra window being created by dialog
    root.withdraw() # hide window as not needed
    username = simpledialog.askstring(a, 'Enter number of elements you want: ')
    yield(username)
    root.destroy()
def main(a):
   from BarGraph import Bar_Graph
   from ListMaker_Saver import List_Maker , Sortime
   from random import shuffle
   from LineGraph import Line_Graph
   from Sorting_Visualization import Working_Showcase,Sort_buble,swap,Insertion_sort,Quick_Sort
   from Sorting_Methods import quick_sort,partition,insertion_sort,bubble_sort
   if(a==1):
      entry=Entry_widger("User given Array")
      for i in entry:
         username=i
      limit=int(username)
      p=list(range(limit))#creating list to be sorted
      shuffle(p)#shuffling list
      shuffle(p)
      m=p.copy()#making Copy one of list p
      n=p.copy()#maiking Copy two of list p
      s=quick_sort(p,0,len(p)-1)
      r=insertion_sort(m)
      o=bubble_sort(n)
      Bar_Graph(s,r,o)
   elif(a==2):
      p=open("List_Number.txt","r")#Calucating for sorted list
      q=open("Quick_aes.txt","r")
      r=open("Insert_aes.txt","r")
      s=open("Bubble_aes.txt","r")
      title="Comparsion : Sorting sorted Arrays"
      p_str=p.read()
      q_str=q.read()
      r_str=r.read()
      s_str=s.read()
      
      p_list=p_str.split()
      q_list=q_str.split()
      r_list=r_str.split()
      s_list=s_str.split()

      Line_Graph(p_list,q_list,r_list,s_list,title)
      
      p.close()
      q.close()
      r.close()
      s.close()
   elif(a==3):
      p=open("List_Number.txt","r")#Calculating  for reverse sorted list
      q=open("Quick_des.txt","r")
      r=open("Insert_des.txt","r")
      s=open("Bubble_des.txt","r")
      title="Comparsion : Sorting reverse sorted Arrays "
      p_str=p.read()
      q_str=q.read()
      r_str=r.read()
      s_str=s.read()
      
      p_list=p_str.split()
      q_list=q_str.split()
      r_list=r_str.split()
      s_list=s_str.split()

      Line_Graph(p_list,q_list,r_list,s_list,title)
      
      p.close()
      q.close()
      r.close()
      s.close()
   elif(a==4):
      p=open("List_Number.txt","r")#Calculating for shuffled list
      q=open("Quick_shuff.txt","r")
      r=open("Insert_shuff.txt","r")
      s=open("Bubble_shuff.txt","r")
      title="Comparsion : Sorting shuffled Arrays"
      p_str=p.read()
      q_str=q.read()
      r_str=r.read()
      s_str=s.read()
      
      p_list=p_str.split()
      q_list=q_str.split()
      r_list=r_str.split()
      s_list=s_str.split()

      Line_Graph(p_list,q_list,r_list,s_list,title)
      
      p.close()
      q.close()
      r.close()
      s.close()
      
   elif(a==6):
      entry=Entry_widger("Quick Sort")
      for i in entry:
         username=i
      limit=int(username)
      Working_Showcase(1,limit)#Quick_Sort_trigger
      
   elif(a==7):
      entry=Entry_widger("Insertion Sort")
      for i in entry:
         username=i
      limit=int(username)
      Working_Showcase(2,limit)#Insertion_Sort_trigger
      
   elif(a==8):
      entry=Entry_widger("Bubble Sort")
      for i in entry:
         username=i
      limit=int(username)
      Working_Showcase(3,limit)#Bubble_Sort_triger
      
