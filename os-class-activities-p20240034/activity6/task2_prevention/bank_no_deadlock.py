"""
Task 2 - Bank Transfer WITH Deadlock Prevention
One shared mutex semaphore (init=1) protects the entire transfer.
Only one transfer runs at a time — no circular wait possible.
Run with: python3 bank_no_deadlock.py
"""

import threading
import time

# ── Shared mutex ──────────────────────────────────────────────────────────────
mutex = threading.Semaphore(1)   # only one transfer at a time

# ── Accounts ──────────────────────────────────────────────────────────────────
class Account:
    def __init__(self, name, balance):
        self.name    = name
        self.balance = balance

account_a = Account("Account-A", 1000)
account_b = Account("Account-B", 1000)

# ── Safe transfer ─────────────────────────────────────────────────────────────
def transfer(worker_id, frm, to, amount):
    name = f"Worker-{worker_id}"
    print(f"{name}: waiting to acquire mutex")
    mutex.acquire()
    try:
        print(f"{name}: mutex acquired — starting transfer")
        time.sleep(0.1)   # simulate processing time
        frm.balance -= amount
        to.balance  += amount
        print(f"{name}: transferred {amount} from {frm.name} to {to.name}  "
              f"| {frm.name}={frm.balance}  {to.name}={to.balance}")
    finally:
        mutex.release()
        print(f"{name}: mutex released")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Task 2: Bank Transfer WITH Deadlock Prevention ===")
    print(f"Strategy: single semaphore mutex (init=1)")
    print(f"Starting — Account-A: {account_a.balance}  "
          f"Account-B: {account_b.balance}")
    total_before = account_a.balance + account_b.balance
    print(f"Starting total: {total_before}\n")

    t1 = threading.Thread(target=transfer, args=(1, account_a, account_b, 100))
    t2 = threading.Thread(target=transfer, args=(2, account_b, account_a, 200))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    total_after = account_a.balance + account_b.balance
    print(f"\nFinal — Account-A: {account_a.balance}  "
          f"Account-B: {account_b.balance}")
    print(f"Final total: {total_after}")
    print(f"Balance check: {total_before} -> {total_after} "
          f"({'OK' if total_before == total_after else 'ERROR'})")
    print("\nNo deadlock occurred")
    print("\n=== Program ended ===")
