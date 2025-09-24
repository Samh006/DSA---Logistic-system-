import numpy as np

def merge_sort(A):
    # Check if input array is valid and has more than one element to sort
    if A is not None and len(A) > 1:
        # Call the recursive merge sort function with initial left and right indices
        merge_sort_recurse(A, 0, len(A) - 1)
    return A

def merge_sort_recurse(A, leftIdx, rightIdx):
    if leftIdx < rightIdx:                         # Proceed only if the subarray has more than one element
        midIdx = (leftIdx + rightIdx) // 2         # Calculate the middle index to divide the array into two halves
        merge_sort_recurse(A, leftIdx, midIdx)       # Recursively sort the left half of the subarray
        merge_sort_recurse(A, midIdx + 1, rightIdx)  # Recursively sort the right half of the subarray
        merge(A, leftIdx, midIdx, rightIdx)        # Merge the two sorted halves into a single sorted subarray

def merge(A, leftIdx, midIdx, rightIdx):
    tempArr = np.empty(rightIdx - leftIdx + 1, dtype=object)   # Create a temporary array to store the merged result
    ii = leftIdx                                               # Initialize index for the left subarray
    jj = midIdx + 1                                            # Initialize index for the right subarray
    kk = 0                                                     # Initialize index for the temporary array

    while ii <= midIdx and jj <= rightIdx:                 # Compare elements from both subarrays and merge them in sorted order
        if A[ii].getTravelTime() <= A[jj].getTravelTime():   # If the left subarray element is smaller or equal, add it to tempArr
            tempArr[kk] = A[ii]                            # Copy the left subarray element to the temporary array
            ii += 1                                        # Move to the next element in the left subarray
        else:                                              # If the right subarray element is smaller, add it to tempArr
            tempArr[kk] = A[jj]                            # Copy the right subarray element to the temporary array
            jj += 1                                        # Move to the next element in the right subarray
        kk += 1                                            # Move to the next position in the temporary array

    while ii <= midIdx:                           # Copy any remaining elements from the left subarray to tempArr
        tempArr[kk] = A[ii]                       # Add the remaining left subarray element to tempArr
        ii += 1                                   # Move to the next element in the left subarray
        kk += 1                                   # Move to the next position in the temporary array


    while jj <= rightIdx:                         # Copy any remaining elements from the right subarray to tempArr
        tempArr[kk] = A[jj]                       # Add the remaining right subarray element to tempArr
        jj += 1                                   # Move to the next element in the right subarray
        kk += 1                                   # Move to the next position in the temporary array


    for kk in range(len(tempArr)):                # Copy the sorted elements from tempArr back to the original array
        A[leftIdx + kk] = tempArr[kk]             # Place the sorted element in its correct position in the original arr

"""Sorts an array of DeliveryRecord objects by estimated_time using Quick Sort with median-of-three pivot."""


def quick_sort_median3(A):
    # Only proceed if the array is not None and has more than one element
    if A is not None and len(A) > 1:
        quick_sort_median3_recurse(A, 0, len(A) - 1)
    return A


def quick_sort_median3_recurse(A, leftIdx, rightIdx):
    # Base case: only sort if left index is less than right index
    if rightIdx > leftIdx:
        midIdx = (leftIdx + rightIdx) // 2

        # Median-of-three pivot selection
        # Ensure A[leftIdx] <= A[midIdx]
        if A[leftIdx].getTravelTime() > A[midIdx].getTravelTime():
            A[leftIdx], A[midIdx] = A[midIdx], A[leftIdx]
        # Ensure A[leftIdx] <= A[rightIdx]
        if A[leftIdx].getTravelTime() > A[rightIdx].getTravelTime():
            A[leftIdx], A[rightIdx] = A[rightIdx], A[leftIdx]
        # Ensure A[midIdx] <= A[rightIdx]
        if A[midIdx].getTravelTime() > A[rightIdx].getTravelTime():
            A[midIdx], A[rightIdx] = A[rightIdx], A[midIdx]

        # Use the median as the pivot
        pivotIdx = midIdx
        # Partition the array and get the final position of the pivot
        newPivotIdx = do_partitioning(A, leftIdx, rightIdx, pivotIdx)
        # Recursively sort the subarrays on either side of the pivot
        quick_sort_median3_recurse(A, leftIdx, newPivotIdx - 1)
        quick_sort_median3_recurse(A, newPivotIdx + 1, rightIdx)


def do_partitioning(A, leftIdx, rightIdx, pivotIdx):
    # Get the pivot value and move it to the end temporarily
    pivotVal = A[pivotIdx].getTravelTime()
    A[pivotIdx], A[rightIdx] = A[rightIdx], A[pivotIdx]

    currIdx = leftIdx  # Tracks the position for elements less than pivot
    for ii in range(leftIdx, rightIdx):
        # If current element is less than pivot, swap it into the left partition
        if A[ii].getTravelTime() < pivotVal:
            A[ii], A[currIdx] = A[currIdx], A[ii]
            currIdx += 1
    # Move the pivot into its final position
    A[currIdx], A[rightIdx] = A[rightIdx], A[currIdx]
    return currIdx  # Return the pivot's final position
