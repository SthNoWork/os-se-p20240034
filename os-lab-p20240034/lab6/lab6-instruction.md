# OS Lab 6 — Linux Security, Users, Groups & File Permissions (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Linux Security: Users, Groups & File Permissions |
| **Chapter** | File Systems, OS Security & Access Control |
| **Duration** | 3 Hours |
| **Lab Type** | Individual |

---

> ⚠️ **IMPORTANT — READ EVERYTHING FIRST**
>
> **Before you type a single command, read through this ENTIRE document from top to bottom.**
> Understand the full scope of what is expected **before** you start working.

---

## Lab Objectives

After completing this lab, students will be able to:

1. Create, modify, and delete Linux user accounts using `useradd`, `usermod`, and `userdel`.
2. Create and manage user groups using `groupadd`, `groupmod`, and `gpasswd`.
3. Interpret and modify file and directory permissions using `chmod` (symbolic and octal notation).
4. Change file ownership using `chown` and `chgrp`.
5. Understand and apply special permission bits: `setuid`, `setgid`, and the sticky bit.
6. Use `sudo` for privilege escalation and audit the sudoers configuration safely.
7. Apply Access Control Lists (ACLs) with `getfacl` and `setfacl` for fine-grained permission control.

> **Scenario:** You are **Alex**, a junior systems engineer at **TechCorp Inc.** Your manager says: *"We're onboarding a new project team. I need you to set up user accounts and groups, lock down sensitive directories, and make sure that no one can accidentally delete each other's files. Security is our top priority — get it right."*

---

## Task Overview

| Task | Title | Key Commands | Screenshots Required |
|:---:|-------|-------------|:-----------:|
| **1** | User Account Management | `useradd`, `passwd`, `usermod`, `userdel` | ✅ (User creation & verification) |
| **2** | Group Management | `groupadd`, `gpasswd`, `id`, `groups` | ✅ (Group setup & membership) |
| **3** | File & Directory Permissions | `chmod`, `chown`, `chgrp`, `ls -l` | ✅ (Permission changes) |
| **4** | Special Permission Bits | `setuid`, `setgid`, sticky bit | ✅ (Special bits in action) |
| **5** | Access Control Lists (ACLs) | `getfacl`, `setfacl` | ✅ (ACL configuration) |

---

## Lab Setup

Navigate into your existing lab submission repository and create the required directory structure **all at once**:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>

# Create lab6 and all required subdirectories in one command
mkdir -p lab6/security_lab lab6/images

