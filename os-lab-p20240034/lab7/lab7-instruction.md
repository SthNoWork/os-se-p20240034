# OS Lab 7 — Bash Scripting, Permissions & Server Automation (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Bash Scripting, Permissions & Server Automation |
| **Chapter** | Shell Scripting, Linux Permissions, Automation |
| **Duration** | 3 Hours |
| **Lab Type** | Individual, with peer interaction |

---

> ⚠️ **IMPORTANT — READ EVERYTHING FIRST**
>
> This lab has scripts that depend on files and permissions created in earlier tasks. Do not skip ahead.

---

## Lab Objectives

1. Write executable Bash scripts using a shebang.
2. Add a personal `~/bin` directory to the shell `PATH`.
3. Customize login behavior using `.bashrc`.
4. Configure Linux permissions for public read-only and write-only directories.
5. Use Bash variables, arrays, loops, command substitution, and redirection.
6. Demonstrate SUID behavior with a compiled C helper program.
7. Write scripts that safely inspect peer directories on a shared Linux server.
8. Automate cross-user feedback by writing messages into peer drop-boxes.

> **Scenario:** You are building a small "server neighborhood" inside `/home`. Each student has a house, an inbox, an outbox, and a few automation bots.

---

## Task Overview

| Task | Title | Key Commands / Concepts | Screenshots Required |
|:---:|-------|-------------------------|:-------------------:|
| **1** | Warm-Up Script | shebang, `chmod +x`, `./script` | ✅ |
| **2** | Custom Command Center | `PATH`, `.bashrc`, `source` | ✅ |
| **3** | Doorstep Login Message | variables, arrays, command substitution | ✅ |
| **4** | Secure Mailbox | `chmod 733`, write-only drop-box | ✅ |
| **5** | Broadcaster Script | redirection, timestamps, public outbox | ✅ |
| **6** | VIP Guestbook | C wrapper, SUID, restricted file writes | ✅ |
| **7** | Data Harvester | loops, `/home/*`, readable-file checks | ✅ |
| **8** | Mailman Bot | `while read`, parsing, cross-user writing | ✅ |

---

## Lab Setup

Navigate into your repo and create the lab7 directory structure all at once:

```bash
cd ~/Desktop/github/os-se-p20240034/os-lab-p20240034
mkdir -p lab7/images lab7/scripts
cd lab7
```

> ✅ This creates:
> ```
> lab7/
> ├── images/
> └── scripts/
> ```

> ⚠️ **Your lab7 path is:**
> `~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab7/`
> This is referred to as `LAB7` in every command below.

Set it as a variable so you don't have to type it every time:
```bash
LAB7=~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab7
```
> ⚠️ You must re-run this line any time you open a new terminal.

---

## Quick Reference

### Bash Script Basics

| Syntax | Purpose |
|--------|---------|
| `#!/bin/bash` | Shebang: tells Linux to run the file with Bash |
| `chmod +x scriptname` | Makes a script executable |
| `./scriptname` | Runs a script from the current directory |
| `echo "text"` | Prints text |
| `date +"%Y-%m-%d %H:%M:%S"` | Prints a formatted timestamp |

### PATH and Configuration

| Command | Purpose |
|---------|---------|
| `echo $PATH` | Shows executable search paths |
| `export PATH="$HOME/bin:$PATH"` | Adds `~/bin` to the front of `PATH` |
| `source ~/.bashrc` | Reloads `.bashrc` without logging out |
| `which commandname` | Shows which executable will run |

### Permissions

| Permission | Meaning |
|------------|---------|
| `chmod 755 dir` | Owner can write; everyone can read/enter |
| `chmod 733 dir` | Owner full access; others can write/enter but cannot list |
| `chmod 600 file` | Owner read/write only |
| `chmod u+s file` | Sets SUID bit on an executable |

---

## Task 1 — Warm-Up Script

**Scenario:** *"Prove that you understand how Linux executes script files."*

Create your personal script directory:

```bash
mkdir -p ~/bin
chmod 755 ~/bin
```

Create the `warmup` script:

```bash
cat > ~/bin/warmup << 'EOF'
#!/bin/bash
echo "Hello from my first script! My current directory is:"
pwd
EOF
```

Try running it without execute permission first (this should fail):

```bash
./~/bin/warmup
```

Now make it executable and run it:

```bash
chmod +x ~/bin/warmup
~/bin/warmup
```

Save evidence to `task1_warmup.txt`:

```bash
{
echo "=== warmup permissions ==="
ls -l ~/bin/warmup
echo "=== warmup output ==="
~/bin/warmup
} > $LAB7/task1_warmup.txt
```

---

📸 **Screenshot 1 starts here:**
```bash
cat $LAB7/task1_warmup.txt
```
📸 **Screenshot 1 ends here**
> Save as: `images/task1_warmup.png`

---

## Task 2 — Custom Command Center: Setting Up PATH

**Scenario:** *"Make your personal scripts run like normal commands without typing `./`."*

Add `~/bin` to your PATH in `.bashrc`:

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Save evidence to `task2_path.txt`:

