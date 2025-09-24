"""
Test file for module 2: Customer Hash Table
Tests core functionality, collision handling and resizing.
uses customerdata.csv
"""
import os
from Module2.Customer import Customer
from Module2.LookUpCustomer import LookUpCustomer
from Module2.HashEntry import hashError
from Module2.HashTable import CustomerHashTable

"""Parse CustomerData.csv, return num of customers loaded"""
def parseCSV(filename):
    module_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(module_dir, filename)
    
    lookup = LookUpCustomer()
    loadedCustomers = 0

    try:
        with open(csv_path, 'r') as file:
            lines = file.readlines()

            # Skip header
            for line in lines[1:]:
                # Tokenize the line using split
                fields = line.strip().split(',')

                # Ensure the line has exactly 5 fields
                if len(fields) != 5:
                    print(f"Skipping invalid line: {line.strip()} (incorrect number of fields)")
                    continue

                # Extract fields
                try:
                    customerID = int(fields[0])  # Convert to int
                    name = fields[1].replace('_', ' ')
                    address = fields[2].replace('_', ' ')
                    priorityLevel = int(fields[3])  # Convert to int
                    deliveryStatus = fields[4].replace('_', ' ')

                    # Create and insert customer
                    customer = Customer(customerID, name, address, priorityLevel, deliveryStatus)
                    lookup.insertCustomer(customer)
                    loadedCustomers += 1
                except ValueError as e:
                    print(f"Skipping invalid line: {line.strip()} (value error: {e})")
                except hashError as e:
                    print(f"Skipping line due to invalid priority: {line.strip()} ({e})")
            return loadedCustomers, lookup
    except FileNotFoundError:
        print(f"Error: {filename} was not found")
        return 0, lookup
    except Exception as e:
        print(f"Error loading csv: {e}")
        return 0, lookup

"""Test insert, search, delete and updates"""
def testFunctionality(lookup):
    print("\n--- Testing the main functionality ---")

    # insertion done in parseCsv, verify the count
    stats = lookup.ht.get_statistics()
    print(f"\n1) Inserted {stats.count} customers from CSV")
    print(f"Table stats: size = {stats.size}, count = {stats.count}, load factor = {stats.load_factor:.3f}")

    # test search
    print("\n2) Testing search:")
    customer_id = 53
    try:
        foundCustomer = lookup.searchCustomer(customer_id)
        print(f"Found customer {customer_id:} {foundCustomer.getName()} - {foundCustomer.getDeliveryStatus()}")
    except hashError as e:
        print(f"Customer {customer_id} not found, (expected: {e}) ")

    customer_id = 1001
    try:
        foundCustomer = lookup.searchCustomer(customer_id)
        print(f" Found customer {customer_id}: {foundCustomer.getName()} - {foundCustomer.getDeliveryStatus()}")
    except hashError as e:
        print(f"Customer {customer_id} not found (expected: {e})")

    customer_id = 1002
    try:
        foundCustomer = lookup.searchCustomer(customer_id)
        print(f"Found customer {customer_id}: {foundCustomer.getName()} - {foundCustomer.getDeliveryStatus()}")
    except hashError as e:
        print(f"Customer {customer_id} not found (expected: {e})")

    customer_id = 999
    try:
        foundCustomer = lookup.searchCustomer(customer_id)
        print(f"Found non-existent customer {customer_id}!")
    except hashError as e:
        print(f"Customer {customer_id} not found (expected: {e})")

    # Test update delivery status
    print("\n3) Testing delivery status update")

    customer_id = 53
    new_status = "Delivered"
    result = lookup.updateStatus(customer_id, new_status)
    print(f"Update customer {customer_id} to '{new_status}': {'Success' if result else 'Failed'}")
    if result:
        try:
            updated_customer = lookup.searchCustomer(customer_id)
            print(f"Verified status: {updated_customer.getDeliveryStatus()}")
        except hashError as e:
            print(f" Verification failed: {e}")

    customer_id = 1001
    new_status = "Out for delivered"
    result = lookup.updateStatus(customer_id, new_status)
    print(f"Update customer {customer_id} to '{new_status}': {'Success' if result else 'Failed'}")
    if result:
        try:
            updated_customer = lookup.searchCustomer(customer_id)
            print(f"Verified status: {updated_customer.getDeliveryStatus()}")
        except hashError as e:
            print(f" Verification failed: {e}")

    customer_id = 999
    new_status = "Processing"
    result = lookup.updateStatus(customer_id, new_status)
    print(f"Update customer {customer_id} to '{new_status}': {'Success' if result else 'Failed'}")
    if result:
        try:
            updated_customer = lookup.searchCustomer(customer_id)
            print(f"Verified status: {updated_customer.getDeliveryStatus()}")
        except hashError as e:
            print(f" Verification failed: {e}")

    # test delete
    print("\n4) Testing the delete function")
    customer_id = 1002
    result = lookup.deleteCustomer(customer_id)
    print(f"Delete customer {customer_id}: {'Success' if result else 'Failed'}")
    try:
        lookup.searchCustomer(customer_id)
        print(f"Error, customer {customer_id} still found after deleting")
    except hashError as e:
        print(f"Confirmed, customer {customer_id} has been deleted")

    customer_id = 999
    result = lookup.deleteCustomer(customer_id)
    print(f"Delete customer {customer_id}: {'Success' if result else 'Failed'}")
    try:
        lookup.searchCustomer(customer_id)
        print(f"Error, customer {customer_id} still found after deleting")
    except hashError as e:
        print(f"Confirmed, customer {customer_id} has been deleted")

