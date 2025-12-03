import random
import matplotlib.pyplot as plt
import matplotlib.animation as anim


def swap(A, i, j):
    a = A[j]
    A[j] = A[i]
    A[i] = a
    # also in python A[i],A[j]=A[j],A[i]


def Sort_buble(arr):
    if (len(arr) == 1):
        return
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if (arr[j] > arr[j + 1]):
                swap(arr, j, j + 1)
            yield arr

def Insertion_sort(arr):
    if(len(arr)==1):
        return
    for i in range(1,len(arr)):
        j = i
        while(j>0 and arr[j-1]>arr[j]):
            swap(arr,j,j-1)
            j-=1
            yield arr

def Quick_Sort(arr,p,q):
    if(p>=q):
        return
    piv = arr[q]
    pivindx = p
    for i in range(p,q):
        if(arr[i]<piv):
            swap(arr,i,pivindx)
            pivindx+=1
        yield arr
    swap(arr,q,pivindx)
    yield arr

    yield from Quick_Sort(arr,p,pivindx-1)
    yield from Quick_Sort(arr,pivindx+1,q)

def Working_Showcase(al,n):
    array = [i + 1 for i in range(n)]
    random.shuffle(array)
    if(al==3):
        title = "Bubble Sort"
        algo = Sort_buble(array)
    elif(al==2):
        title = "Insertion Sort"
        algo = Insertion_sort(array)
    elif(al==1):
        title = "Quick Sort"
        algo = Quick_Sort(array,0,n-1)
            # Initialize fig
    fig, ax = plt.subplots()
    ax.set_title(title)

    bar_rec = ax.bar(range(len(array)), array, align='edge')

    ax.set_xlim(0, n)
    ax.set_ylim(0, int(n * 1.1))

    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    epochs = [0]


    def update_plot(array, rec, epochs):
        for rec, val in zip(rec, array):
            rec.set_height(val)
        epochs[0]+= 1
        text.set_text("No. of operations :{}".format(epochs[0]))


    anima = anim.FuncAnimation(fig, func=update_plot, fargs=(bar_rec, epochs), frames=algo, interval=100, repeat=False)
    plt.show()