```bash
{
echo "=== PATH ==="
echo "$PATH"
echo "=== warmup location ==="
which warmup
echo "=== warmup command output ==="
warmup
} > $LAB7/task2_path.txt
```

---

📸 **Screenshot 2 starts here:**
```bash
cat $LAB7/task2_path.txt
```
📸 **Screenshot 2 ends here**
> Save as: `images/task2_path.png`

---

## Task 3 — Doorstep: Dynamic Login Message

**Scenario:** *"When you log in, your shell should greet you and show a server status snapshot."*

Add the doorstep message block to `.bashrc`:

```bash
cat >> ~/.bashrc << 'EOF'

# Lab 7 doorstep message
users_online=$(who | wc -l)
uptime_info=$(uptime -p)
jokes=("Keep calm and check the logs." "There is no place like 127.0.0.1." "Automate the boring stuff.")
joke=${jokes[$RANDOM % ${#jokes[@]}]}

echo "========================================"
echo "Welcome, $USER"
echo "Users currently logged in: $users_online"
echo "Server uptime: $uptime_info"
echo "Random tech quote: $joke"
echo "========================================"
EOF
```

Test it and save evidence:

```bash
source ~/.bashrc > $LAB7/task3_doorstep.txt
```

---

📸 **Screenshot 3 starts here:**
```bash
cat $LAB7/task3_doorstep.txt
```
📸 **Screenshot 3 ends here**
> Save as: `images/task3_doorstep.png`

---

## Task 4 — Secure Mailbox: Write-Only Drop-Box

**Scenario:** *"Classmates should be able to drop files into your inbox, but not list or read others' messages."*

Create the inbox:

```bash
mkdir -p ~/public_inbox
chmod 733 ~/public_inbox
```

Save evidence to `task4_inbox.txt`:

```bash
{
echo "=== inbox permissions ==="
ls -ld ~/public_inbox
echo "=== inbox files as owner ==="
ls -l ~/public_inbox
} > $LAB7/task4_inbox.txt
```

> 👥 **Ask a classmate** to run this from their account (replace `ken` with your username):
> ```bash
> ls /home/ken/public_inbox          # should fail: Permission denied
> touch /home/ken/public_inbox/test_from_<theirname>.txt   # should succeed
> ```

---

📸 **Screenshot 4 starts here:**
```bash
cat $LAB7/task4_inbox.txt
```
📸 **Screenshot 4 ends here**
> Save as: `images/task4_inbox.png`

---

## Task 5 — Broadcaster: Public Outbox Automation

**Scenario:** *"Create data for the server neighborhood. Your classmates' bots will try to find it."*

Create the public outbox:

```bash
mkdir -p ~/public_outbox
chmod 755 ~/public_outbox
```

Create the `broadcaster` script:

```bash
cat > ~/bin/broadcaster << 'EOF'
#!/bin/bash

secrets=("kernel" "mutex" "scheduler" "filesystem" "semaphore")
secret=${secrets[$RANDOM % ${#secrets[@]}]}
current_time=$(date +"%Y-%m-%d %H:%M:%S")

echo "$secret - $current_time" > "$HOME/public_outbox/secret.txt"
chmod 644 "$HOME/public_outbox/secret.txt"
echo "Broadcast complete: $HOME/public_outbox/secret.txt"
EOF

chmod +x ~/bin/broadcaster
broadcaster
```

Save evidence to `task5_broadcaster.txt`:

```bash
{
echo "=== broadcaster script ==="
ls -l ~/bin/broadcaster
echo "=== outbox permissions ==="
ls -ld ~/public_outbox
echo "=== secret.txt ==="
cat ~/public_outbox/secret.txt
} > $LAB7/task5_broadcaster.txt
```

---

📸 **Screenshot 5 starts here:**
```bash
cat $LAB7/task5_broadcaster.txt
```
📸 **Screenshot 5 ends here**
> Save as: `images/task5_broadcaster.png`

---

## Task 6 — VIP Guestbook: SUID Helper Program

**Scenario:** *"Classmates should be able to sign your guestbook without getting direct access to the file."*

Create and lock down the guestbook:

```bash
touch ~/guestbook.txt
chmod 600 ~/guestbook.txt
```

Create `sign_book.c` in your lab7 folder:

```bash
cat > $LAB7/sign_book.c << 'EOF'
#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: sign_book 'Your Name'\n");
        return 1;
    }

    FILE *file = fopen("/home/ken/guestbook.txt", "a");
    if (file == NULL) {
        printf("Error opening guestbook.\n");
        return 1;
    }

    fprintf(file, "Visitor signed: %s\n", argv[1]);
    fclose(file);
    printf("Successfully signed the VIP guestbook!\n");
    return 0;
}
EOF
```

Compile it and set SUID:

```bash
gcc $LAB7/sign_book.c -o ~/bin/sign_book
chmod 4755 ~/bin/sign_book
chmod 711 "$HOME"
```