"""Test linear probing with ID's 53 and 106"""
def testCollisionHandling(lookup):
    print("\n--- Testing collision handling ---")
    print("\nVerifying customers with colliding hash values (53, 106):")

    customer_id = 53
    try:
        found = lookup.searchCustomer(customer_id)
        hash_value = customer_id % 53
        print(f"Retrieved ID {customer_id} (hash: {hash_value}): {found.getName()} - {found.getDeliveryStatus()}")
    except hashError as e:
        print(f"Error, failed to retrieve ID {customer_id}: {e}")

    customer_id = 106
    try:
        found = lookup.searchCustomer(customer_id)
        hash_value = customer_id % 53
        print(f"Retrieved ID {customer_id} (hash: {hash_value}): {found.getName()} - {found.getDeliveryStatus()}")
    except hashError as e:
        print(f"Error, failed to retrieve ID {customer_id}: {e}")

"""Test resizing based on the load factor"""
def testLoadFactor(lookup):
    print("\n--- Testing load factor and resizing ---")
    stats = lookup.ht.get_statistics()

    print("\nCurrent table stats:")
    print(f"Size: {stats.size}, count: {stats.count}, load factor: {stats.load_factor:.3f}")

    # Check if table has already been upsized from minimum size
    if stats.size > CustomerHashTable.MIN_SIZE:
        print(f"Table has already been upsized from minimum size {CustomerHashTable.MIN_SIZE} to {stats.size}")
        print("This occurred during CSV loading when load factor exceeded 0.7")

    # Test additional upsizing if we're close to the threshold
    if stats.load_factor > 0.5:  # Test when we're getting close to 0.7
        print(f"\nTesting additional upsizing (current load factor: {stats.load_factor:.3f}):")
        try:
            current_size = stats.size

            # Add customers until we trigger a resize
            i = 10000
            while i < 10010:
                customer = Customer(i, f"Extra_{i}", f"{i}_Extra_St", 1, "In_Transit")
                lookup.insertCustomer(customer)

                new_stats = lookup.ht.get_statistics()
                print(f"Added ID {i}: size = {new_stats.size}, count = {new_stats.count}, load factor = {new_stats.load_factor:.3f}")

                if new_stats.size > current_size:
                    print(f"Table successfully upsized from {current_size} to {new_stats.size}")
                    return  # Exit early after successful resize

                if new_stats.load_factor > 0.75:  # Safety check
                    print("Reached high load factor without resize - stopping test")
                    return
                i += 1

        except Exception as e:
            print(f"Insertion error: {e}")
    else:
        print(f"Load factor ({stats.load_factor:.3f}) is too low to test upsizing efficiently")

    # Test downsizing
    print(f"\nTesting downsizing (need load factor < {CustomerHashTable.MIN_LOAD_FACTOR}):")
    stats = lookup.ht.get_statistics()
    initial_size = stats.size

    # Calculate how many customers we need to delete to trigger downsizing
    target_count_float = stats.size * CustomerHashTable.MIN_LOAD_FACTOR
    target_count = int(target_count_float) - 1
    customers_to_delete = stats.count - target_count
    if customers_to_delete < 0:
        customers_to_delete = 0

    print(f"Current: {stats.count} customers, need to delete ~{customers_to_delete} to trigger downsize")

    if customers_to_delete > 0 and stats.size > CustomerHashTable.MIN_SIZE:
        deleted = 0
        # Start from higher IDs to avoid deleting test-critical customers
        customer_id = 1020
        while customer_id < 1060 and deleted < customers_to_delete:
            # Check if customer exists by trying to search for it
            customer_exists = False
            try:
                lookup.searchCustomer(customer_id)
                customer_exists = True
            except hashError:
                customer_exists = False

            # If customer exists, try to delete it
            if customer_exists:
                delete_result = lookup.deleteCustomer(customer_id)
                if delete_result:
                    deleted += 1

                    # Check progress every 5 deletions or when we reach target
                    if deleted % 5 == 0 or deleted == customers_to_delete:
                        new_stats = lookup.ht.get_statistics()
                        print(f"Deleted {deleted} customers: size = {new_stats.size}, count = {new_stats.count}, load factor = {new_stats.load_factor:.3f}")

                        if new_stats.size < initial_size:
                            print(f"Table successfully downsized from {initial_size} to {new_stats.size}")
                            return
            customer_id += 1

        # If we didn't trigger a downsize, check why
        final_stats = lookup.ht.get_statistics()
        if final_stats.size == initial_size:
            if final_stats.size <= CustomerHashTable.MIN_SIZE:
                print(f"Table remained at minimum size {CustomerHashTable.MIN_SIZE} (no downsizing below minimum)")
            else:
                print(f"Load factor {final_stats.load_factor:.3f} still above minimum threshold {CustomerHashTable.MIN_LOAD_FACTOR}")
    else:
        print(f"Cannot test downsizing: table at minimum size ({CustomerHashTable.MIN_SIZE}) or insufficient customers")

