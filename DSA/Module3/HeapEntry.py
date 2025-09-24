class DSAHeapEntry:
    def __init__(self, priority, customer_id, destination_hub, travel_time):
        self.priority = priority
        self.customer_id = customer_id
        self.destination_hub = destination_hub
        self.travel_time = travel_time

    def getPriority(self):
        return self.priority

    def setPriority(self, priority):
        self.priority = priority

    def getCustomerID(self):
        return self.customer_id

    def getDestinationHub(self):
        return self.destination_hub

    def getTravelTime(self):
        return self.travel_time

    def __str__(self):
        return f"(Priority: {self.priority:.2f}, Customer: {self.customer_id}, Hub: {self.destination_hub}, time: {self.travel_time})"