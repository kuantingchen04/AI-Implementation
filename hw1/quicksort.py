import random

def get_grades(file_path):
    grades = []
    for line in open(file_path):
        grades.append(int(line.split(",")[-1]))
    return grades

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
    arr = ['C','A','B','B','C','C','D']
    arr = [1,2,2,2]
    quicksort(arr)
    print (arr)

    g = get_grades("unsorted.txt")
    print (g,len(g))
    quicksort(g)
    print (g,len(g))
