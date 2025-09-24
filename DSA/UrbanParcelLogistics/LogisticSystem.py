import numpy as np
from Module1.Graph import DSAGraph
from Module1.Linked_list import DSALinkedList
from Module1.GraphVertex import Edge
from Module2.LookUpCustomer import LookUpCustomer
from Module2.Customer import Customer
from Module3.Schedule import DeliveryScheduler
from Module3.DeliveryRes import DeliveryRes
from Module4.SortRecords import merge_sort
import os

def setupGraph():
    graph = DSAGraph()          # Create a new directed graph to represent the delivery network
    charNodes = "ABCDEFGH"      # Define a string of node labels (A to H) representing hubs
    edges = DSALinkedList()     # Create a linked list to store edge objects for the graph

    edges.insertLast(Edge('A', 'B', 4))
    edges.insertLast(Edge('A', 'C', 3))
    edges.insertLast(Edge('C', 'F', 3))
    edges.insertLast(Edge('B', 'E', 6))
    edges.insertLast(Edge('B', 'D', 4))
    edges.insertLast(Edge('C', 'G', 7))
    edges.insertLast(Edge('D', 'E', 3))
    edges.insertLast(Edge('E', 'F', 4))
    edges.insertLast(Edge('F', 'G', 5))
    edges.insertLast(Edge('D', 'F', 2))
    edges.insertLast(Edge('B', 'G', 8))

    for node in charNodes:       # Iterate through each node label
        graph.addVertex(node)    # Add vertex for each hub (A, B, C, etc.)
    current = edges.head         # Get the head of the edges linked list to iterate

    while current:                                                         # Iterate through the linked list of edges
        edge = current.getValue()                                          # Get the current edge object
        graph.addEdge(edge.getSource(), edge.getDest(), edge.getWeight())  # Add edge to graph with source, dest, weight
        current = current.getNext()   # Move to the next edge in the linked list
    return graph                      # Return the fully constructed graph

"""Helper function to get the absolute path for data files"""
def get_data_path(filename):
    module_dir = os.path.dirname(os.path.abspath(__file__))    # Get the directory of the current script file
    return os.path.join(module_dir, filename)                  # Join directory with filename for absolute path

def loadCustomers(filename):
    csv_path = get_data_path(filename)  # Get absolute path to customer data file
    lookup = LookUpCustomer()           # Create a new LookUpCustomer object to store customer data

    try:
        with open(csv_path, 'r') as file:
            header = True

            for line in file:
                line = line.strip()
                if header:
                    header = False
                    continue
                if not line or line.startswith('#'):
                    continue
                fields = line.split(',')

                if len(fields) == 5:   # Check if the line has exactly 5 fields (id, name, address, etc.)
                    try:               # Try to create a Customer object
                        customer = Customer(int(fields[0]), fields[1].replace('_', ' '),            # Create Customer with ID, name
                                            fields[2].replace('_', ' '), int(fields[3]), fields[4]) # address, phone, hub
                        lookup.insertCustomer(customer)      # Insert the customer into the lookup hash table
                    except Exception as e:
                        print(f"Skipping invalid customer entry: {line} ({e})")
    except FileNotFoundError:
        print(f"{filename} was not found")
    return lookup          # Return the populated customer lookup object

def loadDeliveryRequests(filename):
    csv_path = get_data_path(filename) # Get absolute path to delivery requests file
    requests = DSALinkedList() # Create linked list to store delivery requests

    try:
        with open(csv_path, 'r') as file:
            header = True

            for line in file:
                line = line.strip()
                if header:           # Check if the current line is the header
                    header = False   # Skip the header row
                    continue
                if not line or line.startswith('#'):
                    continue                # Move to the next line
                fields = line.split(',')    # Split the line

                if len(fields) == 2:     # Check if the line has exactly 2 fields (customer ID, destination hub)
                    try:                 # Try to create a DeliveryRes object
                        request = DeliveryRes(int(fields[0]), fields[1], None) # Create DeliveryRes with ID, hub
                        requests.insertLast(request)                                     # Insert delivery request into the linked list
                    except ValueError:
                        print(f"Skipping invalid requests: {line}")
    except FileNotFoundError:
        print(f"{filename} was not found")
    return requests  # Return the linked list of delivery requests

