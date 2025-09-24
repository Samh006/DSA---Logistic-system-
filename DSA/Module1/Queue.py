import numpy as np

"""
Abstract parent class for Queue implementations.
Provides common methods and structure for queue-based ADTs.
"""
class DSAQueue:
    DEFAULT_CAPACITY = 100                                  # Default queue capacity

    def __init__(self, capacity=DEFAULT_CAPACITY):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")   # Ensure capacity is valid
        self.capacity = capacity                            # Set queue capacity
        self.queue = np.empty(capacity, dtype=object)       # General-purpose object array
        self.count = 0                                      # Tracks the number of elements

    def get_count(self):
        return self.count                   # Return the current number of elements in the queue

    def is_empty(self):
        return self.count == 0              # Check if queue is empty

    def is_full(self):
        return self.count == self.capacity  # Check if queue is full

    def enqueue(self, value):
        raise NotImplementedError("enqueue() must be implemented in subclass")  # Placeholder for subclass implementation

    def dequeue(self):
        raise NotImplementedError("dequeue() must be implemented in subclass")  # Placeholder for subclass implementation

    def peek(self):
        if self.is_empty():
            raise Exception("Queue is empty")     # Prevent peeking if queue is empty
        return self.queue[0]                      # Default behavior, overridden in circular queue

    def __str__(self):
        return str(self.queue[:self.count])      # Default string representation

"""
Shuffling Queue implementation (First-In-First-Out)
Shuffling Queue shifts all elements left when dequeuing, 
making it O(n) and inefficient for large queues.
https://www.geeksforgeeks.org/array-implementation-of-queue-simple/
"""
class DSASqueue(DSAQueue):
    def enqueue(self, value):
        if self.is_full():
            raise Exception("Queue is full")     # Prevent adding if queue is full
        self.queue[self.count] = value           # Add value to the end of the queue
        self.count += 1                          # Increase count to reflect new item

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")     # Prevent removing if queue is empty
        front_val = self.queue[0]                 # Get the front value
        for i in range(1, self.count):
            self.queue[i - 1] = self.queue[i]     # Shift elements left to maintain order
        self.count -= 1                           # Reduce count to remove item
        return front_val                          # Return removed value

    def __str__(self):
        return str(self.queue[:self.count])       # String representation of active elements