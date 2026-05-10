# Class Activity 4 — Shared File API: C++ Mutex & Java synchronized

> **Topics:** Race conditions, shared files, C++ `std::mutex`, Java `synchronized`
> **Environment:** Two machines on the same network, with `g++` and Java JDK

---

## Overview

One student's machine runs the **server**. Both students run **client** programs
at the same time. The server is the only program that touches `shared_score.txt`.

You run each server in two versions:
1. **Before** synchronization — race condition can happen
2. **After** synchronization — C++ uses `std::mutex`, Java uses `synchronized`

---

## Setup — Run Once on the Server Machine

```bash
cd ~/Desktop/github/os-se-p20240034/os-class-activities-p20240034
mkdir -p activity4/{cpp_before,cpp_after,java_before,java_after,screenshots}
cd activity4
echo 0 > shared_score.txt
```

Set your activity path as a variable (re-run this in every new terminal):
```bash
ACT4=~/Desktop/github/os-se-p20240034/os-class-activities-p20240034/activity4
```

Get the server IP — **share this with your partner**:
```bash
hostname -I
```

> Write down the IP. Replace `<SERVER_IP>` in every client command with the real IP.

---

## Task 1 — C++ Server Before Mutex

### Server Machine: Create the files

```bash
cat > $ACT4/cpp_before/server_no_mutex.cpp << 'EOF'
#include <arpa/inet.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <thread>
#include <unistd.h>

const int PORT = 9001;
const std::string FILE_NAME = "shared_score.txt";

int update_score(const std::string& name) {
    std::ifstream input(FILE_NAME);
    int score = 0;
    input >> score;
    input.close();

    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    score++;

    std::ofstream output(FILE_NAME);
    output << score << std::endl;
    output.close();

    std::cout << name << " updated score to " << score << std::endl;
    return score;
}

void handle_client(int client_socket) {
    char buffer[1024] = {0};
    read(client_socket, buffer, sizeof(buffer) - 1);

    std::string name = buffer;
    int score = update_score(name);
    std::string reply = "Score is now " + std::to_string(score) + "\n";

    send(client_socket, reply.c_str(), reply.size(), 0);
    close(client_socket);
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (sockaddr*)&address, sizeof(address));
    listen(server_fd, 20);

    std::cout << "C++ no-mutex server running on port " << PORT << std::endl;

    while (true) {
        int client_socket = accept(server_fd, nullptr, nullptr);
        std::thread(handle_client, client_socket).detach();
    }
}
EOF
```

```bash
cat > $ACT4/cpp_before/client.cpp << 'EOF'
#include <arpa/inet.h>
#include <iostream>
#include <string>
#include <unistd.h>

const int PORT = 9001;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: ./client <server_ip> <student_name>" << std::endl;
        return 1;
    }

    std::string server_ip = argv[1];
    std::string name = argv[2];

    int sock = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in server{};
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    inet_pton(AF_INET, server_ip.c_str(), &server.sin_addr);

    connect(sock, (sockaddr*)&server, sizeof(server));
    send(sock, name.c_str(), name.size(), 0);

    char buffer[1024] = {0};
    read(sock, buffer, sizeof(buffer) - 1);
    std::cout << buffer;

    close(sock);
    return 0;
}
EOF
```

### Server Machine: Compile and start the server

```bash
cd $ACT4
echo 0 > shared_score.txt
g++ -std=c++17 cpp_before/server_no_mutex.cpp -o cpp_before/server_no_mutex -pthread
./cpp_before/server_no_mutex
```

> Leave this terminal running. Open a new terminal for the client.

### Student A — run clients (replace `<SERVER_IP>`):

```bash
cd $ACT4
g++ -std=c++17 cpp_before/client.cpp -o cpp_before/client
for i in {1..10}; do ./cpp_before/client <SERVER_IP> A_$i & done
wait
```

### Student B — run at the same time (replace `<SERVER_IP>`):

```bash
cd $ACT4
g++ -std=c++17 cpp_before/client.cpp -o cpp_before/client
for i in {1..10}; do ./cpp_before/client <SERVER_IP> B_$i & done
wait
```

---

📸 **Screenshot 1 starts here** — on the server machine:
```bash
cat $ACT4/shared_score.txt
```
📸 **Screenshot 1 ends here**
> Capture all 3 terminals (server + both clients) in one screenshot.
> Save as: `screenshots/cpp_before_mutex.png`

---

Stop the server with `Ctrl+C`, then reset:
```bash
echo 0 > $ACT4/shared_score.txt
```

---

## Task 2 — C++ Server After Mutex

### Server Machine: Create the files

