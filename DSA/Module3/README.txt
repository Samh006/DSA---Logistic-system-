Heap based parcel scheduling

This module implements a heap based parcel scheduling system to
prioritize deliveries based on customer priority and estimated
travel time. It integrates with module 1 and module 2 to compute
delivery priorities and schedule them efficiently.

FILES:
- Heap.py: Implements a max heap for prioritizing deliveries.

- HeapEntry.py: Defines HeapEntry for storing delivery details
  (priority, customer ID, hub, travel time).

- DeliveryRes.py: Defines DeliveryRes for delivery results.

- Schedule.py: Implements DeliveryScheduler, integrating
  Modules 1 and 2 with the heap.

- Module3_test.py: Tests scheduling with DeliveryReq.csv and
  CustomerData.csv.

COMPLEXITY:
insert: O(log n) via trickleUP
Extract: O(log n) via trickleDown
Space: O(n) for n deliveries

FUNCTIONALITY:
insertDeliveryRequest in Schedule.py:
- Fetch customer data from Module 2 (LookUpCustomer)
- Compute travel time from module 1 (dijkstra)
- Calculate the priority using the formula
- Insert into heap

processNextDelivery in schedule.py:
- Remove and return the highest priority delivery as a
  DeliveryRes object

- Logs heap status after each operation (log_state)

HOW TO TEST:
linux environment: from desktop change directory to the root
folder, then type python3 -m Module3.Module3_test

Pycharm: Set the main directory to the source root, run the
test file.



