# How to Use AI to Complete Class Activity 4 — Prompt Guide

---

## The Opening Prompt

Paste this at the start of a new session along with your activity instruction file and final structure file:

```
I have a class activity to complete. I will attach the instruction file
and the required folder structure.

Guide me one task at a time. Wait for me to say "next" before moving on.

Rules:
- Send commands in chunks I can paste directly into bash.
- Use cat heredoc (cat > file << 'EOF') to create all source code files.
  Never tell me to use nano or a text editor.
- For screenshot steps, clearly mark them like this:

    📸 Screenshot N starts here:
    [command]
    📸 Screenshot N ends here
    Save as: screenshots/filename.png

- This activity uses TWO machines (server and client). Label every chunk
  clearly with who runs it: "Server Machine", "Student A", or "Student B".
- My username is: ken
- My activity path is:
  ~/Desktop/github/os-se-p20240034/os-class-activities-p20240034/activity4
- Set this as ACT4 variable at the start so commands use it automatically.
- Hardcode my real path. No placeholders except <SERVER_IP> which I will
  fill in myself after running hostname -I.
- Keep explanations short. Commands only.

Start with Task 1.
```

---

## What Each Task Response Should Look Like

```
## Task 1 — C++ Before Mutex

### Server Machine:

    cat > $ACT4/cpp_before/server_no_mutex.cpp << 'EOF'
    [source code here]
    EOF

    cd $ACT4
    echo 0 > shared_score.txt
    g++ ... -o cpp_before/server_no_mutex -pthread
    ./cpp_before/server_no_mutex

### Student A:

    for i in {1..10}; do ./cpp_before/client <SERVER_IP> A_$i & done
    wait

### Student B (run at the same time):

    for i in {1..10}; do ./cpp_before/client <SERVER_IP> B_$i & done
    wait

---

📸 Screenshot 1 starts here:
    cat $ACT4/shared_score.txt
📸 Screenshot 1 ends here
Save as: screenshots/cpp_before_mutex.png
```

---

## Navigation Commands

| You want to... | Say this |
|----------------|----------|
| Move to next task | `next` |
| Repeat current task | `repeat task [number]` |
| Fix an error | Paste the error message directly |
| Ask what a command does | `what does [command] do?` |

---

## Important Notes for This Activity

- **Always reset `shared_score.txt` before each task:**
  ```bash
  echo 0 > $ACT4/shared_score.txt
  ```

- **Stop a server before starting the next one:**
  Press `Ctrl+C` in the server terminal.

- **Each task uses a different port** — don't mix them up:

  | Task | Port |
  |------|------|
  | C++ before mutex | 9001 |
  | C++ after mutex | 9002 |
  | Java before synchronized | 9011 |
  | Java after synchronized | 9012 |

- **Screenshots must show all 3 terminals** — server + Student A + Student B.
  Take a combined/collage screenshot or tile your windows before capturing.

- **Both partners submit the same files** — same screenshots, same source files,
  each in their own repo under `os-class-activities-<StudentID>/activity4/`.

---

## Template: Full Opening Message (Ready to Copy)

```
I have a class activity to complete. Attached are the instruction file
and the required folder structure.

Guide me one task at a time. Wait for "next" before moving on.

Rules:
- Chunk commands for direct bash paste.
- Use cat heredoc for all source files. No nano.
- Mark screenshots:
    📸 Screenshot N starts here:
    [command]
    📸 Screenshot N ends here
    Save as: screenshots/filename.png
- Label every command block: Server Machine / Student A / Student B.
- My path: ~/Desktop/github/os-se-p20240034/os-class-activities-p20240034/activity4
- Set it as ACT4 at the start.
- Keep <SERVER_IP> as a placeholder — I will fill it in myself.
- Commands only, short explanations.

Start with Task 1.
```