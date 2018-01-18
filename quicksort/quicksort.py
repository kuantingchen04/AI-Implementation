import random
import csv

"""quickSort implementation (in-place)"""


def quicksort(arr):
    """Shuffle array & apply qs"""
    random.shuffle(arr)  # preprocess to avoid quadratic-time worst case
    quicksort_helper(arr, 0, len(arr) - 1)

def quicksort_helper(arr, lo, hi):
    """Recursive implementation of qs"""
    if hi <= lo:
        return
    j = partition(arr, lo, hi)
    quicksort_helper(arr, lo, j - 1)
    quicksort_helper(arr, j + 1, hi)

def partition(arr, lo, hi):
    """Let the arr[lo] be the pivot,find the right place to place arr[lo] such that left items< a[j] < right items"""
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
    exchange(arr, lo, j)  # switch pivot to right place
    return j

def read_file(file_path):
    """Read the input file and return a dict with {grades: [last,first]}"""
    r_dict = {}
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            [last, first, grade] = line[0], line[1], int(line[2])
            if grade not in r_dict:
                r_dict[grade] = []
            r_dict[grade] += [(last, first)]  # ppl with same scores
        return r_dict

def write_file(file_path, info_dict, arr):
    with open(file_path, 'w') as f:
        for grade in arr:
            for (last, first) in info_dict[grade]:
                csv_writer = csv.writer(f)
                row = [last, first, grade]
                csv_writer.writerow(row)

def main(input_file, output_file):
    """Set file input/output"""
    info_dict = read_file(input_file)
    grade_arr = info_dict.keys()
    quicksort(grade_arr)  # in-place quicksort funciton
    write_file(output_file, info_dict, grade_arr)

if __name__ == '__main__':

    INPUT_FILE = "unsorted.txt"
    OUTPUT_FILE = "sorted.txt"
    main(INPUT_FILE, OUTPUT_FILE)
