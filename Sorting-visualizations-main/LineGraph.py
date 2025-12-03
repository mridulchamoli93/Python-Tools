def Line_Graph(a,b,c,d,e):
   import matplotlib.pyplot as plt#a no of list element
   plt.plot(b, a, label = "Quick Sort")
   plt.plot(c, a, label = "Insertion Sort")
   plt.plot(d, a, label = "Bubble Sort")
   plt.xticks([])
   plt.yticks([])
   plt.xlabel('Time Taken to Sort(In Seconds)')
   plt.ylabel('Number of Element In ArrayTime Taken to Sort')    # Set the y axis label of the current axis 
   plt.title(e)    # Set a title of the current axes.
   plt.legend()  # show a legend on the plot
   plt.show()    # Display a figure.
