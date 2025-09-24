Sorting delivery records

This module implements sorting functionality to organize
end of day delivery records by est delivery time. It uses
Merge sort and quick sort median of 3 to sort datasets.
In this module, I have modified TestSortsHarness.py to
generate data sets of 100, 500 and 1000. TestSortsHarness.py
was given to us during our practical classes.

FILES:
SortRecords.py: implements a merge sort and quick sort median
of 3 for sorting DeliveryRes objects by travel time.

Module4_test.py tests sorting performance on datasets of 100,
500 and 1000 parcels with three different states (random,
nearly sorted and reversed). It also generates a comparison
graph using matplotlib

SORTING ALGORITHMS:
merge_sort uses divide and conquer to sort DeliveryRes objects
by travel times. Its stable with O(n log n) time complexity and
O(n) space complexity

quick_sort_median3 uses median of three pivot to reduce worst case
scenarios. It was chosen over the regular quick sort since the regular
quick sort was slow and above 950 elements we would get a recursion
error. O(n log n) average time, O(n^2) worst case, O(log n) space and
not stable.

HOW TO TEST:
linux environment: from desktop change directory to the root
folder, then type python3 -m Module4.Module4_test

Pycharm: Set the main directory to the source root, run the
test file.