```bash
cat > $ACT4/cpp_after/server_mutex.cpp << 'EOF'
#include <arpa/inet.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <unistd.h>

const int PORT = 9002;
const std::string FILE_NAME = "shared_score.txt";
std::mutex file_mutex;

int update_score(const std::string& name) {
    std::lock_guard<std::mutex> lock(file_mutex);

    std::ifstream input(FILE_NAME);
    int score = 0;
    input >> score;
    input.close();

    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    score++;

    std::ofstream output(FILE_NAME);
    output << score << std::endl;
    output.close();

    std::cout << name << " updated score to " << score << std::endl;
    return score;
}

void handle_client(int client_socket) {
    char buffer[1024] = {0};
    read(client_socket, buffer, sizeof(buffer) - 1);

    std::string name = buffer;
    int score = update_score(name);
    std::string reply = "Score is now " + std::to_string(score) + "\n";

    send(client_socket, reply.c_str(), reply.size(), 0);
    close(client_socket);
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (sockaddr*)&address, sizeof(address));
    listen(server_fd, 20);

    std::cout << "C++ mutex server running on port " << PORT << std::endl;

    while (true) {
        int client_socket = accept(server_fd, nullptr, nullptr);
        std::thread(handle_client, client_socket).detach();
    }
}
EOF
```

```bash
cat > $ACT4/cpp_after/client.cpp << 'EOF'
#include <arpa/inet.h>
#include <iostream>
#include <string>
#include <unistd.h>

const int PORT = 9002;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: ./client <server_ip> <student_name>" << std::endl;
        return 1;
    }

    std::string server_ip = argv[1];
    std::string name = argv[2];

    int sock = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in server{};
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    inet_pton(AF_INET, server_ip.c_str(), &server.sin_addr);

    connect(sock, (sockaddr*)&server, sizeof(server));
    send(sock, name.c_str(), name.size(), 0);

    char buffer[1024] = {0};
    read(sock, buffer, sizeof(buffer) - 1);
    std::cout << buffer;

    close(sock);
    return 0;
}
EOF
```

### Server Machine: Compile and start the server

```bash
cd $ACT4
echo 0 > shared_score.txt
g++ -std=c++17 cpp_after/server_mutex.cpp -o cpp_after/server_mutex -pthread
./cpp_after/server_mutex
```

### Student A — run clients (replace `<SERVER_IP>`):

```bash
cd $ACT4
g++ -std=c++17 cpp_after/client.cpp -o cpp_after/client
for i in {1..10}; do ./cpp_after/client <SERVER_IP> A_$i & done
wait
```

### Student B — run at the same time (replace `<SERVER_IP>`):

```bash
cd $ACT4
g++ -std=c++17 cpp_after/client.cpp -o cpp_after/client
for i in {1..10}; do ./cpp_after/client <SERVER_IP> B_$i & done
wait
```

---

📸 **Screenshot 2 starts here** — on the server machine:
```bash
cat $ACT4/shared_score.txt
```
📸 **Screenshot 2 ends here**
> Capture all 3 terminals in one screenshot. Score should be exactly 20.
> Save as: `screenshots/cpp_after_mutex.png`

---

Stop the server with `Ctrl+C`, then reset:
```bash
echo 0 > $ACT4/shared_score.txt
```

---

## Task 3 — Java Server Before synchronized

### Server Machine: Create the files

```bash
cat > $ACT4/java_before/ScoreServerNoSync.java << 'EOF'
import java.io.*;
import java.net.*;

public class ScoreServerNoSync {
    private static final int PORT = 9011;
    private static final String FILE_NAME = "shared_score.txt";

    private static int updateScore(String name) throws Exception {
        File file = new File(FILE_NAME);
        int score = 0;

        if (file.exists()) {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line = reader.readLine();
            reader.close();
            if (line != null && !line.isBlank()) {
                score = Integer.parseInt(line.trim());
            }
        }

        Thread.sleep(200);

        score++;

        FileWriter writer = new FileWriter(file, false);
        writer.write(score + "\n");
        writer.close();

        System.out.println(name + " updated score to " + score);
        return score;
    }

    private static void handleClient(Socket socket) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            String name = in.readLine();
            int score = updateScore(name);
            out.println("Score is now " + score);

            socket.close();
        } catch (Exception e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws Exception {
        ServerSocket server = new ServerSocket(PORT);
        System.out.println("Java no-sync server running on port " + PORT);

        while (true) {
            Socket socket = server.accept();
            new Thread(() -> handleClient(socket)).start();
        }
    }
}
EOF
```

