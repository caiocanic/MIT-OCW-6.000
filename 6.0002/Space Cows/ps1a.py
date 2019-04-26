# 6.0002 Problem Set 1a: Space Cows 

from ps1_partition import get_partitions
import time

FILE_NAME = "ps1_cow_data.txt"

def load_cows(filename):
    """
    Read the contents of the given file. Assumes the file contents
    contain data in the form of comma-separated cow name, weight pairs,
    and return a dictionary containing cow names as keys and
    corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows = {}
    with open(filename, "r") as file:
        for line in file:
             values = line.split(",")
             cows[values[0]] = int(values[1])
    return cows

def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that
    attempts to minimize the number of spaceship trips needed to
    transport all the cows. The returned allocation of cows may or may
    not be optimal. Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all
    the trips
    """
    # Convert from dic to list of tuples and sort descending by value
    remaining_cows = sorted([(v, k) for k, v in cows.items()],
                             key=lambda x: x[0], reverse=True)
    transported_cows = []
    while remaining_cows:
        trip_weight = 0
        trip_cows = []
        i = 0
        while trip_weight < limit and i < len(remaining_cows):
            if trip_weight + remaining_cows[i][0] <= limit:
                trip_cows.append(remaining_cows[i][1])
                trip_weight += remaining_cows[i][0]
                del remaining_cows[i]
            else:
                i += 1
        transported_cows.append(trip_cows)
    return transported_cows

def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship
    trips via brute force. Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all
    the trips
    """
    possible_allocations = sorted([x for x in get_partitions(cows.keys())],
                             key=lambda x: len(x))
    for allocation in possible_allocations:
        good_allocation = True
        for trip in allocation:
            trip_weight = 0
            for cow in trip:
                trip_weight += cows[cow]
            if trip_weight > limit:
                good_allocation = False
                break
        if good_allocation:
            return allocation

def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, runs
    greedy_cow_transport and brute_force_cow_transport functions. Print
    out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows(FILE_NAME)
    start = time.time()
    greedy_solution = greedy_cow_transport(cows)
    end = time.time()
    print("The greedy solution run in", end-start, "and solved with",
          len(greedy_solution), "trips.")
    start = time.time()
    brute_solution = brute_force_cow_transport(cows)
    end = time.time()
    print("The brute solution run in", end-start, "and solved with",
          len(brute_solution), "trips.")

if __name__ == "__main__":
    compare_cow_transport_algorithms()