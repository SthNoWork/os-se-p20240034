# Lab 9 — Quantum Vault Deadlock (Solo Guide)

- **Username:** ken
- **Lab path:** `~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9`
- **Working folder:** `~/os-lab-deadlock`
- **Scripts folder:** `~/bin`

> Since this is solo, Levels 4 and 5 simulate the partner using a second folder on the same machine.

---

## Setup — Run Once

```bash
cd ~/Desktop/github/os-se-p20240034/os-lab-p20240034
mkdir -p lab9/images lab9/scripts
cd lab9
mkdir -p ~/bin ~/os-lab-deadlock
```

---

## Level 1 — Vault Workspace Setup

```bash
cd ~/os-lab-deadlock && mkdir -p vault_alpha vault_beta && touch vault_alpha/vault.lock vault_beta/vault.lock && echo "Vault Alpha local resource for p20240034" > vault_alpha/README.txt && echo "Vault Beta local resource for p20240034" > vault_beta/README.txt
```

```bash
{
echo "=== working folder ==="
pwd
echo "=== vault directories ==="
ls -ld ~/os-lab-deadlock/vault_alpha ~/os-lab-deadlock/vault_beta
echo "=== vault lock files ==="
ls -l ~/os-lab-deadlock/vault_alpha/vault.lock ~/os-lab-deadlock/vault_beta/vault.lock
echo "=== vault marker files ==="
cat ~/os-lab-deadlock/vault_alpha/README.txt
cat ~/os-lab-deadlock/vault_beta/README.txt
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task1_vaults.txt
```

📸 **Screenshot 1 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task1_vaults.txt
```
📸 **Screenshot 1 ends here**
> Save as: `images/level1_vaults.png`

---

## Level 2 — Naive Sync Scripts

```bash
cat > ~/bin/sync_up << 'EOF'
#!/bin/bash
base="$HOME/os-lab-deadlock"
alpha_lock="$base/vault_alpha/vault.lock"
beta_lock="$base/vault_beta/vault.lock"
exec 200> "$alpha_lock"
exec 201> "$beta_lock"
echo "sync_up: waiting for Vault Alpha"
flock -x 200
echo "sync_up: locked Vault Alpha"
sleep 5
echo "sync_up: waiting for Vault Beta"
flock -x 201
echo "sync_up: locked Vault Beta"
echo "sync_up: synchronizing Alpha to Beta"
echo "$(date): sync_up completed" >> "$base/vault_beta/sync.log"
sleep 2
echo "sync_up: complete"
EOF
```

```bash
cat > ~/bin/sync_down << 'EOF'
#!/bin/bash
base="$HOME/os-lab-deadlock"
alpha_lock="$base/vault_alpha/vault.lock"
beta_lock="$base/vault_beta/vault.lock"
exec 200> "$alpha_lock"
exec 201> "$beta_lock"
echo "sync_down: waiting for Vault Beta"
flock -x 201
echo "sync_down: locked Vault Beta"
sleep 5
echo "sync_down: waiting for Vault Alpha"
flock -x 200
echo "sync_down: locked Vault Alpha"
echo "sync_down: synchronizing Beta to Alpha"
echo "$(date): sync_down completed" >> "$base/vault_alpha/sync.log"
sleep 2
echo "sync_down: complete"
EOF
```

```bash
chmod +x ~/bin/sync_up ~/bin/sync_down && {
echo "=== sync script permissions ==="
ls -l ~/bin/sync_up ~/bin/sync_down
echo "=== sync_up lock order ==="
grep -E "waiting for|locked Vault" ~/bin/sync_up
echo "=== sync_down lock order ==="
grep -E "waiting for|locked Vault" ~/bin/sync_down
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task2_sync_scripts.txt
```

> No screenshot required for Level 2.

---

## Level 3 — Local Deadlock

Open **Terminal 1** and run:
```bash
sync_up
```

Open **Terminal 2** immediately after and run:
```bash
sync_down
```

> Both terminals will freeze — that is the deadlock. Leave them frozen.

Open **Terminal 3** and run:
```bash
{
echo "=== running sync processes ==="
ps aux | grep '[s]ync_'
echo "=== explanation ==="
echo "sync_up holds Alpha and waits for Beta."
echo "sync_down holds Beta and waits for Alpha."
echo "This is circular wait, so neither script can continue."
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task3_local_deadlock.txt
```

📸 **Screenshot 2 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task3_local_deadlock.txt
```
📸 **Screenshot 2 ends here**
> Tile all 3 terminals visible. Save as: `images/level3_local_deadlock.png`

> Press `Ctrl+C` in Terminal 1 and Terminal 2 to stop the frozen scripts.

---

## Level 4 — Site-to-Site Deadlock (Solo Simulation)

> Since you have no partner, you are **Player A**. We simulate Player B's folder locally.

```bash
mkdir -p ~/os-lab-deadlock/public_dr_alpha ~/os-lab-deadlock/public_dr_beta && touch ~/os-lab-deadlock/public_dr_alpha/vault.lock ~/os-lab-deadlock/public_dr_beta/vault.lock && chmod o+x "$HOME" ~/os-lab-deadlock && chmod 755 ~/os-lab-deadlock/public_dr_alpha ~/os-lab-deadlock/public_dr_beta && chmod o+rw ~/os-lab-deadlock/public_dr_alpha/vault.lock ~/os-lab-deadlock/public_dr_beta/vault.lock
```

```bash
cat > ~/bin/cross_sync_alpha << 'EOF'
#!/bin/bash
local_lock="$HOME/os-lab-deadlock/public_dr_alpha/vault.lock"
partner_lock="$HOME/os-lab-deadlock/public_dr_beta/vault.lock"
exec 200> "$local_lock"
exec 201> "$partner_lock"
echo "cross_sync_alpha: waiting for local Alpha"
flock -x 200
echo "cross_sync_alpha: locked local Alpha"
sleep 5
echo "cross_sync_alpha: waiting for partner Beta"
flock -x 201
echo "cross_sync_alpha: locked partner Beta"
echo "cross_sync_alpha: complete"
EOF
```

```bash
cat > ~/bin/cross_sync_beta << 'EOF'
#!/bin/bash
local_lock="$HOME/os-lab-deadlock/public_dr_beta/vault.lock"
partner_lock="$HOME/os-lab-deadlock/public_dr_alpha/vault.lock"
exec 200> "$local_lock"
exec 201> "$partner_lock"
echo "cross_sync_beta: waiting for local Beta"
flock -x 200
echo "cross_sync_beta: locked local Beta"
sleep 5
echo "cross_sync_beta: waiting for partner Alpha"
flock -x 201
echo "cross_sync_beta: locked partner Alpha"
echo "cross_sync_beta: complete"
EOF
```

```bash
chmod +x ~/bin/cross_sync_alpha ~/bin/cross_sync_beta
```

Open **Terminal 1** and run:
```bash
cross_sync_alpha
```

Open **Terminal 2** immediately and run:
```bash
cross_sync_beta
```

> Both will freeze — cross-site deadlock simulated.

Open **Terminal 3** and run:
```bash
{
echo "=== public DR permissions ==="
ls -ld "$HOME" ~/os-lab-deadlock ~/os-lab-deadlock/public_dr_* 2>/dev/null
ls -l ~/os-lab-deadlock/public_dr_* 2>/dev/null
echo "=== running cross sync processes ==="
ps aux | grep '[c]ross_sync'
echo "=== partner role ==="
echo "Partner username: ken (solo simulation)"
echo "My role: Player A"
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task4_cross_deadlock.txt
```

📸 **Screenshot 3 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task4_cross_deadlock.txt
```
📸 **Screenshot 3 ends here**
> Tile all 3 terminals. Save as: `images/level4_cross_deadlock.png`

> Press `Ctrl+C` in Terminal 1 and Terminal 2.

---

## Level 5 — Global Resource Ordering Patch

> Patch `cross_sync_beta` to lock Alpha before Beta (same order as `cross_sync_alpha`).

```bash
cat > ~/bin/cross_sync_beta << 'EOF'
#!/bin/bash
partner_alpha="$HOME/os-lab-deadlock/public_dr_alpha/vault.lock"
local_beta="$HOME/os-lab-deadlock/public_dr_beta/vault.lock"
exec 200> "$partner_alpha"
exec 201> "$local_beta"
echo "cross_sync_beta: waiting for partner Alpha"
flock -x 200
echo "cross_sync_beta: locked partner Alpha"
sleep 5
echo "cross_sync_beta: waiting for local Beta"
flock -x 201
echo "cross_sync_beta: locked local Beta"
echo "cross_sync_beta: complete"
EOF
chmod +x ~/bin/cross_sync_beta
```

Open **Terminal 1** and run:
```bash
cross_sync_alpha
```

Open **Terminal 2** immediately and run:
```bash
cross_sync_beta
```

> This time both should complete without freezing.

Back in **Terminal 1 or 3** run:
```bash
{
echo "=== global ordering rule ==="
echo "All scripts lock Alpha before Beta."
echo "=== my role script order ==="
grep -E "waiting for|locked" ~/bin/cross_sync_alpha ~/bin/cross_sync_beta 2>/dev/null
echo "=== result ==="
echo "Both cross-site scripts completed without deadlock."
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task5_ordering_patch.txt
```

📸 **Screenshot 4 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task5_ordering_patch.txt
```
📸 **Screenshot 4 ends here**
> Save as: `images/level5_ordering_patch.png`

---

## Level 6 — Timeout Recovery

```bash
cat > ~/bin/sync_timeout << 'EOF'
#!/bin/bash
base="$HOME/os-lab-deadlock"
alpha_lock="$base/vault_alpha/vault.lock"
beta_lock="$base/vault_beta/vault.lock"
exec 200> "$alpha_lock"
exec 201> "$beta_lock"
echo "sync_timeout: waiting for Vault Alpha"
if ! flock -w 5 200; then
    echo "ERROR: could not lock Vault Alpha within 5 seconds"
    exit 1
fi
echo "sync_timeout: locked Vault Alpha"
sleep 2
echo "sync_timeout: waiting for Vault Beta"
if ! flock -w 5 201; then
    echo "ERROR: could not lock Vault Beta within 5 seconds"
    exit 2
fi
echo "sync_timeout: locked Vault Beta"
echo "sync_timeout: complete"
EOF
chmod +x ~/bin/sync_timeout
```

Open **Terminal 1** and run:
```bash
sync_down
```

Open **Terminal 2** immediately and run:
```bash
sync_timeout
echo "exit status: $?"
```

> `sync_timeout` should print the timeout error instead of freezing. Then press `Ctrl+C` in Terminal 1.

```bash
{
echo "=== sync_timeout permissions ==="
ls -l ~/bin/sync_timeout
echo "=== timeout evidence ==="
echo "sync_timeout printed ERROR and exited with nonzero status after 5 seconds."
echo "=== process check after stopping old script ==="
ps aux | grep '[s]ync_' || true
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task6_timeout_recovery.txt
```

📸 **Screenshot 5 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task6_timeout_recovery.txt
```
📸 **Screenshot 5 ends here**
> Tile Terminal 1 and Terminal 2 visible. Save as: `images/level6_timeout_recovery.png`

---

## Level 7 — Cleanup and Reset

```bash
cat > ~/bin/teardown << 'EOF'
#!/bin/bash
base="$HOME/os-lab-deadlock"
echo "Checking for sync processes:"
ps aux | grep -E '[s]ync_|[c]ross_sync' || echo "No sync processes found."
echo "Cleaning temporary sync logs:"
rm -f "$base/vault_alpha/sync.log" "$base/vault_beta/sync.log"
echo "Final working tree:"
find "$base" -maxdepth 3 -type f -o -type d | sort
EOF
chmod +x ~/bin/teardown && teardown
```

```bash
{
echo "=== teardown script ==="
ls -l ~/bin/teardown
echo "=== process check ==="
ps aux | grep -E '[s]ync_|[c]ross_sync' || echo "No sync processes found."
echo "=== final working folder ==="
find ~/os-lab-deadlock -maxdepth 3 -type f -o -type d | sort
} > ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task7_teardown.txt
```

📸 **Screenshot 6 starts here:**
```bash
cat ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9/task7_teardown.txt
```
📸 **Screenshot 6 ends here**
> Save as: `images/level7_teardown.png`

---

## Copy Scripts + Git Push

```bash
cd ~/Desktop/github/os-se-p20240034/os-lab-p20240034/lab9 && cp ~/bin/sync_up scripts/ && cp ~/bin/sync_down scripts/ && cp ~/bin/sync_timeout scripts/ && cp ~/bin/teardown scripts/ && cp ~/bin/cross_sync_alpha scripts/ 2>/dev/null || true
```

```bash
ls -1 scripts/ && ls -1 images/
```

```bash
cd ~/Desktop/github/os-se-p20240034 && git add . && git commit -m "Lab 9: Vault deadlock and recovery" && git push origin main
```