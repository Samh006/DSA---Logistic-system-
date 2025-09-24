import numpy as np
from Module2.HashEntry import CustomerEntry, hashError
from Module2.Customer import Customer

"""
Customer Hash Table Implementation
Uses linear probing for collision resolution
"""
class TableStats:
    def __init__(self, size, count, load_factor):
        self.size = size
        self.count = count
        self.load_factor = load_factor


class CustomerHashTable:
    MIN_SIZE = 53
    MAX_LOAD_FACTOR = 0.7
    MIN_LOAD_FACTOR = 0.3

    def __init__(self, size=53):
        if size < CustomerHashTable.MIN_SIZE:  # Check if provided size is less than minimum
            size = CustomerHashTable.MIN_SIZE  # Set size to minimum if too small
        self.size = size                       # Store the table size
        self.count = 0
        self.hash_array = np.empty(size, dtype=object)
        for i in range(size):                     # Iterate through each index in the array
            self.hash_array[i] = CustomerEntry()  # Initialize each slot with an empty CustomerEntry

    """Find the next prime number after the given number"""
    def _get_next_prime(self, num):  # Find the next prime number

        def is_prime(n):             # Helper function to check if a number is prime
            if n < 2:                # Check if number is less than 2
                return False         # Return False as it is not prime
            i = 2                    # Start checking divisibility from 2
            while i * i <= n:        # Check up to square root of n
                if n % i == 0:       # Check if n is divisible by i
                    return False     # Return False if divisible
                i += 1               # Increment divisor
            return True

        while not is_prime(num):  # Keep incrementing until a prime is found
            num += 1              # Increment the number
        return num                # Return the next prime number

    """Resize the hash table to a new capacity and rehash all entries."""
    def resize(self, new_capacity):
        new_capacity = self._get_next_prime(new_capacity)
        old_array = self.hash_array
        self.size = new_capacity
        self.hash_array = np.empty(self.size, dtype=object)

        for i in range(self.size):                # Iterate through new array
            self.hash_array[i] = CustomerEntry()  # Initialize each slot with an empty CustomerEntry

        self.count = 0  # Reset count of entries

        for entry in old_array:                          # Iterate through old array
            if entry.state == CustomerEntry.USED_STATE:  # Check if entry is used
                self.insert(entry.customer)              # Reinsert customer into new table

    """Compute the hash value for a customer ID."""
    def _hash(self, customer_id):
        return customer_id % self.size  # Return customer_id modulo table size

    """Find the slot for a customer ID using linear probing."""
    def _find_slot(self, customer_id, for_insert=False):
        start_idx = self._hash(customer_id)  # Compute initial hash index
        idx = start_idx                      # Start at the hash index

        for i in range(self.size):        # Iterate up to table size
            entry = self.hash_array[idx]  # Get entry at current index

            if for_insert:                # If searching for insertion
                if entry.state in (CustomerEntry.EMPTY_STATE, CustomerEntry.DELETED_STATE):  # Check if slot is empty or deleted
                    return idx                                                               # Return index for insertion
                elif entry.customer and entry.customer.getID() == customer_id:               # Check if customer ID matches
                    return idx                                                               # Return index for existing customer
            else:                                                                            # If searching for lookup
                if entry.state == CustomerEntry.EMPTY_STATE:                                 # Check if slot is empty
                    return -1                                                                # Return -1 as customer not found
                elif entry.customer and entry.customer.getID() == customer_id:               # Check if customer ID matches
                    return idx                  # Return index of found customer
            idx = (idx + 1) % self.size         # Move to next slot using linear probing
            if idx == start_idx:                # Check if we've looped back to start
                return -1 if not for_insert else idx  # Return -1 for lookup, current idx for insert
        return -1                                     # Return -1 if no slot found

    """Insert or update a customer in the hash table."""
    def insert(self, customer):
        if self.count >= self.size:
            raise Exception("Hash table is full")

        idx = self._find_slot(customer.getID(), for_insert=True)  # Find slot for insertion
        if idx == -1:                                             # Check if no slot was found
            raise Exception("Unable to insert customer")

        entry = self.hash_array[idx]                 # Get entry at found index
        if entry.state != CustomerEntry.USED_STATE:  # Check if slot is not already used
            self.count += 1                          # Increment count of entries

        entry.customer = customer               # Store customer in the entry
        entry.state = CustomerEntry.USED_STATE  # Mark entry as used

        if self.count / self.size > CustomerHashTable.MAX_LOAD_FACTOR:  # Check if load factor exceeds threshold
            self.resize(self.size * 2)                                  # Resize table to double the size
        return True                                                     # Return True to indicate success

    """Search for a customer by their ID."""
    def search(self, customer_id):
        idx = self._find_slot(customer_id)      # Find slot for customer ID
        if idx == -1:                           # Check if customer was not found
            raise hashError(f"customer ID {customer_id} not found")
        return self.hash_array[idx].customer                         # Return the customer object

    """Delete a customer from the hash table by their ID."""
    def delete(self, customer_id):
        idx = self._find_slot(customer_id)  # Find slot for customer ID
        if idx == -1:                       # Check if customer was not found
            return False                    # Return False if not found

        entry = self.hash_array[idx]  # Get entry at found index
        entry.customer = None         # Clear customer data
        entry.state = CustomerEntry.DELETED_STATE  # Mark entry as deleted

        self.count -= 1  # Decrement count of entries

        # Check if load factor is too low
        if (self.size > CustomerHashTable.MIN_SIZE and self.count / self.size < CustomerHashTable.MIN_LOAD_FACTOR):
            self.resize(max(self.size // 2, CustomerHashTable.MIN_SIZE))  # Resize to half size or minimum
        return True  # Return True to indicate successful deletion

    """Check if a customer with the given ID exists in the hash table."""
    def has_customer(self, customer_id):
        return self._find_slot(customer_id) != -1  # Return True if slot is found, False otherwise

    def get_statistics(self):  # Get hash table statistics
        return TableStats(self.size, self.count, self.count / self.size)  # Return TableStats object with current stats

    def update_delivery_status(self, customer_id, new_status):  # Update a customer's delivery status
        idx = self._find_slot(customer_id)  # Find slot for customer ID
        if idx == -1:                       # Check if customer was not found
            return False                    # Return False if not found

        self.hash_array[idx].customer.setDeliveryStatus(new_status)  # Update customer's delivery status
        return True                                                  # Return True to indicate successful update