def processDeliveries():
    print("=== Main delivery work flow ===")

    print("\n1) Initializing deliver network and processing customer data")
    graph = setupGraph()                           # Set up the delivery network graph
    lookup = loadCustomers("CustomerData.csv")     # Load customer data from CSV file
    scheduler = DeliveryScheduler(graph, lookup)   # Create DeliveryScheduler with graph and customer lookup

    print("\nDelivery network system:")
    graph.displayAsList()                # Display the delivery network as an adjacency list

    stats = lookup.ht.get_statistics()   # Get statistics of the customer hash table
    print(f"\nCustomer database stats: size = {stats.size}, count = {stats.count}, load factor = {stats.load_factor:.3f}")

    print("\n2) Scheduling delivery requests")
    requests = loadDeliveryRequests("DeliveryReq.csv")  # Load delivery requests from CSV file

    valid_requests = 0                                 # Initialize counter for valid delivery requests
    current = requests.head                            # Get the head of the requests linked list

    while current:                                     # Iterate through the delivery requests
        request = current.getValue()                   # Get the current delivery request
        customer_id = request.getCustomerID()          # Get the customer ID from the request
        destination_hub = request.getDestinationHub()  # Get the destination hub from the request

        try:   # Try to schedule the delivery request
            if scheduler.insertDeliverRequest(customer_id, destination_hub):  # Schedule the request
                valid_requests += 1         # Increment counter if request is successfully scheduled
        except Exception as e:
            print(f"Rejected request (Customer {customer_id}, Hub: {destination_hub}): {e}\n")
        current = current.getNext()    # Move to the next request in the linked list
    print(f"\nScheduled {valid_requests} valid delivery requests")

    print("\n3) processing the deliveries in priority order")        # Announce step 3: processing deliveries
    processed_deliveries = np.empty(valid_requests, dtype=object)   # Create NumPy array for processed deliveries
    delivery_count = 0                                    # Initialize counter for processed deliveries
    continue_process = delivery_count < valid_requests    # Set condition to continue processing

    while continue_process:                             # Process deliveries while there are valid requests
        delivery = scheduler.processNextDelivery()      # Get the next delivery to process

        if delivery:                                          # If a delivery is returned, process it
            processed_deliveries[delivery_count] = delivery   # Store the delivery in the array
            customer_id = delivery.getCustomerID()            # Get the customer ID from the delivery

            try:                                                         # Try to update the customer's delivery status
                lookup.updateStatus(customer_id, "Delivered")  # Update status to "Delivered"
                print(f"Updated delivery status for customer {customer_id} to Delivered")
                print()
            except Exception as e:
                print(f"Failed to update status for customer {customer_id}: {e}")
            delivery_count += 1                                  # Increment the delivery counter
            continue_process = delivery_count < valid_requests   # Update condition to continue processing
        else:                         # If no delivery is returned
            continue_process = False  # Stop processing
    print(f"\nProcessed {delivery_count} deliveries")

    print("\n4) Generating end of day delivery report (saved to a csv file)")

    if delivery_count > 0:                                    # Check if there are deliveries to report
        sorted_deliveries = merge_sort(processed_deliveries)  # Sort deliveries using merge sort

        with open("DeliveryReport.csv", "w") as w: # Open a new CSV file to write the report
            w.write("Customer_id,name,address,destination_hub,travel_time,delivery_status\n")

            for delivery in sorted_deliveries:          # Iterate through sorted deliveries
                customer_id = delivery.getCustomerID()  # Get customer ID from delivery
                hub = delivery.getDestinationHub()      # Get destination hub from delivery
                travel_time = delivery.getTravelTime()  # Get travel time from delivery
                try:
                    customer = lookup.searchCustomer(customer_id)   # Search for customer in lookup table
                    name = customer.getName()                # Get customer's name
                    address = customer.getAddress()          # Get customer's address
                    status = customer.getDeliveryStatus()    # Get customer's delivery status
                    w.write(f"{customer_id},{name.replace(' ', '_')},{address.replace(' ', '_')},{hub},{travel_time},{status}\n")
                except Exception as e:
                    print(f"Failed to retrieve customer {customer_id} for report: {e}")
        print(f"Delivery report has been saved to DeliveryReport.csv")

        print("\nA sample of sorted deliveries by travel time:") # Announce display of sample deliveries
        display_count = 0      # Initialize counter for displayed deliveries
        max_display = 5        # Set maximum number of deliveries to display
        current_delivery = 0   # Initialize index for sorted deliveries

        while current_delivery < len(sorted_deliveries) and display_count < max_display:  # Iterate up to display limit
            delivery = sorted_deliveries[current_delivery]   # Get the current delivery
            customer_id = delivery.getCustomerID()   # Get customer ID from delivery
            hub = delivery.getDestinationHub()       # Get destination hub from delivery
            travel_time = delivery.getTravelTime()   # Get travel time from delivery
            try:
                customer = lookup.searchCustomer(customer_id) # Try to retrieve and display customer details, Search for customer
                print(f"Delivery {display_count+1}: customer {customer_id} ({customer.getName()}), hub {hub}, {travel_time} min")
            except: # Handle case where customer lookup fails
                print(f"Delivery {display_count+1}: Customer {customer_id}, Hub {hub}, {travel_time} min")
            display_count += 1      # Increment display counter
            current_delivery += 1   # Move to the next delivery
    else:
        print("No deliveries processed for reporting")   # If no deliveries were processed

if __name__ == "__main__":
    processDeliveries()