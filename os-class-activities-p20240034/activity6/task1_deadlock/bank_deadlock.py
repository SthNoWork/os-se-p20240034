"""
Task 1 - Bank Transfer WITH Deadlock
Worker 1: Account A -> Account B
Worker 2: Account B -> Account A
Each locks source first, then destination — causes circular wait.
Run with: python3 bank_deadlock.py
"""

import threading
import time

# ── Accounts ──────────────────────────────────────────────────────────────────
class Account:
    def __init__(self, name, balance):
        self.name    = name
        self.balance = balance
        self.lock    = threading.Semaphore(1)

account_a = Account("Account-A", 1000)
account_b = Account("Account-B", 1000)

transfer_done = [False, False]   # track completion per worker

# ── Unsafe transfer (causes deadlock) ─────────────────────────────────────────
def transfer(worker_id, frm, to, amount):
    name = f"Worker-{worker_id}"
    try:
        print(f"{name}: trying to lock {frm.name} (source)")
        frm.lock.acquire()
        print(f"{name}: locked {frm.name}")

        time.sleep(0.15)          # pause so the other thread runs and grabs its lock

        print(f"{name}: trying to lock {to.name} (destination)  <-- may wait here")
        to.lock.acquire()
        print(f"{name}: locked {to.name}")

        frm.balance -= amount
        to.balance  += amount
        print(f"{name}: transfer of {amount} complete  "
              f"| {frm.name}={frm.balance}  {to.name}={to.balance}")

        to.lock.release()
        frm.lock.release()
        transfer_done[worker_id - 1] = True

    except Exception as e:
        print(f"{name}: exception — {e}")


# ── Watchdog ──────────────────────────────────────────────────────────────────
def watchdog(threads, timeout=2.5):
    time.sleep(timeout)
    if not all(transfer_done):
        print("\nDeadlock detected: transactions are stuck")
        still_waiting = []
        if not transfer_done[0]:
            still_waiting.append("Worker-1 is waiting for Account-B")
        if not transfer_done[1]:
            still_waiting.append("Worker-2 is waiting for Account-A")
        for msg in still_waiting:
            print(f"  {msg}")
        print(f"\n  Current balances (unchanged due to deadlock):")
        print(f"  Account-A: {account_a.balance}")
        print(f"  Account-B: {account_b.balance}")
        import os
        os._exit(1)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Task 1: Bank Transfer WITHOUT Deadlock Prevention ===")
    print(f"Starting balances — Account-A: {account_a.balance}  "
          f"Account-B: {account_b.balance}")
    print(f"Starting total: {account_a.balance + account_b.balance}\n")

    t1 = threading.Thread(target=transfer, args=(1, account_a, account_b, 100))
    t2 = threading.Thread(target=transfer, args=(2, account_b, account_a, 200))
    wd = threading.Thread(target=watchdog, args=([t1, t2],), daemon=True)

    t1.start()
    t2.start()
    wd.start()

    t1.join()
    t2.join()

    if all(transfer_done):
        print(f"\nFinal — Account-A: {account_a.balance}  "
              f"Account-B: {account_b.balance}")
        print(f"Final total: {account_a.balance + account_b.balance}")

    print("\n=== Program ended ===")
