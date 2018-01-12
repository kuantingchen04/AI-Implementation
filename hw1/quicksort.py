import random

def quicksort(arr):
    random.shuffle(arr) # avoid quadratic-time worst case
    quicksort_helper(arr,0,len(arr)-1)

def quicksort_helper(arr,lo,hi):
    if hi <= lo:
        return
    j = partition(arr,lo,hi)
    quicksort_helper(arr, lo, j-1)
    quicksort_helper(arr, j+1, hi)

def partition(arr,lo,hi):
    def exchange(arr,i,j):
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp

    i = lo + 1
    j = hi
    pivot = arr[lo]
    while True:
        while arr[i] <= pivot: # left to right
            i += 1
            if i == (hi+1): # boundary condition
                break
        while pivot <= arr[j]:
            j -= 1
            if j == (lo): # boundary condition
                break
        if i >= j:
            break
        exchange(arr,i,j)
    exchange(arr,lo,j)
    return j

if __name__ == '__main__':
    #arr = ['C','A','B','B','C','C','D']
    #arr = ['A','B','C','D']
    #pivot = partition(arr,0,len(arr)-1)
    #print (arr)
    #print (pivot)
    arr = ['C','A','B','B','C','C','D']
    quicksort(arr)
    print (arr)
