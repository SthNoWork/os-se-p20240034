https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/labs/lab1/lab1-instruction.md

Expected:

os-se-<YourStudentID>/
└── os-lab-<YourStudentID>/
    └── lab1/
        ├── README.md
        ├── images/
        │   ├── task1.png
        │   ├── task2.png
        │   ├── task3.png
        │   ├── task4.png
        │   ├── task5.png
        │   └── task6.png
        ├── task1_os_info.txt
        ├── task2_file_commands.txt
        ├── task2_files/
        │   ├── a.txt
        │   └── b_renamed.txt
        ├── task3_apt_install.txt
        ├── task3_apt_purge.txt
        ├── task3_apt_remove.txt
        ├── task3_apt_update.txt
        ├── task3_config_after_purge.txt
        ├── task3_config_after_remove.txt
        ├── task3_verify_install.txt
        ├── task4_process_list.txt
        ├── task5_app_verify.txt
        ├── task5_multitasking.txt
        └── task6_virtualization_check.txt

Result:
hengrith@hengrith-VMware-Virtual-Platform:~/Desktop/os-se-p20240034/os-lab-p20240034/lab1$ tree
.
├── images
│   ├── task1.png
│   ├── task2.png
│   ├── task3.png
│   ├── task4.png
│   ├── task5.png
│   └── task6.png
├── README.md
├── task1_os_info.txt
├── task2_file_commands.txt
├── task2_files
│   ├── a.txt
│   └── b_renamed.txt
├── task3_apt_install.txt
├── task3_apt_purge.txt
├── task3_apt_remove.txt
├── task3_apt_update.txt
├── task3_config_after_purge.txt
├── task3_config_after_remove.txt
├── task3_verify_install.txt
├── task4_process_list.txt
├── task5_app_verify.txt
└── task6_virtualization_check.txt

Note:
task 1:
    uname — displays kernel and system information
    lsb_release — displays Ubuntu distribution details

doing a command then using ">" instead of the terminal being cluttered it will output it all to the specified .txt
example: uname -a > task1_os_info.txt

task 2:

pwd — Print Working Directory (shows your current location).
ls — List directory contents (shows files and folders).
mkdir / cd — Make a new directory / Change into a directory.
touch — Creates a new, empty file.
echo — Prints text (often redirected to insert text into a file).
cat — Concatenates and displays the contents of a file.
cp / mv / rm — Copy, Move/Rename, and Remove (delete) files

example: 
touch filename.extension filename.extension
echo "hello" > filename.extension 
(this overwrites(>) everything in the file with whatver in the "")
cat opens and copies the content output it to terminal 

cp input.txt output.txt
mv name.txt renamed.txt
rm filename.extenion

task 3:
Commands Used:

    apt-get update — refreshes the local package index from remote repositories
    apt-get install — downloads and installs a package
    apt-get remove — uninstalls a package but keeps its configuration files
    apt-get purge — uninstalls a package and removes its configuration files
    apt-get upgrade — upgrades all currently installed packages to their latest available versions
    apt list --installed — lists all packages currently installed on the system
    ls — used here to check for the existence of configuration directories


Task 4 — Programs vs Processes (Single Process)

Purpose: Demonstrate that a program becomes a running process when it is executed.

Commands Used:

    sleep — runs a program that simply pauses for a specified duration
    & — added to the end of a command to run a program in the background
    ps — lists currently running processes

Instructions:

    Run a background process:

    sleep 120 &

    Capture the list of running processes:

    ps > task4_process_list.txt

Output File: task4_process_list.txt
Task 5 — Installing Real Applications & Observing Multitasking

Purpose: Install commonly used, server-friendly CLI applications and observe multiple programs running simultaneously under the OS.

Commands Used:

    apt-get install
    python3 (built-in tool to run a background web server)

Instructions:

    Install htop (an interactive process viewer) and tmux (a terminal multiplexer):

    sudo apt-get install htop tmux -y

    Verify their installations:

    which htop tmux > task5_app_verify.txt

    Start multiple background applications to simulate a multitasking environment:

    sleep 500 &
    sleep 600 &
    python3 -m http.server 8080 &

    Capture the process list showing your simultaneous background applications:

    ps > task5_multitasking.txt

    Optional cleanup: You can stop the web server by typing kill %3 if it was the third background job.

Output Files: task5_app_verify.txt, task5_multitasking.txt
Task 6 — Virtualization and Hypervisor Detection

Purpose: Check whether the operating system is running on physical hardware or a virtual machine.

Commands Used:

    systemd-detect-virt
    lscpu
    uname, hostname

Instructions:

systemd-detect-virt > task6_virtualization_check.txt
lscpu | grep -i hypervisor >> task6_virtualization_check.txt
uname -r >> task6_virtualization_check.txt
hostname >> task6_virtualization_check.txt

Output File: task6_virtualization_check.txt