cd lab6
```

> ✅ This creates:
> ```
> lab6/
> ├── security_lab/
> └── images/
> ```

### Documenting Your Work

1. **Screenshots:** All tasks require screenshots as proof of execution.
2. **Save All Images:** Save all screenshots to the `images/` folder inside your `lab6` directory.  
   Name them **exactly** as listed in the Screenshot Checklist below.
3. **Output Files:** The commands in each task will redirect output into `.txt` files automatically.

> ⚠️ **All commands in Tasks 1–5 must be run from inside the `lab6/` directory**, unless a task explicitly says to `cd` elsewhere.

---

## Quick Reference

### User & Group Management

| Command | Purpose |
|---------|---------|
| `useradd -m -s /bin/bash <name>` | Create a user with home directory and bash shell |
| `passwd <name>` | Set or change a user's password |
| `usermod -aG <group> <user>` | Add a user to a supplementary group |
| `usermod -l <newname> <oldname>` | Rename a user account |
| `userdel -r <name>` | Delete a user and their home directory |
| `groupadd <group>` | Create a new group |
| `groupmod -n <newname> <oldname>` | Rename a group |
| `gpasswd -d <user> <group>` | Remove a user from a group |
| `id <user>` | Show UID, GID, and supplementary groups |
| `groups <user>` | List all groups a user belongs to |

### Permission & Ownership

| Command | Purpose |
|---------|---------|
| `ls -l` | Long listing showing permissions, owner, group |
| `chmod 755 <file>` | Set permissions using octal notation |
| `chmod u+x <file>` | Add execute for owner (symbolic) |
| `chown user:group <file>` | Change owner and group |
| `chgrp <group> <file>` | Change group only |
| `umask` | Show/set default permission mask |

### Special Bits

| Bit | Octal | Effect on File | Effect on Directory |
|-----|-------|---------------|---------------------|
| `setuid` | `4xxx` | Run as file owner | — |
| `setgid` | `2xxx` | Run as file group | New files inherit group |
| Sticky | `1xxx` | — | Only owner can delete own files |

### Key Files

| File | Purpose |
|------|---------|
| `/etc/passwd` | User account database |
| `/etc/shadow` | Hashed passwords (root-readable only) |
| `/etc/group` | Group database |
| `/etc/sudoers` | Sudo privilege configuration (edit with `visudo`) |

---

## Task 1 — User Account Management

**Scenario:** *"We have two new engineers joining the project: `dev_alice` and `dev_bob`. Create their accounts, set passwords, and verify the accounts are properly configured."*

> ⚠️ **Make sure you are in `lab6/` before running these commands.**

**Instructions:**

1. Create two new user accounts:
   ```bash
   sudo useradd -m -s /bin/bash dev_alice
   sudo useradd -m -s /bin/bash dev_bob
   ```

2. Set passwords for both users:
   ```bash
   sudo passwd dev_alice
   sudo passwd dev_bob
   ```
   > Use a simple password like `Password123` for this lab exercise.

3. Verify accounts and home directories, then **save to `task1_users.txt`**:
   ```bash
   grep "dev_alice\|dev_bob" /etc/passwd > task1_users.txt
   ls -la /home/ | grep "dev_alice\|dev_bob" >> task1_users.txt
   cat task1_users.txt
   ```

   > 📸 **Screenshot 1:** Take a screenshot of the `cat task1_users.txt` output.  
   > Save as `images/task1_user_creation.png`.

4. Modify `dev_alice` — add a GECOS comment field with her full name:
   ```bash
   sudo usermod -c "Alice Developer" dev_alice
   grep dev_alice /etc/passwd
   ```

   > 📸 **Screenshot 2:** Take a screenshot showing the updated `/etc/passwd` entry for `dev_alice`.  
   > Save as `images/task1_user_modify.png`.

---

## Task 2 — Group Management

**Scenario:** *"The two new engineers belong to the `devteam` group. Create it, add them both, and then verify the memberships."*

> ⚠️ **Make sure you are in `lab6/` before running these commands.**

**Instructions:**

1. Create a new group called `devteam`:
   ```bash
   sudo groupadd devteam
   ```

2. Add both users to the group:
   ```bash
   sudo usermod -aG devteam dev_alice
   sudo usermod -aG devteam dev_bob
   ```

3. Verify group membership, then **save to `task2_groups.txt`**:
   ```bash
   groups dev_alice > task2_groups.txt
   id dev_bob >> task2_groups.txt
   grep devteam /etc/group >> task2_groups.txt
   cat task2_groups.txt
   ```

   > 📸 **Screenshot 3:** Take a screenshot of `cat task2_groups.txt`.  
   > Save as `images/task2_group_setup.png`.

4. Create an additional group `auditors` and add only `dev_alice`:
   ```bash
   sudo groupadd auditors
   sudo usermod -aG auditors dev_alice
   id dev_alice
   ```

   > 📸 **Screenshot 4:** Take a screenshot of `id dev_alice` showing both `devteam` and `auditors`.  
   > Save as `images/task2_multi_group.png`.

---

## Task 3 — File & Directory Permissions

**Scenario:** *"Create a shared project directory for the `devteam` group. Set up permissions so that only team members can read and write files, but others cannot access the folder at all."*

> ⚠️ **Make sure you are in `lab6/` before running these commands.**

**Instructions:**

1. Create the shared project directory and set ownership/permissions:
   ```bash
   sudo mkdir -p /opt/techcorp/devproject
   sudo chown root:devteam /opt/techcorp/devproject
   sudo chmod 770 /opt/techcorp/devproject
   ls -ld /opt/techcorp/devproject
   ```

2. Create a test file inside the directory:
   ```bash
   sudo touch /opt/techcorp/devproject/project_notes.txt
   sudo chown dev_alice:devteam /opt/techcorp/devproject/project_notes.txt
   sudo chmod 664 /opt/techcorp/devproject/project_notes.txt
   ls -l /opt/techcorp/devproject/
   ```

3. **Save permissions output to `task3_permissions.txt`**:
   ```bash
   ls -ld /opt/techcorp/devproject > task3_permissions.txt
   ls -l /opt/techcorp/devproject/ >> task3_permissions.txt
   cat task3_permissions.txt
   ```

   > 📸 **Screenshot 5:** Take a screenshot of `cat task3_permissions.txt`.  
   > Save as `images/task3_dir_permissions.png`.

4. **Save `stat` output to `task3_stat_output.txt`**:
   ```bash
   stat /opt/techcorp/devproject > task3_stat_output.txt
   cat task3_stat_output.txt
   ```

5. Test access control — create a user not in `devteam` and verify access is denied:
   ```bash
   sudo useradd -m -s /bin/bash temp_user
   sudo su - temp_user -c "cat /opt/techcorp/devproject/project_notes.txt"
   ```
   > **Expected:** `Permission denied` — because `temp_user` is not in `devteam`.

   > 📸 **Screenshot 6:** Take a screenshot showing the `Permission denied` error.  
   > Save as `images/task3_access_denied.png`.

---

## Task 4 — Special Permission Bits

**Scenario:** *"Configure the shared directory so that new files automatically inherit the group ownership (`setgid`), and no one can delete another user's files (sticky bit)."*

> ⚠️ **Make sure you are in `lab6/` before running these commands.**

**Instructions:**

1. Apply the `setgid` bit to the shared directory:
   ```bash
   sudo chmod g+s /opt/techcorp/devproject
   ls -ld /opt/techcorp/devproject
   ```
   > **Observe:** The group execute bit changes from `x` to `s`.

2. Test `setgid` — switch to `dev_bob` and create a file:
   ```bash
   sudo su - dev_bob -c "touch /opt/techcorp/devproject/bob_file.txt"
   ls -l /opt/techcorp/devproject/
   ```
   > **Observe:** `bob_file.txt` should have `devteam` as its group (inherited from the directory).

   > 📸 **Screenshot 7:** Take a screenshot showing the setgid directory listing and `bob_file.txt` with the `devteam` group.  
   > Save as `images/task4_setgid.png`.

3. Apply the **sticky bit** to the directory:
   ```bash
   sudo chmod +t /opt/techcorp/devproject
   ls -ld /opt/techcorp/devproject
   ```
   > **Observe:** The others execute bit shows `t`.

4. Test the sticky bit — `dev_bob` should NOT be able to delete `dev_alice`'s file:
   ```bash
   sudo su - dev_bob -c "rm /opt/techcorp/devproject/project_notes.txt"
   ```
   > **Expected:** `Operation not permitted`

   > 📸 **Screenshot 8:** Take a screenshot showing the `t` bit in `ls -ld` and the `Operation not permitted` error.  
   > Save as `images/task4_sticky_bit.png`.

5. Create the `setuid` C program — **go into `security_lab/` first**:
   ```bash
   cd security_lab
   ```

   Create `whoami_suid.c`:
   ```bash
   cat > whoami_suid.c << 'EOF'
   #include <stdio.h>
   #include <unistd.h>

   int main() {
       printf("Real UID:      %d\n", getuid());
       printf("Effective UID: %d\n", geteuid());
       printf("Running as:    ");
       fflush(stdout);
       execlp("whoami", "whoami", NULL);
       return 0;
   }
   EOF
   ```

6. Compile, set ownership, and apply `setuid`:
   ```bash
   gcc -o whoami_suid whoami_suid.c
   sudo chown root:root whoami_suid
   sudo chmod u+s whoami_suid
   ls -l whoami_suid
   ```
   > **Observe:** The owner execute bit shows `s` (setuid active).

7. Run the program as `dev_alice`:
   ```bash
   sudo su - dev_alice -c "$(pwd)/whoami_suid"
   ```
   > The effective UID will be `0` (root) while the real UID is `dev_alice`'s UID.

   > 📸 **Screenshot 9:** Take a screenshot showing `ls -l whoami_suid` with the setuid bit and the program's UID output.  
   > Save as `images/task4_setuid.png`.

8. **Return to `lab6/` and save summary to `task4_special_bits.txt`**:
   ```bash
   cd ..
   ls -ld /opt/techcorp/devproject > task4_special_bits.txt
   ls -l security_lab/whoami_suid >> task4_special_bits.txt
   cat task4_special_bits.txt
   ```

---

## Task 5 — Access Control Lists (ACLs)

**Scenario:** *"The `auditors` group needs read-only access to the project directory — but we cannot change the primary group. Use ACLs to grant fine-grained access without modifying standard permissions."*

> ⚠️ **Make sure you are in `lab6/` before running these commands.**

**Instructions:**

1. Check current ACL state:
   ```bash
   getfacl /opt/techcorp/devproject
   ```

2. Grant the `auditors` group read and execute access via ACL:
   ```bash
   sudo setfacl -m g:auditors:rx /opt/techcorp/devproject
   sudo setfacl -m g:auditors:r /opt/techcorp/devproject/project_notes.txt
   ```

3. View the resulting ACL:
   ```bash
   getfacl /opt/techcorp/devproject
   getfacl /opt/techcorp/devproject/project_notes.txt
   ```
   > **Observe:** You will see `group:auditors:r-x` ACE entries.

   > 📸 **Screenshot 10:** Take a screenshot of `getfacl /opt/techcorp/devproject`.  
   > Save as `images/task5_acl_dir.png`.

4. Test ACL access — `dev_alice` (in `auditors`) should succeed, `temp_user` should be denied:
   ```bash
   sudo su - dev_alice -c "cat /opt/techcorp/devproject/project_notes.txt"
   sudo su - temp_user -c "ls /opt/techcorp/devproject"
   ```
   > `dev_alice` succeeds (file may be empty, but no error). `temp_user` gets `Permission denied`.

   > 📸 **Screenshot 11:** Take a screenshot showing both results side by side.  
   > Save as `images/task5_acl_test.png`.

5. **Save ACL output to `task5_acl.txt`**:
   ```bash
   getfacl /opt/techcorp/devproject > task5_acl.txt
   getfacl /opt/techcorp/devproject/project_notes.txt >> task5_acl.txt
   cat task5_acl.txt
   ```

   > 📸 **Screenshot 12:** Take a screenshot of `cat task5_acl.txt`.  
   > Save as `images/task5_acl_output.png`.

6. Clean up the ACL entry:
   ```bash
   sudo setfacl -x g:auditors /opt/techcorp/devproject
   getfacl /opt/techcorp/devproject
   ```

---

## Challenge — Secure Shared Drop-Box

> ⭐ **Bonus Challenge (10 extra points)**

**Scenario:** *"Create a `/opt/techcorp/dropbox` directory that behaves like a shared drop-box: any user can create files inside, but no user can read or delete another user's files."*

**Requirements:**

1. Create `/opt/techcorp/dropbox` with `devteam` as the group owner.
2. Set permissions so all `devteam` members can write into it, but cannot read or delete others' files.
3. Apply both `setgid` and the sticky bit in a single `chmod` call.
4. Test by:
   - Switching to `dev_alice` and creating a file.
   - Switching to `dev_bob` and attempting to delete `dev_alice`'s file (should fail).
   - Verifying `dev_bob` can create his own file.
5. Document with screenshots and redirect output to `challenge_dropbox.txt`.

> 📸 **Challenge Screenshot:** Show the final `ls -ld /opt/techcorp/dropbox` and the failed deletion attempt. Save as `images/challenge_dropbox.png`.

---

## Screenshot Checklist

Before submitting, verify you have **all** required screenshots in your `images/` folder:

| # | File Name | Task | What It Shows |
|:-:|-----------|:----:|---------------|
| 1 | `task1_user_creation.png` | Task 1 | Output of `cat task1_users.txt` |
| 2 | `task1_user_modify.png` | Task 1 | Updated `/etc/passwd` entry for `dev_alice` |
| 3 | `task2_group_setup.png` | Task 2 | `cat task2_groups.txt` output |
| 4 | `task2_multi_group.png` | Task 2 | `id dev_alice` with both `devteam` and `auditors` |
| 5 | `task3_dir_permissions.png` | Task 3 | `cat task3_permissions.txt` with `drwxrwx---` |
| 6 | `task3_access_denied.png` | Task 3 | `Permission denied` error from `temp_user` |
| 7 | `task4_setgid.png` | Task 4 | Directory listing with `s` bit + `bob_file.txt` |
| 8 | `task4_sticky_bit.png` | Task 4 | `t` bit in listing + `Operation not permitted` |
| 9 | `task4_setuid.png` | Task 4 | `s` bit on `whoami_suid` + UID output |
| 10 | `task5_acl_dir.png` | Task 5 | `getfacl` showing `auditors` ACE |
| 11 | `task5_acl_test.png` | Task 5 | `dev_alice` succeeds, `temp_user` denied |
| 12 | `task5_acl_output.png` | Task 5 | `cat task5_acl.txt` |

---

## Answers to Lab Questions

Fill these in your `README.md` before submitting:

1. **What is the difference between `userdel` and `userdel -r`?**

2. **Why is it safer to use `visudo` instead of directly editing `/etc/sudoers`?**

3. **What happens when a `setgid` directory contains files created by different users? What benefit does this provide for team collaboration?**

4. **What limitation of standard Unix permissions does the ACL system solve?**

---

## Final Submission

### Verify Your Folder Structure

After completing all tasks, your `lab6/` folder should look exactly like this:

```
os-se-<YourStudentID>/
└── os-lab-<YourStudentID>/
    └── lab6/
        ├── README.md
        ├── task1_users.txt              ← created in Task 1, step 3
        ├── task2_groups.txt             ← created in Task 2, step 3
        ├── task3_permissions.txt        ← created in Task 3, step 3
        ├── task3_stat_output.txt        ← created in Task 3, step 4
        ├── task4_special_bits.txt       ← created in Task 4, step 8
        ├── task5_acl.txt                ← created in Task 5, step 5
        ├── security_lab/
        │   └── whoami_suid.c            ← created in Task 4, step 5
        └── images/
            ├── task1_user_creation.png
            ├── task1_user_modify.png
            ├── task2_group_setup.png
            ├── task2_multi_group.png
            ├── task3_dir_permissions.png
            ├── task3_access_denied.png
            ├── task4_setgid.png
            ├── task4_sticky_bit.png
            ├── task4_setuid.png
            ├── task5_acl_dir.png
            ├── task5_acl_test.png
            └── task5_acl_output.png
```

You can quickly verify your `.txt` files are all present:
```bash
ls -1 ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab6/*.txt
```

### Git Push

```bash
cd ~/os-se-<YourStudentID>
git add .
git commit -m "Lab 6: Linux Security, Users, Groups & File Permissions"
git push origin main
```