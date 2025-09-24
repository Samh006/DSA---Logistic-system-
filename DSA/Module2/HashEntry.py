"""
Customer Entry class for the hash table.

customer_id: Unique customer id (string)
name: customers name (string)
address: delivery address, may inc hub label (string)
priority level: Priority level (1-5 int)
delivery status: Delivery status (eg in transit (string))
"""
class hashError(Exception):
    pass

class CustomerEntry:
    # Constants for the state of a customer entry
    EMPTY_STATE = 0    # Slot is empty, never used
    USED_STATE = 1     # Slot contains a valid customer
    DELETED_STATE = 2  # Slot had a customer that was deleted

    def __init__(self, customer = None):
        if customer is None:
            self.customer = None
            self.state = CustomerEntry.EMPTY_STATE
        else:
            self.customer = customer
            self.state = CustomerEntry.USED_STATE