> 👥 **Ask a classmate** to run (replace `ken` with your username):
> ```bash
> /home/ken/bin/sign_book "Hello from <theirname>"
> ```

Verify the guestbook:

```bash
cat ~/guestbook.txt
```

Save evidence to `task6_guestbook.txt`:

```bash
{
echo "=== guestbook permissions ==="
ls -l ~/guestbook.txt
echo "=== sign_book permissions ==="
ls -l ~/bin/sign_book
echo "=== guestbook contents ==="
cat ~/guestbook.txt
} > $LAB7/task6_guestbook.txt
```

---

📸 **Screenshot 6 starts here:**
```bash
cat $LAB7/task6_guestbook.txt
```
📸 **Screenshot 6 ends here**
> Save as: `images/task6_guestbook.png`

---

## Task 7 — Data Harvester: Cross-User Scripting

**Scenario:** *"Write a bot that scans the server neighborhood and collects readable secrets."*

Create the `harvester` script:

```bash
cat > ~/bin/harvester << 'EOF'
#!/bin/bash

report="$HOME/harvest_report.txt"
> "$report"

for user_dir in /home/*; do
    username=$(basename "$user_dir")
    target_file="$user_dir/public_outbox/secret.txt"

    if [ -f "$target_file" ] && [ -r "$target_file" ]; then
        secret_data=$(cat "$target_file")
        echo "${username}'s secret is: $secret_data" >> "$report"
    fi
done

echo "Harvest complete. Report saved to $report"
EOF

chmod +x ~/bin/harvester
harvester
```

Copy the report to lab7:

```bash
cp ~/harvest_report.txt $LAB7/harvest_report.txt
```

---

📸 **Screenshot 7 starts here:**
```bash
cat $LAB7/harvest_report.txt
```
📸 **Screenshot 7 ends here**
> Save as: `images/task7_harvester.png`

---

## Task 8 — Mailman Bot: Automated Feedback

**Scenario:** *"Drop automated messages into classmates' inboxes based on what your harvester found."*

Create the `mailman` script:

```bash
cat > ~/bin/mailman << 'EOF'
#!/bin/bash

report="$HOME/harvest_report.txt"
sent_count=0

if [ ! -f "$report" ]; then
    echo "Missing $report. Run harvester first."
    exit 1
fi

while read -r line; do
    classmate=$(echo "$line" | awk -F"'" '{print $1}')
    secret=$(echo "$line" | awk -F"is: " '{print $2}' | awk -F" - " '{print $1}')
    inbox="/home/$classmate/public_inbox"
    message="$inbox/message_from_$USER.txt"

    if [ -d "$inbox" ]; then
        echo "Hello $classmate, I am an automated bot written by $USER. I successfully read your secret word: $secret." > "$message" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Sent message to $classmate"
            sent_count=$((sent_count + 1))
        else
            echo "Could not write to $classmate's inbox"
        fi
    fi

    if [ "$sent_count" -ge 3 ]; then
        break
    fi
done < "$report"

echo "Messages sent: $sent_count"
EOF

chmod +x ~/bin/mailman
mailman
```

Save evidence to `task8_mailman.txt`:

```bash
{
echo "=== mailman output ==="
mailman
echo "=== my inbox ==="
ls -l ~/public_inbox
echo "=== messages I received ==="
cat ~/public_inbox/message_from_*.txt 2>/dev/null
} > $LAB7/task8_mailman.txt
```

---

📸 **Screenshot 8 starts here:**
```bash
cat $LAB7/task8_mailman.txt
```
📸 **Screenshot 8 ends here**
> Save as: `images/task8_mailman.png`

---

## Copy Scripts for Submission

Run this after all tasks are done:

```bash
cp ~/bin/warmup $LAB7/scripts/
cp ~/bin/broadcaster $LAB7/scripts/
cp ~/bin/harvester $LAB7/scripts/
cp ~/bin/mailman $LAB7/scripts/
cp ~/bin/sign_book $LAB7/scripts/sign_book_binary
```

---

## Verify Your Folder Structure

```bash
ls -1 $LAB7/*.txt $LAB7/sign_book.c
ls -1 $LAB7/scripts/
ls -1 $LAB7/images/
```

Expected output:
```
lab7/
├── README.md
├── task1_warmup.txt
├── task2_path.txt
├── task3_doorstep.txt
├── task4_inbox.txt
├── task5_broadcaster.txt
├── task6_guestbook.txt
├── harvest_report.txt
├── task8_mailman.txt
├── sign_book.c
├── scripts/
│   ├── warmup
│   ├── broadcaster
│   ├── harvester
│   ├── mailman
│   └── sign_book_binary
└── images/
    ├── task1_warmup.png
    ├── task2_path.png
    ├── task3_doorstep.png
    ├── task4_inbox.png
    ├── task5_broadcaster.png
    ├── task6_guestbook.png
    ├── task7_harvester.png
    └── task8_mailman.png
```

---

## Git Push

```bash
cd ~/Desktop/github/os-se-p20240034
git add .
git commit -m "Lab 7: Bash scripting and server automation"
git push origin main
```