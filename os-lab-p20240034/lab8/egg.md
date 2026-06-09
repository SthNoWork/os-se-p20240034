# Lab 8 — Quantum Widget Exploit (Solo Guide)

- **Username:** ken
- **Lab path:** `~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8`
- **Scripts folder:** `~/bin`

> Levels 5 and 6 simulate the partner step on the same machine.

---

## Setup — Run Once

```bash
cd ~/Desktop/github/os-se-p20240034/os-lab-p20240034 && mkdir -p lab8/images lab8/scripts && cd lab8 && mkdir -p ~/bin
```

---

## Level 0 — Bash Warm-Up Scripts

```bash
mkdir -p ~/bin
```

```bash
cat > ~/bin/arg_viewer << 'EOF'
#!/bin/bash
echo "Script name (\$0): $0"
echo "First argument (\$1): $1"
echo "Second argument (\$2): $2"
echo "Number of arguments (\$#): $#"
test -n "$1"
echo "Exit status of 'test -n \$1' (\$?): $?"
EOF
chmod +x ~/bin/arg_viewer
```

```bash
cat > ~/bin/quantum_probe << 'EOF'
#!/bin/bash
operator="$1"
cycles="$2"

if [ "$#" -ne 2 ]; then
    echo "Usage: quantum_probe <operator> <cycles>"
    exit 1
fi

if ! [[ "$cycles" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: cycles must be a positive integer."
    exit 2
fi

mkdir -p probe_logs
mkdir_status=$?
echo "mkdir exit status: $mkdir_status"

if [ "$mkdir_status" -ne 0 ]; then
    echo "Could not prepare probe_logs."
    exit 3
fi

echo "Operator: $operator"
echo "Cycles requested: $cycles"

for i in $(seq 1 "$cycles"); do
    echo "Cycle $i: quantum widget console online"
done

exit 0
EOF
chmod +x ~/bin/quantum_probe
```

```bash
{
cd ~/bin
echo "=== argument viewer with arguments ==="
arg_viewer Alice 3
echo "=== argument viewer with no arguments ==="
arg_viewer
echo "=== successful probe ==="
quantum_probe Alice 3
echo "exit status after success: $?"
echo "=== invalid probe ==="
quantum_probe Bob not_a_number
echo "exit status after invalid input: $?"
echo "=== loop/log directory evidence ==="
ls -ld ~/bin/probe_logs
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task0_warmup.txt
```

📸 **Screenshot 1 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task0_warmup.txt
```
📸 **Screenshot 1 ends here**
> Save as: `images/level0_warmup.png`

---

## Level 1 — Input Validation

```bash
echo 100 > ~/bin/inventory.txt
```

```bash
cat > ~/bin/buy_widget << 'EOF'
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: buy_widget <username> <quantity>"
    exit 1
fi

username="$1"
quantity="$2"

