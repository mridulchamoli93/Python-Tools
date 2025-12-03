def Bar_Graph(a,b,c):
   import matplotlib.pyplot as plt
   x=["Quick Sort","Insertion Sort","Bubble Sort"]
   y=[a,b,c]
   plt.bar(x, y, color='teal')
   plt.xlabel("Sorting Algorithm")
   plt.ylabel("Time Taken to Compute(In Seconds)")
   plt.title("Comparsion Of Sorting Algorithm")
   plt.show()
