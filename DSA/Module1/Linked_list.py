"""Define a class to represent each node in the doubly linked list"""
class DSAListNode:
    # Constructor to initialize the node with a value and set next/prev to None
    def __init__(self, value):
        self.value = value      # Store the data value in the node
        self.next = None        # Pointer to the next node in the list (default None)
        self.prev = None        # Pointer to the previous node in the list (default None)

    # Getter method to return the value stored in the node
    def getValue(self):
        return self.value

    # Getter method to return the previous node
    def getPrev(self):
        return self.prev

    # Getter method to return the next node
    def getNext(self):
        return self.next

    # Setter method to update the value in the node
    def setValue(self, value):
        self.value = value

    # Setter method to update the next node reference
    def setNext(self, new_next):
        self.next = new_next

    # Setter method to update the previous node reference
    def setPrev(self, new_prev):
        self.prev = new_prev


"""Define a class to represent the doubly linked list itself"""
class DSALinkedList:
    # Constructor to initialize an empty list with no head or tail
    def __init__(self):
        self.head = None    # The first node in the list
        self.tail = None    # The last node in the list

    # Method to check if the list is empty
    def isEmpty(self):
        return self.head is None    # Returns True if head is None (i.e. list is empty)

    # Method to insert a new value at the beginning of the list
    def insertFirst(self, newValue):
        new_node = DSAListNode(newValue)    # Create a new node with the given value
        if self.isEmpty():                  # If the list is empty
            self.head = new_node            # Set both head and tail to the new node
            self.tail = new_node
        else:
            new_node.setNext(self.head)           # Link the new node to the current head
            self.head.setPrev(new_node)           # Link the current head back to the new node
            self.head = new_node                  # Update the head to be the new node

    # Method to insert a new value at the end of the list
    def insertLast(self, newValue):
        new_node = DSAListNode(newValue)    # Create a new node with the given value
        if self.isEmpty():                  # If the list is empty
            self.head = new_node            # Set both head and tail to the new node
            self.tail = new_node
        else:
            self.tail.setNext(new_node)          # Link the current tail to the new node
            new_node.setPrev(self.tail)          # Link the new node back to the current tail
            self.tail = new_node                 # Update the tail to be the new node


    # Method to remove and return the first element in the list
    def removeFirst(self):
        if self.isEmpty():                        # Raise an error if the list is empty
            raise Exception("The list is empty")
        value = self.head.getValue()              # Store the value to return later
        if self.head == self.tail:                # If there's only one node
            self.head = None                      # Set both head and tail to None
            self.tail = None
        else:
            self.head = self.head.getNext()       # Move head to the next node
            self.head.setPrev(None)               # Remove the previous link from new head
        return value                              # Return the removed value

    # Method to remove and return the last element in the list
    def removeLast(self):
        if self.isEmpty():                        # Raise an error if the list is empty
            raise Exception("The list is empty")
        value = self.tail.getValue()              # Store the value to return later
        if self.head == self.tail:                # If there's only one node
            self.head = None                      # Set both head and tail to None
            self.tail = None
        else:
            self.tail = self.tail.getPrev()       # Move tail to the previous node
            self.tail.setNext(None)               # Remove the next link from new tail
        return value                              # Return the removed value

    def get_count(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.getNext()
        return count