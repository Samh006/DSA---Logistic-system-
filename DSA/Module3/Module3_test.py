from Module1.Graph import DSAGraph
from Module1.Linked_list import DSALinkedList
from Module2.LookUpCustomer import LookUpCustomer
from Module2.Customer import Customer
from Module3.Schedule import DeliveryScheduler
from Module3.DeliveryRes import DeliveryRes
import numpy as np
import os

"""Helper function to get absolute path for linux"""
def get_module_path(filename):
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(module_dir, filename)
    
"""parse DeliveryReq.csv"""
def parseRequests(filename):
    requests = DSALinkedList()
    csv_path = get_module_path(filename)

    try:
        with open(csv_path, 'r') as file:
            lines = file.readlines()

            for line in lines[1:]:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Tokenize using split
                fields = line.split(',')
                if len(fields) != 2:
                    print(f"Skipping invalid line: {line} (expected 2 fields)")
                    continue

                try:
                    customer_id = int(fields[0])
                    destination_hub = fields[1]
                    if not destination_hub:
                        raise ValueError("Destination hub cannot be empty")
                    request = DeliveryRes(customer_id, destination_hub, None)
                    requests.insertLast(request)
                except ValueError as e:
                    print(f"Skipping invalid line: {line} (error: {e})")
    except FileNotFoundError:
        print(f"Error: {filename} not found")
    return requests

"""parse CustomerData.csv"""
def parseCustomers(filename):
    customers = DSALinkedList()
    csv_path = get_module_path(filename)

    try:
        with open(csv_path, 'r') as file:
            lines = file.readlines()
            # Skip header
            for line in lines[1:]:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Tokenize using split
                fields = line.split(',')
                if len(fields) != 5:
                    print(f"Skipping invalid line: {line} (expected 5 fields)")
                    continue

                try:
                    customer_id = int(fields[0])
                    name = fields[1].replace('_', ' ')
                    address = fields[2].replace('_', ' ')
                    priority_level = int(fields[3])
                    delivery_status = fields[4].replace('_', ' ')
                    customer = Customer(customer_id, name, address, priority_level, delivery_status)
                    customers.insertLast(customer)
                except ValueError as e:
                    print(f"Skipping invalid line: {line} (error: {e})")
    except FileNotFoundError:
        print(f"Error: {filename} not found")
    return customers

"""Set up graph and customer lookup."""
def setupData():

    # inner edge class
    class Edge:
        def __init__(self, source, destination, weight):
            self.source = source
            self.destination = destination
            self.weight = weight

    # Hardcode graph
    graph = DSAGraph()
    node_chars = "ABCDEFGH"
    edges = DSALinkedList()
    edges.insertLast(Edge('A', 'B', 5))
    edges.insertLast(Edge('A', 'C', 3))
    edges.insertLast(Edge('B', 'D', 4))
    edges.insertLast(Edge('B', 'E', 6))
    edges.insertLast(Edge('C', 'F', 2))
    edges.insertLast(Edge('C', 'G', 7))
    edges.insertLast(Edge('D', 'E', 3))
    edges.insertLast(Edge('E', 'F', 4))
    edges.insertLast(Edge('F', 'G', 5))
    edges.insertLast(Edge('D', 'F', 2))
    edges.insertLast(Edge('B', 'G', 8))

    for node in node_chars:
        graph.addVertex(node)
    current = edges.head
    while current:
        edge = current.getValue()
        graph.addEdge(edge.source, edge.destination, edge.weight)
        current = current.getNext()

    # Load customers
    lookup = LookUpCustomer()
    customers = parseCustomers("CustomerData.csv")
    current = customers.head
    while current:
        customer = current.getValue()
        lookup.insertCustomer(customer)
        current = current.getNext()
    return graph, lookup


def testAddingRequests():
    """Test adding delivery requests (Modules 1, 2, 3 integration)."""
    print("\n" + "=" * 60)
    print("TEST 1: ADDING DELIVERY REQUESTS - VALIDATION TEST")
    print("=" * 60)
    print("Purpose: Verify that delivery requests are properly validated and added")
    print("Expected: 4 valid requests should be successfully added")
    print("-" * 60)

    graph, lookup = setupData()
    scheduler = DeliveryScheduler(graph, lookup)

    requests = parseRequests("DeliveryReq.csv")
    valid_count = 0
    current = requests.head
    while current:
        request = current.getValue()
        customer_id = request.getCustomerID()
        destination_hub = request.getDestinationHub()
        try:
            scheduler.insertDeliverRequest(customer_id, destination_hub)
            valid_count += 1
            print(f"[SUCCESS] Added valid request - Customer ID: {customer_id}, Destination: {destination_hub}\n")
        except Exception as e:
            print(f"[FILTERED] Rejected invalid request - Customer ID: {customer_id}, Destination: {destination_hub}")
            print(f"           Reason: {e}\n")
        current = current.getNext()

    print("\n" + "-" * 60)
    if valid_count >= 4:  # Expect 4 valid requests (53,B; 106,C; 1001,B; 106,F)
        print(f"RESULT: PASS - Correct number of valid requests processed ({valid_count}/4)")
    else:
        print(f"RESULT: FAIL - Expected at least 4 valid requests, got {valid_count}")


def testProcessingDeliveries():
    """Test processing deliveries in priority order."""
    print("\n" + "=" * 60)
    print("TEST 2: PROCESSING DELIVERIES - PRIORITY ORDER TEST")
    print("=" * 60)
    print("Purpose: Verify deliveries are processed in correct priority order")
    print("Expected Order: (106,C), (1001,B), (106,F), (53,B)")
    print("-" * 60)

    graph, lookup = setupData()
    scheduler = DeliveryScheduler(graph, lookup)

    # defining expected order
    dtype = [('customer_id', int), ('hub', 'U1')]
    expected_order = np.array([(106, 'C'), (1001, 'B'), (106, 'F'), (53, 'B')], dtype=dtype)

    requests = parseRequests("DeliveryReq.csv")
    current = requests.head
    while current:
        request = current.getValue()
        try:
            scheduler.insertDeliverRequest(request.getCustomerID(), request.getDestinationHub())
            print()
        except Exception as e:
            print(f"Skipped invalid request: {e}")
        current = current.getNext()

    processed_deliveries = np.empty(4, dtype=object)
    processed_count = 0
    done = False

    print("Processing deliveries in order:")
    while processed_count < 4 and not done:
        result = scheduler.processNextDelivery()
        if result:
            customer_id = result.getCustomerID()
            hub = result.getDestinationHub()
            processed_deliveries[processed_count] = result
            if processed_count < 4:
                expected_id = expected_order[processed_count]['customer_id']
                expected_hub = expected_order[processed_count]['hub']
                if customer_id == expected_id and hub == expected_hub:
                    print(f"[CORRECT] Delivery {processed_count + 1}: Customer {customer_id} to {hub}\n")
                else:
                    print(
                        f"[INCORRECT] Expected Customer {expected_id} to {expected_hub}, got {customer_id} to {hub}\n")
            processed_count += 1
        else:
            print("[COMPLETE] No more deliveries in queue")
            done = True

    print("\n" + "-" * 60)
    if processed_count == 4:
        print("RESULT: PASS - All 4 expected deliveries were processed")
    else:
        print(f"RESULT: FAIL - Expected 4 deliveries, processed {processed_count}")
    return processed_deliveries


if __name__ == "__main__":
    testAddingRequests()
    processed_deliveries = testProcessingDeliveries()
