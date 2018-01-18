import unittest
import quicksort
# import numpy as np
import random

def partition(alist,first,last):
   pivotvalue = alist[first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp
   return rightmark


class TestQS(unittest.TestCase):
    # arr = ['C', 'A', 'B', 'B', 'C', 'C', 'D']
    # quicksort(arr)
    # print(arr)

    def test_partition(self):
        arr = [54, 26, 93, 17, 77, 31, 44, 55, 20]
        # self.assertEqual(quicksort.partition(arr,1,5),partition(arr,1,5))

    def test_neg_output(self):
        arr1 = [54, 26, 93, 17, 77, 31, 44, 55, 20, 20, -10]
        arr2 = arr1[:]
        quicksort.quicksort(arr1),arr2.sort()
        self.assertEqual(arr1,arr2)

    def test_float_output(self):
        # arr1 = np.random.rand(20)
        arr1 = [random.random() for _ in range(100)]
        arr2 = arr1[:]
        quicksort.quicksort(arr1), arr2.sort()
        self.assertEqual(arr1,arr2)

if __name__ == '__main__':
    unittest.main()