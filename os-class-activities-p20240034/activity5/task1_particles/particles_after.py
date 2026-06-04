"""
Task 1B - Particle Pair Buffer WITH Semaphores
Correct synchronization using three semaphores:

  empty_pairs  (Counting, init=50)  – pair slots available in the buffer
  full_pairs   (Counting, init=0)   – complete pairs waiting to be packaged
  mutex        (Binary,   init=1)   – protects buffer list and counters

Run with: python3 particles_after.py
Stop with: Ctrl+C  (runs forever if correct; stops itself only on a detected error)
"""

import threading
import time
import random

# ── Shared state ──────────────────────────────────────────────────────────────
BUFFER_CAPACITY = 100          # 100 particles = 50 pairs
BUFFER_PAIRS    = BUFFER_CAPACITY // 2

buffer         = []            # list of particle strings
produced_pairs = 0
packaged_pairs = 0
error_flag     = False

# ── Semaphores ────────────────────────────────────────────────────────────────
empty_pairs = threading.Semaphore(BUFFER_PAIRS)   # 50 pair-slots free
full_pairs  = threading.Semaphore(0)              # 0 complete pairs ready
mutex       = threading.Semaphore(1)              # mutual exclusion


# ── Producer ──────────────────────────────────────────────────────────────────
def producer(machine_id):
    global buffer, produced_pairs, error_flag

    pair_id = 0
    while not error_flag:
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        # Wait until there is room for one more pair
        empty_pairs.acquire()

        # Enter critical section
        mutex.acquire()
        try:
            # Safety check (should never fire with correct semaphores)
            if len(buffer) + 2 > BUFFER_CAPACITY:
                print("\nThe producing machine is broken")
                error_flag = True
                return

            # Add BOTH particles atomically (inside mutex)
            buffer.append(p1)
            buffer.append(p2)
            produced_pairs += 1
        finally:
            mutex.release()

        # Signal that one more complete pair is available
        full_pairs.release()

        # Small sleep to keep output readable
        time.sleep(random.uniform(0.02, 0.08))


# ── Consumer ──────────────────────────────────────────────────────────────────
def consumer():
    global buffer, packaged_pairs, error_flag

    while not error_flag:
        # Wait until at least one complete pair is available
        full_pairs.acquire()

        # Enter critical section
        mutex.acquire()
        try:
            # Safety check (should never fire with correct semaphores)
            if len(buffer) < 2:
                print("\nThe packaging machine is broken")
                error_flag = True
                return

            p1 = buffer.pop(0)
            p2 = buffer.pop(0)

            # Verify pair integrity
            # Format: M<machine>-<pair_id>-P1  and  M<machine>-<pair_id>-P2
            p1_key = "-".join(p1.split("-")[:2])   # e.g. "M2-17"
            p2_key = "-".join(p2.split("-")[:2])

            if p1_key != p2_key:
                print("\nPairs are incorrect")
                print(f"  Got: {p1} + {p2}")
                error_flag = True
                return

            packaged_pairs += 1
            buf_size = len(buffer)
        finally:
            mutex.release()

        # Signal that one pair-slot is now free
        empty_pairs.release()

        print(f"Packaged: {p1} + {p2}  |  "
              f"Produced pairs: {produced_pairs}  |  "
              f"Packaged pairs: {packaged_pairs}  |  "
              f"Buffer: {buf_size}")

        time.sleep(random.uniform(0.03, 0.07))


# ── Periodic status printer ───────────────────────────────────────────────────
def status_printer():
    while not error_flag:
        time.sleep(1.0)
        print(f"\n[STATUS] Produced pairs: {produced_pairs} | "
              f"Packaged pairs: {packaged_pairs} | "
              f"Buffer particles: {len(buffer)}\n")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    NUM_PRODUCERS = 4

    print("=== Task 1B: Particle Buffer WITH Semaphores ===")
    print(f"Producers : {NUM_PRODUCERS}")
    print(f"Buffer cap: {BUFFER_CAPACITY} particles ({BUFFER_PAIRS} pairs)")
    print("Semaphores: empty_pairs=50, full_pairs=0, mutex=1")
    print("Press Ctrl+C to stop.\n")

    threads = []

    for i in range(1, NUM_PRODUCERS + 1):
        t = threading.Thread(target=producer, args=(i,), daemon=True)
        threads.append(t)

    consumer_thread = threading.Thread(target=consumer, daemon=True)
    threads.append(consumer_thread)

    status_thread = threading.Thread(target=status_printer, daemon=True)
    threads.append(status_thread)

    for t in threads:
        t.start()

    try:
        while not error_flag:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped by user (Ctrl+C).")

    time.sleep(0.3)
    print("\n=== Program ended ===")
