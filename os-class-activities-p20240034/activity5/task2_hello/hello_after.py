"""
Task 2B - Print HELLO WITH Semaphores
Semaphores force the correct print order every time.

Semaphore design:
  start_h  (init=1) — lets Process 1 print H immediately
  after_e  (init=0) — blocks Process 2 until H and E are done
  after_l1 (init=0) — blocks Process 2's second L until first L is done
  after_l2 (init=0) — blocks Process 3 until both L's are done

Order enforced: H → E → L → L → O

Run with: python3 hello_after.py
"""

import threading


# ── Semaphores ────────────────────────────────────────────────────────────────
start_h  = threading.Semaphore(1)   # Process 1 may begin immediately
after_e  = threading.Semaphore(0)   # Process 2 waits until HE is printed
after_l1 = threading.Semaphore(0)   # Process 2 waits between its two L's
after_l2 = threading.Semaphore(0)   # Process 3 waits until LL is printed


def process1():
    """Prints H then E, then signals Process 2 to start."""
    start_h.acquire()
    print("H", end="", flush=True)
    print("E", end="", flush=True)
    after_e.release()               # allow Process 2 to print first L


def process2():
    """Prints first L, signals itself, prints second L, signals Process 3."""
    after_e.acquire()               # wait for HE
    print("L", end="", flush=True)
    after_l1.release()              # allow own second step

    after_l1.acquire()              # wait (ensures first L is committed)
    print("L", end="", flush=True)
    after_l2.release()              # allow Process 3 to print O


def process3():
    """Prints O after both L's are done."""
    after_l2.acquire()              # wait for LL
    print("O", end="", flush=True)


if __name__ == "__main__":
    print("=== Task 2B: HELLO WITH Semaphores ===")
    print("Semaphores: start_h=1, after_e=0, after_l1=0, after_l2=0\n")

    print("Output: ", end="", flush=True)

    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t3 = threading.Thread(target=process3)

    # All three start concurrently — semaphores enforce the order
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print()   # newline after HELLO
    print("\n=== Program ended ===")
