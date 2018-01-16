import random

# quickSort implementation (in-place)

def read_file(file_path):
    # Read the input file and return a dict with "grade" key
    # {grades: [last,first]}

    r_dict = {}
    for line in open(file_path,'r'):
        [last, first, grade] = line.rstrip('\n').split(', ')
        # print (last, first, grade)
        grade = int(grade)
        if not r_dict.get(grade):
            r_dict[int(grade)] = []
        r_dict[int(grade)] += [(last, first)] # ppl with same scores
    return r_dict

def write_file(file_path,info_dict,arr):

    with open(file_path,'w') as f:
        for grade in arr:
            # print info_dict[grade]
            for (last,first) in info_dict[grade]:
                s = "%s, %s, %s \n" % (last,first,str(grade))
                f.write(s)

def quicksort(arr):
    random.shuffle(arr)  # avoid quadratic-time worst case
    quicksort_helper(arr, 0, len(arr) - 1)


def quicksort_helper(arr, lo, hi):
    if hi <= lo:
        return
    j = partition(arr, lo, hi)
    quicksort_helper(arr, lo, j - 1)
    quicksort_helper(arr, j + 1, hi)


def partition(arr, lo, hi):
    def exchange(arr, i, j):
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp

    i = lo + 1
    j = hi
    pivot = arr[lo]
    while True:
        while arr[i] <= pivot:  # left to right
            i += 1
            if i == (hi + 1):  # boundary condition
                break
        while pivot <= arr[j]:
            j -= 1
            if j == (lo):  # boundary condition
                break
        if i >= j:
            break
        exchange(arr, i, j)
    exchange(arr, lo, j)
    return j

def main(input_file, output_file):
    info_dict = read_file(input_file)
    grade_arr = info_dict.keys()
    quicksort(grade_arr) # in-place quicksort funciton
    write_file(output_file,info_dict,grade_arr) #


if __name__ == '__main__':
    # arr = ['C', 'A', 'B', 'B', 'C', 'C', 'D']
    # quicksort(arr)
    # print(arr)

    # arr = read_file("unsorted.txt").keys()
    # quicksort(arr)
    # print(arr)
    input_file = "unsorted.txt"
    output_file = "sorted.txt"
    main(input_file,output_file)
