import csv
import sys
from collections import deque  

# Process class to represent each process
class Process:
    def __init__(self, pid, arrival, burst, priority):
        # Unique identifier for the process (e.g., P1, P2...)
        self.pid = pid
        # The time when this process arrives in the system
        self.arrival = arrival
        # The total time this process needs to execute (its "burst time")
        self.burst = burst
        # How much burst time is still left (we'll decrease this as the process runs)
        self.remaining = burst
        # Priority value: lower numbers mean higher priority
        self.priority = priority
        # When the process first starts executing (None by default)
        self.start = None
        # When the process finishes execution
        self.completion = None


# Function to read from the CSV file I made
def read_processes(file_path):
    # Empty list to hold all the processes
    processes = []


    with open(file_path) as file:
        # Read the CSV rows as dictionaries
        reader = csv.DictReader(file)  
        for row in reader:

            # Convert each row into a Process object as we defined above and add to the processes list
            p = Process(
                # Convert the string values from the CSV to integers and put them where they belong in the table
                int(row['pid']),
                int(row['arrive']),
                int(row['burst']),
                int(row['priority'])
            )

            # append the process to our list of processes
            processes.append(p)

    # return the list of processes
    return processes

# Priority + Round Robin Scheduler
def priority_round_robin(processes, quantum):
    # Initialize a clock, a counter for the context switches, a terminated process list, and a ready queue 
    time = 0
    ctx_switches = 0
    complete = []
    queue = [] 

    # First, sort all incoming processes by arrival time as a priority measure
    processes.sort(key=lambda p: p.arrival)

    # The simulation runs while we still have new or unfinished processes
    while processes or queue:
        # Check for processes that have arrived and move them into the queue
        while processes and processes[0].arrival <= time:
            queue.append(processes.pop(0))

        # If no process is available, simulate idle time
        if not queue:
            time += 1
            continue

        # Sort queue by priority and arrival (so ties go to earlier arrivals)
        queue.sort(key=lambda p: (p.priority, p.arrival))

        # Pick the first process from the queue
        current = queue.pop(0)

        # If this is the first time the process is running, note the start time, so we can calculate priority metrics later
        if current.start is None:
            current.start = time

        # Process runs for either the full time quantum or whatever time it has left, we just simulate it by subtracting the time quantum
        run_time = min(quantum, current.remaining)
        current.remaining -= run_time
        # Advance the clock forward by however much the CPU burst was
        time += run_time 
        # Count this as a context switch
        ctx_switches += 1

        # Add new processes (like a real CPU would do)
        while processes and processes[0].arrival <= time:
            queue.append(processes.pop(0))

        # If the current process is not finished yet, put it back in the queue, perfectly simulating Round Robin
        if current.remaining > 0:
            queue.append(current)
        else:
            # Mark completion time and store it in the finished list
            current.completion = time
            complete.append(current)

    return complete, ctx_switches, time


# Function to calculate metrics, the metrics come from the priority + round robin function above
def calculate_metrics(processes, ctx_switches, total_time, ctx_time=0.5):
    # Initialize variables to hold total waiting and turnaround times
    n = len(processes)
    total_wait = 0
    total_turn = 0

    for p in processes:
        # Turnaround Time = Completion Time - Arrival Time
        tat = p.completion - p.arrival
        # Waiting Time = Turnaround Time - Burst Time
        wt = tat - p.burst
        total_wait += wt
        total_turn += tat

    # Return a dictionary of rounded metrics
    return {
        "Avg Waiting Time": round(total_wait / n, 2),
        "Avg Turnaround Time": round(total_turn / n, 2),
        "CPU Utilization": round(1 - (ctx_switches * ctx_time / total_time), 2),
        "Throughput": round(n / total_time, 2),
        "Context Switches": ctx_switches
    }

# Main code block that calls all the function above
if __name__ == "__main__":
    # The user must provide a CSV file and a time quantum value as command line arguments or else the program will exit as this info is needed
    if len(sys.argv) < 3:
        print("Usage: python scheduler.py <path_to_csv> <time_quantum>")
        sys.exit(1)

    # Grab the path to the CSV file and the time quantum value
    path = sys.argv[1]
    quantum = int(sys.argv[2])

    # Read the list of processes from the file
    processes = read_processes(path)

    # Run the Round Robin / Priority simulation and destructure the metrics
    completed, ctx, total_time = priority_round_robin(processes, quantum)

    # Calculate performance metrics for this run
    metrics = calculate_metrics(completed, ctx, total_time)

    # Print the data
    print(f"\n[Time Quantum = {quantum}]\n")
    print("PID\tArrival\tBurst\tPriority\tCompletion\tTurnaround\tWaiting")

    # Print info for each completed process
    for p in completed:
        tat = p.completion - p.arrival
        wt = tat - p.burst
        print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.priority}\t\t{p.completion}\t\t{tat}\t\t{wt}")

    # Print all calculated metrics nicely
    print("\nMetrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
