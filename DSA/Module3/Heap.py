import numpy as np
from Module3.HeapEntry import DSAHeapEntry

class DSAHeap:  # Define the DSAHeap class for max heap implementation
    def __init__(self, capacity=100):  # Constructor for DSAHeap
        if capacity <= 0:              # Check if capacity is positive
            raise ValueError("capacity must be positive")
        self.heap = np.empty(capacity, dtype=object)  # Create fixed-size numpy array for heap storage
        for i in range(capacity):                     # Iterate through each index in the array
            self.heap[i] = None                       # Initialize each slot to None
        self.count = 0                                # Initialize count
        self.capacity = capacity                      # Store the heap capacity

    """Insert a delivery request with its priority score and travel time."""
    def insert(self, priority, customer_id, destination_hub, travel_time):
        if self.count >= self.capacity:      # Check if heap is full
            raise Exception("Heap is full")
        if not isinstance(customer_id, int) or not isinstance(destination_hub, str):  # Validate input types
            raise ValueError("Invalid customer id or destination hub")                # Raise error for invalid types
        entry = DSAHeapEntry(priority, customer_id, destination_hub, travel_time)     # Create new heap entry
        self.heap[self.count] = entry                        # Place entry at the end of the heap
        self.trickleUp(self.count)                           # Restore max heap property by bubbling up
        self.count += 1                                      # Increment count of entries
        self.log_state("Insert", entry)             # Log the heap state after insertion

    """Remove and return the highest priority delivery from the heap."""
    def extract_priority(self):
        if self.count == 0:                   # Check if heap is empty
            raise Exception("Heap is empty")
        root = self.heap[0]                    # Store the root (highest priority) entry
        self.count -= 1                        # Decrement count of entries
        self.heap[0] = self.heap[self.count]   # Move last entry to root
        self.heap[self.count] = None           # Clear the last slot
        if self.count > 0:                     # Check if there are entries left to trickle down
            self.trickleDown(0)                # Restore max heap property by bubbling down
        self.log_state("Extract", root)  # Log the heap state after extraction
        return root                               # Return the extracted entry

    """Bubble up a node to restore the max heap property"""
    def trickleUp(self, index):
        currentIdx = index                 # Start at the given index
        parentIdx = (currentIdx - 1) // 2  # Calculate parent index

        # Continue while not at root and current priority is greater than parent
        while currentIdx > 0 and self.heap[currentIdx].getPriority() > self.heap[parentIdx].getPriority():
            self.heap[currentIdx], self.heap[parentIdx] = self.heap[parentIdx], self.heap[currentIdx]  # Swap current node with parent
            currentIdx = parentIdx              # Move to parent index
            parentIdx = (currentIdx - 1) // 2   # Recalculate new parent index

    """Bubble down a node to restore the max heap property."""
    def trickleDown(self, index):
        currentIdx = index              # Start at the given index
        lChildIdx = 2 * currentIdx + 1  # Calculate left child index
        swapped = True                  # Flag to track
        while lChildIdx < self.count and swapped:  # Continue while left child exists and swaps occurred
            swapped = False                        # Reset swap flag
            rChildIdx = lChildIdx + 1              # Calculate right child index
            largeIdx = lChildIdx                   # Assume left child is larger

            # Check if right child exists and has higher priority
            if rChildIdx < self.count and self.heap[rChildIdx].getPriority() > self.heap[lChildIdx].getPriority():
                largeIdx = rChildIdx                                                     # Update to right child index
            if self.heap[largeIdx].getPriority() > self.heap[currentIdx].getPriority():  # Check if larger child has higher priority than current
                self.heap[currentIdx], self.heap[largeIdx] = self.heap[largeIdx], self.heap[currentIdx]  # Swap with larger child
                currentIdx = largeIdx                                                                    # Move to larger child index
                lChildIdx = 2 * currentIdx + 1  # Recalculate new left child index
                swapped = True                  # Mark that a swap occurred

    """Log the current state of the heap after an operation."""
    def log_state(self, operation, entry):
        print(f"{operation}: {entry}")          # Print the operation and entry details
        print("Heap state: [", end="")          # Start printing heap state
        for i in range(self.count):             # Iterate through current entries
            print(str(self.heap[i]), end="")    # Print each entry
            if i < self.count - 1:              # Check if not the last entry
                print(", ", end="")             # Print separator
        print("]")
        print()