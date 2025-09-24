class DeliveryRes:
    def __init__(self, customer_id, destination_hub, travel_time):
        self.customer_id = customer_id
        self.destination_hub = destination_hub
        self.travel_time = travel_time

    def getCustomerID(self):
        return self.customer_id

    def getDestinationHub(self):
        return self.destination_hub

    def getTravelTime(self):
        return self.travel_time

    def __str__(self):
        return f"Customer: {self.customer_id}, hub: {self.destination_hub}, travel time = {self.travel_time}"
