"""
Task 2A - Print HELLO WITHOUT Semaphores
Three threads start concurrently with no ordering control.
Letters print in unpredictable order — rarely "HELLO".
Run with: python3 hello_before.py
"""

import threading
import time
import random


def process1():
    # Prints H and E — but no guarantee when
    time.sleep(random.uniform(0, 0.05))
    print("H", end="", flush=True)
    time.sleep(random.uniform(0, 0.05))
    print("E", end="", flush=True)


def process2():
    # Prints L and L — but no guarantee when
    time.sleep(random.uniform(0, 0.05))
    print("L", end="", flush=True)
    time.sleep(random.uniform(0, 0.05))
    print("L", end="", flush=True)


def process3():
    # Prints O — but no guarantee when
    time.sleep(random.uniform(0, 0.05))
    print("O", end="", flush=True)


if __name__ == "__main__":
    print("=== Task 2A: HELLO WITHOUT Semaphores ===")
    print("Expected: HELLO")
    print("Actual output (10 runs):\n")

    for run in range(1, 11):
        print(f"Run {run:>2}: ", end="", flush=True)

        t1 = threading.Thread(target=process1)
        t2 = threading.Thread(target=process2)
        t3 = threading.Thread(target=process3)

        # All three start at the same time — no ordering
        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        print()  # newline after each run

    print("\n=== Program ended ===")
