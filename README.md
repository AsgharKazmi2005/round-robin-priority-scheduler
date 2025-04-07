How to run the priority scheduler:

1. Download or clone the repository
2. Open the folder/repo
3. Open a terminal rooted in the home directory of the repository
4. Run the priority scheduler using the following syntax:
         python scheduler.py proc_list.csv [TIME_QUANTUM]

You may adjust the proc_list or time quantum as you desire to test different configurations

____________________________________________________________________________________________________________________________________________________________________________________

Sample Output with a time quantum of 4:

PID     Arrival Burst   Priority    Completion  Turnaround  Waiting
1       0       5       2           12          12          7
2       1       7       1           17          16          9

Metrics:
Avg Waiting Time: 6.25
Avg Turnaround Time: 10.75
CPU Utilization: 0.92
Throughput: 0.25
Context Switches: 14

____________________________________________________________________________________________________________________________________________________________________________________

Project Details:

This project uses a combination of the Round Robin scheduling algorithm and the Priority scheduling algorithm to efficiently and fairly simulate CPU process execution. Round-robin refers to the context switching of processes based on a time quantum. Round-robin ensures that every pricess has its fair opportunity to utlize CPU resources. However, if we purely rely on Round-robin, yes the resources will be more evenly split, but that is not what we always want. Rather, we want to make sure that high priority process execute first as they are more important, so we sort the ready queue based on their priority. The issue raised by this is starvation. If we always give priority to high-priority processes, the low-priority processes will starve. To fix this, the algorithm also implements aging which gradually increments the priority of low-priority processes the longer they are in the queue.

_____________________________________________________________________________________________________________________________________________________________________________________

Gallery:
