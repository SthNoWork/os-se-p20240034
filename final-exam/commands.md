# commands.md — exact commands I ran, per part

## Part A — Threads, Mapping & Signals

```bash
cd ~/os-se-p20240034/final-exam/partA_threads

# A1 — thread_demo.c: compile with -pthread flag, run
gcc -pthread thread_demo.c -o thread_demo
./thread_demo

# A2 — capture LWP mapping while thread_demo is alive (sleep(15) added to worker())
# Terminal 1:
./thread_demo
# Terminal 2 (run while Terminal 1 is sleeping):
ps -eLf | grep thread_demo > thread_map.txt
cat thread_map.txt

# A3 — signal_demo.c: compile and run, send SIGINT via Ctrl+C
gcc signal_demo.c -o signal_demo
./signal_demo
# (Ctrl+C sent manually in terminal to trigger SIGINT handler)
```

## Part B — Permissions, Special Bits

```bash
cd ~/os-se-p20240034/final-exam/partB_security

# B1 — permission story
mkdir -p perm_demo/shared_dir
echo "this is private" > perm_demo/private_file.txt
chmod 600 perm_demo/private_file.txt
chmod 711 perm_demo/shared_dir

ls -l perm_demo/private_file.txt
ls -ld perm_demo/shared_dir
stat perm_demo/private_file.txt
stat perm_demo/shared_dir
# (output captured into perm_report.txt)

# B2 — special bits
mkdir -p perm_demo/setgid_dir
chmod g+s perm_demo/setgid_dir

mkdir -p perm_demo/sticky_dir
chmod 1777 perm_demo/sticky_dir

gcc setuid_demo.c -o setuid_demo
chmod u+s setuid_demo

ls -l perm_demo/setgid_dir perm_demo/sticky_dir setuid_demo
ls -ld perm_demo/setgid_dir perm_demo/sticky_dir
./setuid_demo
```

## Part C — Bash Scripting, PATH & Safe Scanning

```bash
cd ~/os-se-p20240034/final-exam/partC_scripting

# C1 — greeter
mkdir -p ~/bin
chmod +x ~/bin/greeter
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
which greeter
greeter
echo $PATH > path_report.txt
which greeter >> path_report.txt
cp ~/bin/greeter scripts/greeter

# C2 — collector (test data with valid, missing, and unreadable files)
mkdir -p sample_data/dir1 sample_data/dir2 sample_data/dir3
echo "Data from dir1 file A" > sample_data/dir1/fileA.txt
echo "Data from dir2 file B" > sample_data/dir2/fileB.txt
echo "Data from dir3 file C" > sample_data/dir3/fileC.txt
echo "secret data" > sample_data/dir1/locked.txt
chmod 000 sample_data/dir1/locked.txt

chmod +x ~/bin/collector
collector
cat collected_report.txt
cp ~/bin/collector scripts/collector
```

## Part D — Race Condition & flock

```bash
cd ~/os-se-p20240034/final-exam/partD_secure

# D1 — buy_reactor_core (initial unpatched version)
chmod +x ~/bin/buy_reactor_core
cp ~/bin/buy_reactor_core scripts/buy_reactor_core
echo 200 > stock.txt
buy_reactor_core Ken 5
cat stock.txt
cat sales.log

# D2 — swarm (unpatched, demonstrates race)
chmod +x ~/bin/swarm
cp ~/bin/swarm scripts/swarm

echo 200 > stock.txt
swarm
cat stock.txt
# repeated 3 times, results recorded in observations.txt: -1, -1, -1

# D3 — patch with flock (rewrote buy_reactor_core with exclusive lock around
# the read-modify-write critical section, anchored paths with $HOME)
chmod +x ~/bin/buy_reactor_core
cp ~/bin/buy_reactor_core scripts/buy_reactor_core

echo 200 > stock.txt
swarm
cat stock.txt
# patched result: 160, deterministic across multiple runs
```

## Part E — Backups & cron

```bash
cd ~/os-se-p20240034/final-exam/partE_automation

# E1 — backup_project
mkdir -p scripts sample_project/src sample_project/docs backups
echo "int main() { return 0; }" > sample_project/src/main.c
echo "Project notes" > sample_project/docs/notes.md
chmod +x ~/bin/backup_project
cp ~/bin/backup_project scripts/backup_project

for i in 1 2 3 4 5; do
  backup_project
  sleep 1
done
ls -la backups/

# E2 — timed_job + crontab (recurring + one-shot)
mkdir -p logs
touch logs/cron_recurring.log
touch logs/cron_oneshot.log
chmod +x ~/bin/timed_job
cp ~/bin/timed_job scripts/timed_job

crontab -l 2>/dev/null > ~/cron_backup.txt
crontab -e
# added:
# * * * * * /home/se-lor-hengrith/bin/timed_job /home/se-lor-hengrith/os-se-p20240034/final-exam/partE_automation/logs/cron_recurring.log
# 35 14 30 6 * /home/se-lor-hengrith/bin/timed_job /home/se-lor-hengrith/os-se-p20240034/final-exam/partE_automation/logs/cron_oneshot.log
crontab -l

# E3 — backup_exam + crontab (short interval + 16:00 one-shot)
mkdir -p ~/exam-backups
chmod +x ~/bin/backup_exam
cp ~/bin/backup_exam scripts/backup_exam

backup_exam
ls -la ~/exam-backups/

crontab -e
# added:
# */5 * * * * /home/se-lor-hengrith/bin/backup_exam >> .../logs/backup_exam.log 2>&1
# 0 16 30 6 * /home/se-lor-hengrith/bin/backup_exam >> .../logs/backup_exam.log 2>&1
crontab -l

# wait for 14:35 and 16:00 entries to fire, then:
cat logs/cron_recurring.log
cat logs/cron_oneshot.log
cat logs/backup_exam.log
ls -la ~/exam-backups/
# all captured into cron_report.txt
```