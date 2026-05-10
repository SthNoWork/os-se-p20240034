# How to Use AI to Complete Linux Labs — Prompt Guide

This guide explains how to instruct an AI assistant to walk you through
a Linux lab the same way this session was done — one task at a time,
with clear screenshot markers.

---

## The Starting Prompt

Paste this at the start of every new lab session, along with your lab
instruction file and the final folder structure file:

```
I have a Linux lab to complete. I will give you the lab instructions
and the required final folder structure.

I need you to guide me through it one task at a time.

Rules:
- Send one task at a time. Wait for me to say "next" before moving on.
- Send commands in chunks that I can paste directly into bash.
- For any step that requires a screenshot, wrap the exact command(s)
  inside clearly marked headers like this:

  📸 Screenshot X starts here:
  [command]
  📸 Screenshot X ends here
  Save as: images/filename.png

- Use heredoc (cat > file << 'EOF') to create script files instead of nano.
- Hardcode my actual username and paths. My username is [YOUR USERNAME]
  and my lab path is [YOUR FULL LAB PATH].
- If a command saves output to a .txt file, the screenshot command should
  just be: cat filename.txt
- Do not explain theory. Only give commands and brief notes where needed.

Start with Task 1 when I say "start".
```

> Replace `[YOUR USERNAME]` and `[YOUR FULL LAB PATH]` with your real values.
> Example: username = `ken`, lab path = `~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab7`

---

## How Each Task Should Look

A good task response from the AI looks like this:

```
## Task 1 — Warm-Up Script

Run this to create the script:

    mkdir -p ~/bin
    chmod 755 ~/bin
    cat > ~/bin/warmup << 'EOF'
    #!/bin/bash
    echo "Hello! Current directory:"
    pwd
    EOF
    chmod +x ~/bin/warmup

Save the output:

    ~/bin/warmup > /your/lab/path/task1_warmup.txt

---

📸 Screenshot 1 starts here:
    cat /your/lab/path/task1_warmup.txt
📸 Screenshot 1 ends here
Save as: images/task1_warmup.png
```

---

## What to Say to Move Between Tasks

| You want to... | Say this |
|----------------|----------|
| Start the lab | `start` |
| Move to next task | `next` |
| Repeat current task | `repeat task [number]` |
| Fix an error | Paste the error message directly |
| Skip a task | `skip to task [number]` |
| Ask about a command | `what does [command] do?` |

---

## When You Get an Error

Just paste the error message directly into the chat. Example:

```
rm: cannot remove '/opt/techcorp/devproject/file.txt': Operation not permitted
```

The AI will explain whether it is expected behavior or a real error,
and give you the fix if needed.

---

## Tips

- Always run the **Lab Setup** commands first to create your folder structure
  before starting Task 1.
- Set your lab path as a variable at the start of every new terminal session:
  ```bash
  LAB=~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab7
  ```
- For tasks that need a **classmate**, tell the AI:
  ```
  I need to do the classmate step. What do they need to run?
  ```
  The AI will give you the exact command to send to your classmate.
- Take the screenshot **before** pressing Enter on the next command so the
  output is still visible on screen.
- Save screenshots immediately after each marked section — do not batch them
  at the end.

---

## Template: Full Opening Message

Copy and fill in the blanks, then paste it along with your uploaded lab files:

```
I have a Linux lab to complete. I will attach the lab instruction file
and the required folder structure file.

Guide me one task at a time. Wait for me to say "next" before moving on.

Rules:
- Chunk commands so I can paste them into bash directly.
- For screenshot steps, wrap the command in:
    📸 Screenshot N starts here:
    [command]
    📸 Screenshot N ends here
    Save as: images/filename.png
- Use cat heredoc instead of nano for creating files.
- My Linux username is: ken
- My lab folder path is: ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab7
- Hardcode these into every command. Do not use placeholders.
- Keep explanations short. Commands only.

Start with Task 1.
```