"""Test error conditions"""
def testErrorHandling(lookup):
    print("\n--- Testing error handling ---")

    # test invalid priority
    priority = 0
    try:
        customer = Customer(9999, "test customer", "test address", priority, "test status")
        lookup.insertCustomer(customer)
        print(f"Error, priority {priority} should have been rejected")
    except hashError as e:
        print(f" correctly rejected priority {priority}: {e}")

    priority = 6
    try:
        customer = Customer(9999, "test customer", "test address", priority, "test status")
        lookup.insertCustomer(customer)
        print(f"Error, priority {priority} should have been rejected")
    except hashError as e:
        print(f" correctly rejected priority {priority}: {e}")

    priority = -1
    try:
        customer = Customer(9999, "test customer", "test address", priority, "test status")
        lookup.insertCustomer(customer)
        print(f"Error, priority {priority} should have been rejected")
    except hashError as e:
        print(f" correctly rejected priority {priority}: {e}")

    # Test non existent customer
    print("\n2) Testing on non existent customer")

    customer_id = 999
    try:
        customer = lookup.searchCustomer(customer_id)
        print(f"Error, found a non existent customer {customer_id}")
    except hashError as e:
        print(f"Correctly handled missing customer")
    result = lookup.updateStatus(customer_id, "test status")
    print(f"Update non existent ID {customer_id}: {'Success' if result else 'Failed (expected)'}")

    customer_id = 1234
    try:
        customer = lookup.searchCustomer(customer_id)
        print(f"Error, found a non existent customer {customer_id}")
    except hashError as e:
        print(f"Correctly handled missing customer")
    result = lookup.updateStatus(customer_id, "test status")
    print(f"Update non existent ID {customer_id}: {'Success' if result else 'Failed (expected)'}")


"""Verify handling of 50+ customers"""
def test50Customers(lookup, loadedCustomers):
    print("\n--- Testing with 50+ customers ---")
    stats = lookup.ht.get_statistics()
    print(f"\nLoaded {loadedCustomers} customers from CSV")
    if loadedCustomers < 50:
        print(f"Warning, expected 50+ customers, loaded {loadedCustomers}")
    print(f"Table stats size = {stats.size}, Count={stats.count}, Load Factor={stats.load_factor:.3f}")

    print("\nVerifying retrieval of sample customers:")
    customer_id = 53
    try:
        customer = lookup.searchCustomer(customer_id)
        print(f"Retrieved ID {customer_id}: {customer.getName()} - {customer.getDeliveryStatus()}")
    except hashError as e:
        print(f"Failed to retrieve ID {customer_id}: {e}")

    customer_id = 1001
    try:
        customer = lookup.searchCustomer(customer_id)
        print(f"Retrieved ID {customer_id}: {customer.getName()} - {customer.getDeliveryStatus()}")
    except hashError as e:
        print(f"Failed to retrieve ID {customer_id}: {e}")

def main():
    print("Module 2: customer hash table test cases")

    try:
        loadedCustomers, lookup = parseCSV('CustomerData.csv')
        if loadedCustomers == 0:
            print("No customers have been loading")
            return

        testFunctionality(lookup)
        testCollisionHandling(lookup)
        testLoadFactor(lookup)
        testErrorHandling(lookup)
        test50Customers(lookup, loadedCustomers)

        print("All tests complete")
    except Exception as e:
        print(f"\nTest case failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
