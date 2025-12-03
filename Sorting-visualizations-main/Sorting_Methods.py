#Part of Quick sort function
def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot 
    for j in range(low, high): 
        # If current element is smaller than or
        # equal to pivot
        if arr[j] <= pivot:
            # increment index of smaller element
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
 
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index
# Function to do Quick sort
def quick_sort(arr, low, high):
    import time
    Start=time.time()
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi-1)
        quick_sort(arr, pi+1, high)
    End=time.time()
    Time_taken=End-Start
    return Time_taken
        

# Function to do Insertion sort
def insertion_sort(arr):
    import time
    Start=time.time()
    # Traverse through 1 to len(arr) 
    for i in range(1, len(arr)):   
        key = arr[i]   
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key
    End=time.time()
    Time_taken= End-Start
    return Time_taken



        
        
#Function to do Bubble sort
def bubble_sort(arr):
    import time
    Start=time.time()
    n = len(arr) 
    # Traverse through all array elements 
    for i in range(n-1): 
    # range(n) also work but outer loop will repeat one time more than needed.   
        # Last i elements are already in place 
        for j in range(0, n-i-1):  
            # traverse the array from 0 to n-i-1 
            # Swap if the element found is greater 
            # than the next element 
            if arr[j] > arr[j+1] : 
                arr[j], arr[j+1] = arr[j+1],arr[j]
    End=time.time()
    Time_taken=End-Start
    return Time_taken





                