```bash
cat > $ACT4/java_before/ScoreClient.java << 'EOF'
import java.io.*;
import java.net.*;

public class ScoreClient {
    private static final int PORT = 9011;

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.out.println("Usage: java ScoreClient <server_ip> <student_name>");
            return;
        }

        String serverIp = args[0];
        String name = args[1];

        Socket socket = new Socket(serverIp, PORT);
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

        out.println(name);
        System.out.println(in.readLine());

        socket.close();
    }
}
EOF
```

### Server Machine: Compile and start the server

```bash
cd $ACT4
echo 0 > shared_score.txt
javac java_before/ScoreServerNoSync.java java_before/ScoreClient.java
java -cp java_before ScoreServerNoSync
```

### Student A — run clients (replace `<SERVER_IP>`):

```bash
cd $ACT4
for i in {1..10}; do java -cp java_before ScoreClient <SERVER_IP> A_$i & done
wait
```

### Student B — run at the same time (replace `<SERVER_IP>`):

```bash
cd $ACT4
for i in {1..10}; do java -cp java_before ScoreClient <SERVER_IP> B_$i & done
wait
```

---

📸 **Screenshot 3 starts here** — on the server machine:
```bash
cat $ACT4/shared_score.txt
```
📸 **Screenshot 3 ends here**
> Capture all 3 terminals in one screenshot.
> Save as: `screenshots/java_before_synchronized.png`

---

Stop the server with `Ctrl+C`, then reset:
```bash
echo 0 > $ACT4/shared_score.txt
```

---

## Task 4 — Java Server After synchronized

### Server Machine: Create the files

```bash
cat > $ACT4/java_after/ScoreServerSync.java << 'EOF'
import java.io.*;
import java.net.*;

public class ScoreServerSync {
    private static final int PORT = 9012;
    private static final String FILE_NAME = "shared_score.txt";

    private static synchronized int updateScore(String name) throws Exception {
        File file = new File(FILE_NAME);
        int score = 0;

        if (file.exists()) {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line = reader.readLine();
            reader.close();
            if (line != null && !line.isBlank()) {
                score = Integer.parseInt(line.trim());
            }
        }

        Thread.sleep(200);

        score++;

        FileWriter writer = new FileWriter(file, false);
        writer.write(score + "\n");
        writer.close();

        System.out.println(name + " updated score to " + score);
        return score;
    }

    private static void handleClient(Socket socket) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            String name = in.readLine();
            int score = updateScore(name);
            out.println("Score is now " + score);

            socket.close();
        } catch (Exception e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws Exception {
        ServerSocket server = new ServerSocket(PORT);
        System.out.println("Java synchronized server running on port " + PORT);

        while (true) {
            Socket socket = server.accept();
            new Thread(() -> handleClient(socket)).start();
        }
    }
}
EOF
```

```bash
cat > $ACT4/java_after/ScoreClient.java << 'EOF'
import java.io.*;
import java.net.*;

public class ScoreClient {
    private static final int PORT = 9012;

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.out.println("Usage: java ScoreClient <server_ip> <student_name>");
            return;
        }

        String serverIp = args[0];
        String name = args[1];

        Socket socket = new Socket(serverIp, PORT);
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

        out.println(name);
        System.out.println(in.readLine());

        socket.close();
    }
}
EOF
```

### Server Machine: Compile and start the server

```bash
cd $ACT4
echo 0 > shared_score.txt
javac java_after/ScoreServerSync.java java_after/ScoreClient.java
java -cp java_after ScoreServerSync
```

### Student A — run clients (replace `<SERVER_IP>`):

```bash
cd $ACT4
for i in {1..10}; do java -cp java_after ScoreClient <SERVER_IP> A_$i & done
wait
```

### Student B — run at the same time (replace `<SERVER_IP>`):

```bash
cd $ACT4
for i in {1..10}; do java -cp java_after ScoreClient <SERVER_IP> B_$i & done
wait
```

---

📸 **Screenshot 4 starts here** — on the server machine:
```bash
cat $ACT4/shared_score.txt
```
📸 **Screenshot 4 ends here**
> Capture all 3 terminals in one screenshot. Score should be exactly 20.
> Save as: `screenshots/java_after_synchronized.png`

---

Stop the server with `Ctrl+C`.

---

## Verify Your Folder Structure

```bash
ls -1 $ACT4
ls -1 $ACT4/cpp_before/
ls -1 $ACT4/cpp_after/
ls -1 $ACT4/java_before/
ls -1 $ACT4/java_after/
ls -1 $ACT4/screenshots/
```

---

## Git Push

```bash
cd ~/Desktop/github/os-se-p20240034
git add .
git commit -m "Activity 4: Shared File API with C++ mutex and Java synchronized"
git push origin main
```