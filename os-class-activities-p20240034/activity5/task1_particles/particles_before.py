"""
Task 1A - Particle Pair Buffer WITHOUT Semaphores
Demonstrates broken/unsafe behavior:
  - Buffer can overflow
  - Buffer can underflow
  - Pairs can be split (P1 and P2 from different producers)
Run with: python3 particles_before.py
Stop with: Ctrl+C  (or it stops itself when an error is detected)
"""

import threading
import time
import random

# ── Shared state ──────────────────────────────────────────────────────────────
BUFFER_CAPACITY = 100          # max particles (50 pairs)
buffer          = []           # list of particle strings
produced_pairs  = 0
packaged_pairs  = 0
error_flag      = False        # set True when an error is detected

# No locks / semaphores intentionally


# ── Producer ──────────────────────────────────────────────────────────────────
def producer(machine_id):
    global buffer, produced_pairs, error_flag

    pair_id = 0
    while not error_flag:
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        # ── NO semaphore: check + add is NOT atomic ───────────────────────────
        if len(buffer) + 2 > BUFFER_CAPACITY:
            print(f"\nThe producing machine is broken")
            error_flag = True
            return

        # Tiny sleep between the two appends so the consumer (or another
        # producer) can slip in between – this is what causes pair splitting.
        buffer.append(p1)
        time.sleep(random.uniform(0, 0.002))   # deliberate race window
        buffer.append(p2)

        produced_pairs += 1
        time.sleep(random.uniform(0.01, 0.05))


# ── Consumer ──────────────────────────────────────────────────────────────────
def consumer():
    global buffer, packaged_pairs, error_flag

    while not error_flag:
        time.sleep(random.uniform(0.01, 0.04))

        # ── NO semaphore: check + remove is NOT atomic ────────────────────────
        if len(buffer) < 2:
            print(f"\nThe packaging machine is broken")
            error_flag = True
            return

        p1 = buffer.pop(0)
        p2 = buffer.pop(0)

        # Verify they belong to the same pair (same machine + same pair_id)
        # Format: M<machine>-<pair_id>-P1  /  M<machine>-<pair_id>-P2
        p1_key = "-".join(p1.split("-")[:2])   # e.g. "M2-17"
        p2_key = "-".join(p2.split("-")[:2])

        if p1_key != p2_key:
            print(f"\nPairs are incorrect")
            print(f"  Got: {p1} + {p2}")
            error_flag = True
            return

        packaged_pairs += 1
        print(f"Packaged: {p1} + {p2}  |  "
              f"Produced: {produced_pairs}  |  "
              f"Packaged: {packaged_pairs}  |  "
              f"Buffer: {len(buffer)}")


# ── Status printer ────────────────────────────────────────────────────────────
def status_printer():
    while not error_flag:
        time.sleep(0.5)
        print(f"[STATUS] Produced pairs: {produced_pairs} | "
              f"Packaged pairs: {packaged_pairs} | "
              f"Buffer particles: {len(buffer)}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    NUM_PRODUCERS = 4

    print("=== Task 1A: Particle Buffer WITHOUT Semaphores ===")
    print(f"Producers: {NUM_PRODUCERS}  |  Buffer capacity: {BUFFER_CAPACITY} particles\n")

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

    # Wait until an error fires (or Ctrl+C)
    try:
        while not error_flag:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped by user.")

    time.sleep(0.3)   # let the error message print
    print("\n=== Program ended ===")
