# Class Activity 3 — Socket Communication & Multithreading

- **Student Name:** LOR Hengrith
- **Student ID:** p20240034
- **Date:** 17 APRIL 2026

## Command Paths (Match Required Structure)

Use these folders when running commands so files are created in the expected locations:

```bash
# activity3 root
cd /home/hengrith/OS-SE-p20240034/os-class-activities-p20240034/activity3

# create required directories (once)
mkdir -p screenshots task1_socket task2_threads task3_java

# Task 1 commands run here
cd task1_socket

# Task 2 commands run here
cd ../task2_threads

# Task 3 commands run here
cd ../task3_java
```

Expected output/history files:

- `task1_socket/result_socket.txt`
- `task1_socket/command_used_socket.txt`
- `task2_threads/result_threads.txt`
- `task2_threads/result_threads_mutex.txt`
- `task2_threads/result_observe_linux.txt`
- `task2_threads/command_used_threads.txt`
- `task3_java/result_thread_demo.txt`
- `task3_java/result_runnable_demo.txt`
- `task3_java/result_pool_demo.txt`
- `task3_java/command_used_java.txt`

---

## Task 1: TCP Socket Communication (C)

### Compilation & Execution

![Socket exchange](screenshots/task1_socket_exchange.png)

### Answers

1. **Role of `bind()` / Why client doesn't call it:**
   > Server calls `bind()` to listen on a fixed address/port. Client doesn't need it—`connect()` automatically assigns an ephemeral port.

2. **What `accept()` returns:**
   > A new socket file descriptor for the connected client. The original server socket stays open to listen for more connections.

3. **Starting client before server:**
   > Client fails with "Connection refused." Server must call `bind()`, `listen()`, and `accept()` before client connects.

4. **What `htons()` does:**
   > Converts port number from host byte order to network byte order (big-endian) for correct network transmission.

5. **Socket call sequence diagram:**
   > Server: socket → bind → listen → accept. Client: socket → connect. Then exchange: send/recv.

---

## Task 2: POSIX Threads (C)

### Output — Without Mutex (Race Condition)

![Threads output](screenshots/task2_threads_output.png)

### Output — With Mutex (Correct)

_(Include in the same screenshot or a separate one)_

### Answers

1. **What is a race condition?**
   > Multiple threads modify shared data without synchronization, causing unpredictable results. In `threads.c`, counter gets lost updates.

2. **What does `pthread_mutex_lock()` do?**
   > Locks a mutex so only one thread can enter the critical section at a time. Other threads wait until `unlock()`.

3. **Removing `pthread_join()`:**
   > Main thread exits immediately without waiting. Worker threads get killed, program terminates early with incomplete output.

4. **Thread vs Process:**
   > Threads share memory (lighter, faster, risky). Processes have separate memory (heavier, safer, isolated).

---

## Task 3: Java Multithreading

### ThreadDemo Output

![Java threading](screenshots/task3_java_output.png)

### RunnableDemo Output

_(Include output or screenshot)_

### PoolDemo Output

_(Include output or screenshot)_

### Answers

1. **Thread vs Runnable:**
   > Thread: extend class (simple, single inheritance). Runnable: implement interface (flexible, preferred).

2. **Pool size limiting concurrency:**
   > Pool size 2 means max 2 tasks run concurrently. Others queue and wait. Limits resources and prevents thread explosion.

3. **thread.join() in Java:**
   > Blocks main thread until worker threads finish. Without it, main exits while threads still running.

4. **ExecutorService advantages:**
   > Pooling/reuse, task queuing, lifecycle management, exception handling, better scaling.

---

## Task 4: Observing Threads

### Linux — `ps -eLf` Output

_(Paste the relevant ps output here)_

### Linux — htop Thread View

![htop threads](screenshots/task4_htop_threads.png)

### Windows — Task Manager

![Task Manager threads](screenshots/task4_taskmanager_threads.png)

### Answers

1. **LWP column meaning:**
   > Light Weight Process ID—the Linux kernel thread ID. Shows OS-level visibility of each thread.

2. **/proc/PID/task/ count:**
   > Number of files = number of threads. 5 worker threads + 1 main = 6 entries.

3. **Extra Java threads:**
   > JVM creates threads for GC, signal handling, and housekeeping. More threads than you explicitly created.

4. **Linux vs Windows thread viewing:**
   > Linux: `ps -eLf` shows LWP; each thread separate line. Windows: Task Manager shows total count, not per-thread.

---

## Reflection

> Socket communication shows how networked programs exchange data across processes. Threading and mutexes reveal the complexity of concurrent access to shared memory—understanding OS-level synchronization helps prevent race conditions and write safer, more efficient concurrent code. This foundation is crucial for building scalable systems.