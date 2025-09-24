from Module2.HashTable import CustomerHashTable

class LookUpCustomer:
    def __init__(self):
        self.ht = CustomerHashTable()

    def insertCustomer(self, customer):
        return self.ht.insert(customer)

    def searchCustomer(self, customer_id):
        return self.ht.search(customer_id)

    def deleteCustomer(self, customer_id):
        return self.ht.delete(customer_id)

    def updateStatus(self, customer_id, new_status):
        return self.ht.update_delivery_status(customer_id, new_status)