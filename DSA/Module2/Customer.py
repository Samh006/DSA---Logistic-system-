from Module2.HashEntry import hashError

"""
Customer class for storing customer data
Inc customer ID, name, address, priority level and delivery status
"""
class Customer:
    def __init__(self, customer_id, name, address, priority_level, delivery_status):
        if not isinstance(priority_level, int) or priority_level < 1 or priority_level > 5:
            raise hashError("Priority must be an int between 1 and 5")
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.priority_level = priority_level
        self.delivery_status = delivery_status

    def getID(self):
        return self.customer_id

    def getName(self):
        return self.name

    def getAddress(self):
        return self.address

    def getPriorityLevel(self):
        return self.priority_level

    def getDeliveryStatus(self):
        return self.delivery_status

    def setDeliveryStatus(self, new_status):
        self.delivery_status = new_status



