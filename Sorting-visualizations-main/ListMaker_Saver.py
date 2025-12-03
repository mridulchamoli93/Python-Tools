def List_Maker():
   a=int(input("Enter No. of Element(First List)"))
   b=int(input("Enter No. of Element(Last List)"))
   c=int(input("Incerement in Size with "))
   from random import shuffle
   Sorted_List=[]#list with all element sorted
   number=[]#number of element in list
   i=a
   while i<b+1:
      t=list(range(i))
      Sorted_List.append(t)
      number.append(i)
      i=i+c
      
   return Sorted_List,number
def Sortime():
   from Sorting_Methods import quick_sort,partition,insertion_sort,bubble_sort
   from LineGraph import Line_Graph
   import sys
   from random import shuffle
   sys.setrecursionlimit(10**4)
   a,x=List_Maker()
   b=a.copy()
   c=a.copy()
   
   Quick=open("Quick_aes.txt","w")  
   Insert=open("Insert_aes.txt","w")  
   Bubble=open("Bubble_aes.txt","w")
   for i in a:
      j=len(i)-1
      r= (str((bubble_sort(i))) + " ")
      p= (str((quick_sort(i,0,j))) + " ")
      q= (str((insertion_sort(i)))+ " ")
      Quick.write(p)
      Insert.write(q)
      Bubble.write(r)
   Quick.close()
   Insert.close()
   Bubble.close()
   
   Quick=open("Quick_des.txt","w")  
   Insert=open("Insert_des.txt","w")  
   Bubble=open("Bubble_des.txt","w")
   for i in b:
      j=len(i)-1
      i.reverse()
      r= (str((bubble_sort(i))) + " ")
      i.reverse()
      p= (str((quick_sort(i,0,j))) + " ")
      i.reverse()
      q= (str((insertion_sort(i)))+ " ")
      Quick.write(p)
      Insert.write(q)
      Bubble.write(r)
   Quick.close()
   Insert.close()
   Bubble.close()
   
   Quick=open("Quick_shuff.txt","w")  
   Insert=open("Insert_shuff.txt","w")  
   Bubble=open("Bubble_shuff.txt","w")
   for i in c:
      j=len(i)-1
      shuffle(i)
      r= (str((bubble_sort(i))) + " ")
      shuffle(i)
      p= (str((quick_sort(i,0,j))) + " ")
      shuffle(i)
      q= (str((insertion_sort(i)))+ " ")
      Quick.write(p)
      Insert.write(q)
      Bubble.write(r)
   Quick.close()
   Insert.close()
   Bubble.close()
   List_No=open("List_Number.txt","w")
   for i in x :
      aa=str(i)
      a=(aa)+" "
      List_No.write(a)
   List_No.close()
 