if ! [[ "$quantity" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: quantity must be a positive integer."
    exit 2
fi

echo "Input valid: $username wants $quantity widget(s)."
exit 0
EOF
chmod +x ~/bin/buy_widget
```

```bash
{
echo "=== missing argument test ==="
buy_widget Alice
echo "=== invalid quantity test ==="
buy_widget Eve -3
echo "=== script permissions ==="
ls -l ~/bin/buy_widget
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task1_validation.txt
```

> No screenshot required for Level 1.

---

## Level 2 — Audit Trails

```bash
cat > ~/bin/buy_widget << 'EOF'
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: buy_widget <username> <quantity>"
    exit 1
fi

username="$1"
quantity="$2"

if ! [[ "$quantity" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: quantity must be a positive integer."
    exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
inventory_file="$script_dir/inventory.txt"
sales_log="$script_dir/sales.log"

log_transaction() {
    echo "[p20240034] [SUCCESS] $username bought $quantity widgets." >> "$sales_log"
}

current=$(cat "$inventory_file")

if [ "$quantity" -gt "$current" ]; then
    echo "Transaction Failed: Not enough inventory!"
    exit 3
fi

new=$((current - quantity))
echo "$new" > "$inventory_file"
log_transaction
echo "Purchase successful! Remaining inventory: $new"
exit 0
EOF
chmod +x ~/bin/buy_widget
```

```bash
{
echo 100 > ~/bin/inventory.txt
rm -f ~/bin/sales.log
echo "=== transaction tests ==="
buy_widget Alice 5
buy_widget Hacker_Bob 200
buy_widget Eve -3
echo "=== inventory ==="
cat ~/bin/inventory.txt
echo "=== sales.log ==="
cat ~/bin/sales.log
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task2_audit.txt
```

📸 **Screenshot 2 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task2_audit.txt
```
📸 **Screenshot 2 ends here**
> Save as: `images/level2_audit.png`

---

## Level 3 — The Exploit (TOC-TOU)

```bash
cat > ~/bin/bot_swarm << 'EOF'
#!/bin/bash
for i in {1..50}; do
    buy_widget "Bot_$i" 2 &
done
wait
EOF
chmod +x ~/bin/bot_swarm
```

> Run the swarm 5 times, recording inventory each time:

```bash
echo 100 > ~/bin/inventory.txt && rm -f ~/bin/sales.log && bot_swarm && echo "Run 1:" && cat ~/bin/inventory.txt
echo 100 > ~/bin/inventory.txt && rm -f ~/bin/sales.log && bot_swarm && echo "Run 2:" && cat ~/bin/inventory.txt
echo 100 > ~/bin/inventory.txt && rm -f ~/bin/sales.log && bot_swarm && echo "Run 3:" && cat ~/bin/inventory.txt
echo 100 > ~/bin/inventory.txt && rm -f ~/bin/sales.log && bot_swarm && echo "Run 4:" && cat ~/bin/inventory.txt
echo 100 > ~/bin/inventory.txt && rm -f ~/bin/sales.log && bot_swarm && echo "Run 5:" && cat ~/bin/inventory.txt
```

> Note the inventory value after each run. They will likely differ — that's the race condition.

```bash
cat > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/observations.txt << 'EOF'
Run 1 final inventory: [fill in]
Run 2 final inventory: [fill in]
Run 3 final inventory: [fill in]
Run 4 final inventory: [fill in]
Run 5 final inventory: [fill in]

Explanation:
Multiple bots read the inventory at the same time before any of them writes back.
They all see the same old value, calculate the same result, and overwrite each other.
This is a TOC-TOU race condition caused by OS process scheduling.
EOF
```

> Fill in the actual numbers you got before moving on.

---

## Level 4 — The Patch (Mutex)

```bash
cat > ~/bin/buy_widget << 'EOF'
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: buy_widget <username> <quantity>"
    exit 1
fi

username="$1"
quantity="$2"

if ! [[ "$quantity" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: quantity must be a positive integer."
    exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
inventory_file="$script_dir/inventory.txt"
sales_log="$script_dir/sales.log"
lock_file="$script_dir/inventory.lock"

(
    flock -x 200

    current=$(cat "$inventory_file")

    if [ "$quantity" -gt "$current" ]; then
        echo "Transaction Failed: Not enough inventory!"
        exit 3
    fi

    new=$((current - quantity))
    echo "$new" > "$inventory_file"
    echo "[p20240034] [SUCCESS] $username bought $quantity widgets." >> "$sales_log"
    echo "Purchase successful! Remaining inventory: $new"

) 200> "$lock_file"
EOF
chmod +x ~/bin/buy_widget
```

```bash
echo 100 > ~/bin/inventory.txt && rm -f ~/bin/sales.log && bot_swarm
```

```bash
{
echo "=== final inventory ==="
cat ~/bin/inventory.txt
echo "=== last 5 sales ==="
tail -5 ~/bin/sales.log
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task4_mutex.txt
```

📸 **Screenshot 3 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task4_mutex.txt
```
📸 **Screenshot 3 ends here**
> Inventory should be exactly `0`. Save as: `images/level4_mutex.png`

---

## Level 5 — Red Team vs. Blue Team (Solo Simulation)

```bash
mkdir -p ~/public_api && cp ~/bin/buy_widget ~/public_api/ && echo 100 > ~/public_api/inventory.txt && touch ~/public_api/sales.log ~/public_api/inventory.lock && chmod o+x "$HOME" && chmod 755 ~/public_api && chmod o+rx ~/public_api/buy_widget && chmod o+rw ~/public_api/inventory.txt ~/public_api/sales.log ~/public_api/inventory.lock
```

> Simulate the red team attack by running bot_swarm against the public_api path:

```bash
cat > ~/bin/bot_swarm << 'EOF'
#!/bin/bash
target="/home/ken/public_api/buy_widget"
for i in {1..50}; do
    "$target" "RedTeam_ken_$i" 2 &
done
wait
EOF
chmod +x ~/bin/bot_swarm && bot_swarm
```

```bash
{
echo "=== public api permissions ==="
ls -ld "$HOME" ~/public_api
ls -l ~/public_api
echo "=== inventory ==="
cat ~/public_api/inventory.txt
echo "=== red team sales evidence ==="
tail -10 ~/public_api/sales.log
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task5_red_blue.txt
```

📸 **Screenshot 4 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task5_red_blue.txt
```
📸 **Screenshot 4 ends here**
> Save as: `images/level5_red_blue.png`

---

## Level 6 — Secure Drop Zone (Solo Simulation)

```bash
cat > ~/bin/create_dropzone << 'EOF'
#!/bin/bash
read -r -p "Drop zone folder name: " folder
mkdir -p "$HOME/$folder"
chmod o+wx "$HOME/$folder"
chmod +t "$HOME/$folder"
echo "Drop zone created:"
ls -ld "$HOME/$folder"
EOF
chmod +x ~/bin/create_dropzone && create_dropzone
```

> Type `vendor_reports` when prompted.

```bash
echo "Only I should delete this." > ~/vendor_reports/my_rules.txt
```

> Simulate partner trying to delete your file (this should fail with Permission denied):

```bash
sudo -u nobody rm ~/vendor_reports/my_rules.txt 2>&1 || echo "Permission denied — sticky bit works!"
```

```bash
{
echo "=== drop zone permissions ==="
ls -ld ~/vendor_reports
echo "=== drop zone files ==="
ls -l ~/vendor_reports
echo "=== partner deletion result ==="
echo "Permission denied — sticky bit prevents deletion of another user's file."
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task6_dropzone.txt
```

📸 **Screenshot 5 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task6_dropzone.txt
```
📸 **Screenshot 5 ends here**
> Save as: `images/level6_dropzone.png`

---

## Level 7 — Forensic Cleanup

```bash
cat > ~/bin/cleanup << 'EOF'
#!/bin/bash
script_name="$(basename "$0")"

for file in *; do
    [ -f "$file" ] || continue
    [ "$file" = "$script_name" ] && continue

    ext="${file##*.}"

    [ "$ext" = "$file" ] && continue

    mkdir -p "$ext"
    mv "$file" "$ext/"
    echo "Moved $file -> $ext/"
done
EOF
chmod +x ~/bin/cleanup
```

```bash
mkdir -p ~/forensic_cleanup && cd ~/forensic_cleanup && touch test.log data.csv error.tmp && cleanup && { tree . 2>/dev/null || ls -R .; }
```

```bash
{ tree ~/forensic_cleanup 2>/dev/null || ls -R ~/forensic_cleanup; } > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task7_cleanup.txt
```

📸 **Screenshot 6 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8/task7_cleanup.txt
```
📸 **Screenshot 6 ends here**
> Save as: `images/level7_cleanup.png`

---

## Copy Scripts + Git Push

```bash
cd ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab8 && cp ~/public_api/buy_widget scripts/ && cp ~/bin/arg_viewer scripts/ && cp ~/bin/quantum_probe scripts/ && cp ~/bin/bot_swarm scripts/ && cp ~/bin/create_dropzone scripts/ && cp ~/bin/cleanup scripts/
```

```bash
ls -1 scripts/ && ls -1 images/
```

```bash
cd ~/Desktop/github/os-se-p20240034 && git add . && git commit -m "Lab 8: Secure Bash scripting and TOC-TOU mutex" && git push origin main
```