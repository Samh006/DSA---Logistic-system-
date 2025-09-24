Hash based customer look up

This module implements a hash based customer look up system.
It enables fast retrieval of customer information via
customer ID's. This module includes a hash table with linear
probing for collusion handling.

FILES:
- Customer.py: Defines the customer class with fields for ID, name,
  address, priority level (1-5) and delivery status

- HashEntry.py: Defines CustomerEntry for hash table slots

- HashTable.py: CustomerHashTable with linear probing, resizing and
core operations

- LookUpCustomer: provides an interface for hash table operations

- Module2_test.py: Tests functionality, collision handling, resizing
and error cases using CustomerData.csv for entries.

COMPLEXITY:
insert/search/delete: O(1) avg, O(n) worst case due to linear probing
resizing: O(n) when triggered by load factor thresholds

FUNCTIONALITY
- insert adds customers and resizes if load factor is greater
  than 0.7

- search retrieves customers by ID, raise error if not found.

- delete marks entries as deleted and resizes if load factor drops
  below 0.3

- update_delivery_status modifies delivery status

COLLISION HANDLING
linear probing takes care of collisions by checking sequential slots.
Tested in Module2_test.py with ID'S 53 and 105 which hash to the same
index, 0.

HOW TO TEST:
linux environment: from desktop change directory to the root
folder, then type python3 -m Module2.Module2_test

Pycharm: Set the main directory to the source root, run the
test file.




