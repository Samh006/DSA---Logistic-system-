from Module1.Graph import DSAGraph, GraphErrorHandle
from Module2.LookUpCustomer import LookUpCustomer
from Module3.Heap import DSAHeap
from Module3.DeliveryRes import DeliveryRes

class DeliveryScheduler:
    def __init__(self, graph, lookup):
        if not isinstance(graph, DSAGraph):
            raise ValueError("Graph must be a DSAGraph instance")
        if not isinstance(lookup, LookUpCustomer):
            raise ValueError("Lookup must be a lookupcustomer instance")

        self.heap = DSAHeap(capacity=100)
        self.graph = graph
        self.lookup = lookup

    """Adds a delivery request to the scheduler"""
    def insertDeliverRequest(self, customer_id, destination_hub):
        #  fetch customer data using module 2
        try:
            customer = self.lookup.searchCustomer(customer_id)
        except Exception as e:
            raise ValueError(f"Customers ID {customer_id} not found: {e}")

        delivery_status = customer.getDeliveryStatus()
        is_active = (delivery_status == 'In_Transit' or delivery_status == 'In Transit' or delivery_status == 'Delayed'
                     or delivery_status == 'Delayed_')
        if not is_active:
            print(f"Skipping {customer_id}: not an active delivery ({delivery_status})")
            return False

        # Get travel time from dijksra in module 1
        source_hub = 'A'
        try:
            dijkstra_results = self.graph.dijkstra(source_hub)
            travel_time = None
            current = dijkstra_results.head
            found = False

            while current and not found:
                result = current.getValue()
                if result.getLabel() == destination_hub:
                    travel_time = result.getDistance()
                    found = True
                else:
                    current = current.getNext()
            if travel_time is None or travel_time == float('inf'):
                raise GraphErrorHandle(f"No path to hub {destination_hub}")
            if travel_time == 0:
                raise ValueError("Travel time cannot be zero")
        except GraphErrorHandle as e:
            raise GraphErrorHandle(f"Error computing travel time: {e}")

        # calculate priority
        priority_level = customer.getPriorityLevel()
        priority = (6 - priority_level) + (1000 / travel_time)

        # insert into heap with travel time
        self.heap.insert(priority, customer_id, destination_hub, travel_time)
        return True

    """Process deliveries with the highest priority"""
    def processNextDelivery(self):
        try:
            entry = self.heap.extract_priority()
            customer_id = entry.getCustomerID()
            destination_hub = entry.getDestinationHub()
            priority = entry.getPriority()
            travel_time = entry.getTravelTime()

            print(f"Processing delivery: customer = {customer_id}, hub = {destination_hub}, priority = {priority:.2f}, travel time = {travel_time}")
            return DeliveryRes(customer_id, destination_hub, travel_time)
        except Exception as e:
            print(f"Error processing delivery: {e}")
            return None