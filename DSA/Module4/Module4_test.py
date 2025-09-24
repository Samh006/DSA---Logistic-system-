import numpy as np
import sys
import time
import random
import matplotlib.pyplot as plt
from Module3.DeliveryRes import DeliveryRes
from Module4.SortRecords import merge_sort, quick_sort_median3

REPEATS = 3  # Number of times to run sorts
NEARLY_PERCENT = 0.10  # Percent of items to move in nearly sorted
RANDOM_SWAPS = 100  # Number of swaps for random state


def generate_dataset(n, processed_deliveries, arrayType, hubs):
    """Generate a dataset of DeliveryRes objects with varied travel times."""
    A = np.empty(n, dtype=object)

    # Seed with Module 3 data if available
    seed_count = min(n, len(processed_deliveries)) if processed_deliveries is not None else 0
    for i in range(seed_count):
        A[i] = processed_deliveries[i]

    # Generate synthetic data with more varied travel times
    for i in range(seed_count, n):
        customer_id = 1000 + i
        hub = hubs[random.randint(0, len(hubs) - 1)]
        # Generate more realistic travel times between 1.0 and 15.0 minutes
        travel_time = round(random.uniform(1.0, 15.0), 1)
        A[i] = DeliveryRes(customer_id, hub, travel_time)

    if arrayType == 'r':  # Random - already random from generation
        # Additional shuffling to ensure randomness
        for i in range(RANDOM_SWAPS):
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            A[x], A[y] = A[y], A[x]
    elif arrayType == 'n':  # Nearly sorted
        # Sort first
        A = merge_sort(A.copy())
        # Perturb a small percentage of elements
        num_swaps = max(1, int(n * NEARLY_PERCENT / 2))
        for i in range(num_swaps):
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            A[x], A[y] = A[y], A[x]
    elif arrayType == 'd':  # Reversed (worst case for quick sort)
        # Sort first, then reverse
        A = merge_sort(A.copy())
        for i in range(n // 2):
            A[i], A[n - i - 1] = A[n - i - 1], A[i]

    return A


def print_sorted(A, max_items=5):
    """Print first few sorted DeliveryRes objects and a sample from across the range."""
    print("Sorted Deliveries (Customer, Hub, Travel Time):")

    # Print first few
    print("First few items:")
    for i in range(min(max_items, len(A))):
        if A[i]:
            delivery = A[i]
            print(
                f"Customer {delivery.getCustomerID()}: Hub {delivery.getDestinationHub()}: {delivery.getTravelTime()} min")

    # Print some from the middle
    if len(A) > 10:
        print("\nSample from middle:")
        mid = len(A) // 2
        for i in range(mid, min(mid + max_items, len(A))):
            if A[i]:
                delivery = A[i]
                print(
                    f"Customer {delivery.getCustomerID()}: Hub {delivery.getDestinationHub()}: {delivery.getTravelTime()} min")

    # Print last few
    if len(A) > 10:
        print("\nLast few items:")
        for i in range(max(0, len(A) - max_items), len(A)):
            if A[i]:
                delivery = A[i]
                print(
                    f"Customer {delivery.getCustomerID()}: Hub {delivery.getDestinationHub()}: {delivery.getTravelTime()} min")


def doSort(n, sortType, arrayType, processed_deliveries, hubs):
    """Generate and sort a dataset, return execution time."""
    A = generate_dataset(n, processed_deliveries, arrayType, hubs)

    # Create a copy for sorting to avoid modifying original
    A_copy = A.copy()

    startTime = time.perf_counter()
    if sortType == "m":
        sorted_A = merge_sort(A_copy)
    elif sortType == "q":
        sorted_A = quick_sort_median3(A_copy)
    else:
        raise ValueError("Unsupported sort type")
    endTime = time.perf_counter()

    # Verify sorting correctness
    for i in range(len(sorted_A) - 1):
        if sorted_A[i].getTravelTime() > sorted_A[i + 1].getTravelTime():
            raise ValueError(f"Array not properly sorted at index {i}")

    return sorted_A, endTime - startTime


def test_sorting(processed_deliveries=None):
    """Test sorting algorithms on DeliveryRes datasets."""
    # Test parameters
    sizes = np.array([100, 500, 1000])
    arrayTypes = np.array(['r', 'n', 'd'])  # random, nearly sorted, reversed
    sortTypes = np.array(['m', 'q'])  # merge, quick
    hubs = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G'])

    # Storage for timing results using NumPy arrays
    # Shape: (3 arrayTypes, 3 sizes) for each sort type
    merge_times = np.zeros((3, 3), dtype=float)
    quick_times = np.zeros((3, 3), dtype=float)

    print("\n" + "=" * 70)
    print("MODULE 4: SORTING DELIVERY RECORDS PERFORMANCE TESTING")
    print("=" * 70)
    print("Testing Merge Sort vs Quick Sort (median-of-three pivot)")
    print("Dataset sizes: 100, 500, 1000 parcels")
    print("Conditions: Random, Nearly Sorted, Reversed")

    for size_idx in range(len(sizes)):
        n = sizes[size_idx]
        print(f"\n{'=' * 50}")
        print(f"DATASET SIZE: {n} parcels")
        print(f"{'=' * 50}")

        for array_idx in range(len(arrayTypes)):
            arrayType = arrayTypes[array_idx]
            condition_names = np.array(['Random Order', 'Nearly Sorted', 'Reversed Order (worst case)'])
            condition = condition_names[array_idx]
            print(f"\nCondition: {condition}")
            print("-" * 40)

            merge_total = 0
            quick_total = 0
            sorted_result = None

            # Run multiple times for accurate timing
            for run in range(REPEATS):
                # Merge Sort
                result_m, merge_time = doSort(n, 'm', arrayType, processed_deliveries, hubs)
                merge_total += merge_time

                # Quick Sort
                result_q, quick_time = doSort(n, 'q', arrayType, processed_deliveries, hubs)
                quick_total += quick_time

                # Keep one result for display
                if run == 0:
                    sorted_result = result_m

            # Calculate averages
            merge_avg = merge_total / REPEATS
            quick_avg = quick_total / REPEATS

            # Store results for plotting
            merge_times[array_idx, size_idx] = merge_avg
            quick_times[array_idx, size_idx] = quick_avg

            # Display results
            print(f"Merge Sort Average Time: {merge_avg:.6f} seconds")
            print(f"Quick Sort Average Time: {quick_avg:.6f} seconds")


            # Show sample of sorted data
            if sorted_result is not None:
                print_sorted(sorted_result)

    # Generate performance graphs
    create_performance_graphs(sizes, merge_times, quick_times, arrayTypes)

    # Performance analysis and recommendations
    print_performance_analysis(merge_times, quick_times, sizes, arrayTypes)


def create_performance_graphs(sizes, merge_times, quick_times, arrayTypes):
    """Create and save performance comparison graphs."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    condition_labels = np.array(['Random Order', 'Nearly Sorted', 'Reversed Order'])
    colors = ['#2E86AB', '#A23B72']  # merge, quick

    for idx in range(len(arrayTypes)):
        ax = axes[idx]
        ax.plot(sizes, merge_times[idx],
                label="Merge Sort", marker='o', linewidth=2,
                markersize=6, color=colors[0])
        ax.plot(sizes, quick_times[idx],
                label="Quick Sort", marker='s', linewidth=2,
                markersize=6, color=colors[1])

        ax.set_title(f"Performance: {condition_labels[idx]}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Dataset Size (parcels)", fontsize=10)
        ax.set_ylabel("Execution Time (seconds)", fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_yscale('linear')  # Log scale for better visualization

    plt.suptitle("Sorting Algorithm Performance Comparison", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('sorting_performance_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\nPerformance graphs saved as 'sorting_performance_comparison.png'")


def print_performance_analysis(merge_times, quick_times, sizes, arrayTypes):
    """Print detailed performance analysis and recommendations."""
    print("\n" + "=" * 70)
    print("PERFORMANCE ANALYSIS & ALGORITHM RECOMMENDATIONS")
    print("=" * 70)

    print("\nAlgorithm Characteristics:")
    print("• Merge Sort:")
    print("  - Time Complexity: O(n log n) guaranteed (best, average, worst case)")
    print("  - Space Complexity: O(n)")
    print("  - Stable: Yes (maintains relative order of equal elements)")
    print("  - Performance: Consistent across all input conditions")

    print("\n• Quick Sort (median-of-three):")
    print("  - Time Complexity: O(n log n) average, O(n²) worst case")
    print("  - Space Complexity: O(log n)")
    print("  - Stable: No")
    print("  - Performance: Varies significantly with input condition")

if __name__ == "__main__":
    # Sample processed deliveries for testing
    sample_deliveries = np.array([
        DeliveryRes(106, 'C', 3.2),
        DeliveryRes(1001, 'B', 8.5),
        DeliveryRes(106, 'F', 5.7),
        DeliveryRes(53, 'B', 12.1),
        DeliveryRes(205, 'A', 2.8),
        DeliveryRes(89, 'G', 9.3)
    ])

    # Set random seed for reproducible results during testing
    random.seed(42)
    np.random.seed(42)

    # Run the sorting performance tests
    test_sorting(sample_deliveries)