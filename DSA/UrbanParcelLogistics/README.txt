Work flow

This module integrates module 1-4 to create a complete work flow.
It combines graphs based route planning, hash based customer
lookup, heap based parcel scheduling and sorting delivery records.

FILES:
LogisticSystem.py: The main file that showcases the work flow and
generates a report in a cvs format.

it NEEDS all the modules and imports them as packages.

WORKFLOW:
setupGraph creates a undirected weighted graph with 8 nodes and 11
edges, it sets up the delivery network.

loadCustomers populates a hash table with customer data, read from
CustomerData.csv

loadDeliveryRequests and scheduler.insertDeliveryRequest loads
requests from DeliverReq.csv, compute priority using customer data
and travel time, then insert them into a max heap

processNextDelivery extracts highest priority deliveries, updates
status to delivered in the hash table and stores results.

merge_sort sorts deliveries by travel time and generates DeliveryReport.csv
with customer details. Sorted by lowest travel time to highest.

HOW TO TEST:
linux environment: from desktop change directory to the root
folder, then type python3 -m UrbanParcelLogistics.LogisticSystem

Pycharm: Set the main directory to the source root, run the file.
