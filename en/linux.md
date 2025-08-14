# 🐧 Linux Command Line Cheat Sheet

> 📘 Basic and advanced commands for navigation, working with files, processes, networking, and automation in the Linux terminal.  
> Suitable for DevOps engineers of all levels.

---

## 📂 Contents

- [🐧 Linux Command Line Cheat Sheet](#-linux-command-line-cheat-sheet)
  - [📂 Contents](#-contents)
  - [🔹 Basic commands](#-basic-commands)
  - [🔸 Intermediate level](#-intermediate-level)
  - [🔧 Advanced commands](#-advanced-commands)
  - [🌐 Network commands](#-network-commands)
  - [🔍 Searching and managing files](#-searching-and-managing-files)
  - [📊 System monitoring](#-system-monitoring)
  - [📦 Package management](#-package-management)
  - [💽 File systems](#-file-systems)
  - [🤖 Scripts and automation](#-scripts-and-automation)
  - [🛠 Development and debugging](#-development-and-debugging)
  - [📌 Miscellaneous](#-miscellaneous)
  - [Additional resources](#additional-resources)

---

## 🔹 Basic commands

| Command       | Example                        | Description |
| ------------- | ------------------------------ | ----------- |
| [**`cat`**](https://tldr.inbrowser.app/pages/linux/cat) | | **Show file content or concatenate multiple files** |
|               | `cat file.txt`                 | View file content |
|               | `cat file1 file2`              | Concatenate and output two files |
|               | `cat file1 file2 > merged.txt` | Concatenate files and save to a new file |
| [**`cd`**](https://tldr.inbrowser.app/pages/common/cd) | | **Change to the specified directory** |
|               | `cd /etc`                      | Go to absolute path `/etc` |
|               | `cd ~`                         | Go to home directory |
|               | `cd ..`                        | Move one level up |
|               | `cd -`                         | Return to previous directory |
| [**`clear`**](https://tldr.inbrowser.app/pages/common/clear) | | **Clear the terminal output** |
| [**`cp`**](https://tldr.inbrowser.app/pages/common/cp) | | **Copy files and directories** |
|               | `cp file1.txt file2.txt`       | Copy file with a new name |
|               | `cp -r dir1 dir2`              | Recursively copy directory |
|               | `cp -i file.txt /tmp/`         | Copy with confirmation before overwrite |
| [**`echo`**](https://tldr.inbrowser.app/pages/common/echo) | | **Print text or variable value** |
|               | `echo "Hello, World!"`         | Print a simple string |
|               | `echo $HOME`                   | Show home directory path |
|               | `echo -e "1\t2\n3"`            | Interpret escape sequences (`\t`, `\n`) |
| [**`history`**](https://tldr.inbrowser.app/pages/common/history) | | **Show command history** |
| [**`id`**](https://tldr.inbrowser.app/pages/common/id) | | **Show UID, GID and groups of current user** |
| [**`ls`**](https://tldr.inbrowser.app/pages/common/ls) | | **List files and directories** |
|               | `ls -l`                        | Detailed list with permissions and owners |
|               | `ls -a`                        | Show hidden files |
|               | `ls -lh`                       | Human-readable file sizes |
| [**`mkdir`**](https://tldr.inbrowser.app/pages/common/mkdir) | | **Create a new directory** |
|               | `mkdir folder`                 | Create a regular directory |
|               | `mkdir -p a/b/c`               | Create nested directories |
|               | `mkdir dir{1,2,3}`             | Create multiple directories at once |
| [**`mv`**](https://tldr.inbrowser.app/pages/common/mv) | | **Move or rename file/directory** |
|               | `mv oldname.txt newname.txt`   | Rename file |
|               | `mv file.txt /path/to/dir/`    | Move file to another directory |
|               | `mv *.txt archive/`            | Move all `.txt` files to `archive` folder |
| [**`pwd`**](https://tldr.inbrowser.app/pages/common/pwd) | | **Show absolute path to current directory** |
|               | `pwd -P`                       | Show physical path (no symbolic links) |
|               | `cd /tmp && pwd`               | Show path after changing to `/tmp` |
| [**`rm`**](https://tldr.inbrowser.app/pages/common/rm) | | **Delete file or directory** |
|               | `rm file.txt`                  | Delete a file |
|               | `rm -i file.txt`               | Delete file with confirmation |
|               | `rm -r folder/`                | Delete directory recursively |
|               | `rm -rf folder/`               | Delete everything without confirmation (⚠️ no confirmation) |
| [**`rmdir`**](https://tldr.inbrowser.app/pages/common/rmdir) | | **Remove empty directory** |
|               | `rmdir emptydir`               | Remove directory `emptydir` |
| [**`touch`**](https://tldr.inbrowser.app/pages/common/touch) | | **Create empty file or update modification time** |
|               | `touch newfile.txt`            | Create a new empty file if it doesn’t exist |
|               | `touch a b c`                  | Create multiple files at once |
|               | `touch -c file.txt`            | Update time without creating file if it doesn’t exist |
| [**`whereis`**](https://tldr.inbrowser.app/pages/linux/whereis) | | **Show path to binary, source and documentation of a command** |
|               | `whereis ls`                   | Find executable and docs location of `ls` |
|               | `whereis bash`                 | Show paths for bash binary and docs |
|               | `whereis -b bash`              | Search for binary only |
| [**`which`**](https://tldr.inbrowser.app/pages/common/which) | | **Show path to executable file of a command** |
|               | `which python3`                | Path to `python3` |
|               | `which grep`                   | Path to utility `grep` |
|               | `which --skip-alias ls`        | Skip aliases when searching |
| [**`whoami`**](https://tldr.inbrowser.app/pages/common/whoami) | | **Show current user name** |

---

## 🔸 Intermediate level

| Command        | Example                                | Description |
| -------------- | -------------------------------------- | ----------- |
| [**`chmod`**](https://tldr.inbrowser.app/pages/common/chmod) | | **Changes file or directory permissions** |
|                | `chmod 755 file`                       | Change file or folder permissions. Numbers: `7` = read, write, execute `(rwx)`, `5` = read, execute `(r-x)` |
|                | `chmod +x script.sh`                   | Add execution permission |
|                | `chmod -R 644 dir/`                    | Recursively set permissions: `6` = read and write `(rw-)` for owner, `4` = read `(r--)` for group and others; applies to all files/folders in `dir/` |
| [**`chown`**](https://tldr.inbrowser.app/pages/common/chown) | | **Change owner (user) and group for files and directories** |
|                | `chown user file`                      | Change file owner |
|                | `chown user:group file`                | Change owner and group |
|                | `chown -R user:group dir/`             | Recursively change owner and group |
| [**`curl`**](https://tldr.inbrowser.app/pages/common/curl) | | **Send an HTTP request to a server and get a response** |
|                | `curl -I https://example.com`          | HEAD request (headers only) |
|                | `curl -O https://example.com/file.txt` | Download a file with its original name |
|                | `curl -d "a=1&b=2" -X POST url`        | Send a POST request with parameters |
| [**`df`**](https://tldr.inbrowser.app/pages/linux/df) | | **Display disk usage summary of the filesystem** |
|                | `df -h`                                | Show disk usage in human-readable format |
|                | `df /home`                             | Usage of a specific filesystem |
|                | `df -T`                                | Show filesystem types |
| [**`diff`**](https://tldr.inbrowser.app/pages/common/diff) | | **Compare files and directories** |
|                | `diff file1 file2`                     | Compare contents of two files |
|                | `diff -u old.c new.c`                  | Unified diff output (useful for patches) |
|                | `diff -r dir1 dir2`                    | Compare directories |
| [**`du`**](https://tldr.inbrowser.app/pages/common/du) | | **Disk usage: estimate and summarize space used by files/directories** |
|                | `du -sh *`                             | Show size of all items in current directory |
|                | `du -h file.txt`                       | Show size of one file |
|                | `du -sh --max-depth=1 /var`            | Show sizes of directories in `/var` without subfolders |
| [**`find`**](https://tldr.inbrowser.app/pages/common/find) | | **Recursive search for files/folders in a directory** |
|                | `find . -name "*.log"`                 | Find all `.log` files in current directory |
|                | `find / -type f -size +100M`           | Find files larger than 100MB |
|                | `find . -mtime -1`                     | Files modified within the last 24 hours |
| [**`free`**](https://tldr.inbrowser.app/pages/linux/free) | | **Show amount of free and used memory in the system** |
|                | `free -h`                              | Show memory usage in human-readable format |
|                | `free -m`                              | Show in megabytes |
|                | `watch -n 2 free -h`                   | Auto-refresh memory info every 2 seconds |
| [**`grep`**](https://tldr.inbrowser.app/pages/common/grep) | | **Search patterns in files using regular expressions** |
|                | `grep "error" logfile`                 | Search for "error" in a file |
|                | `grep -r "error" /var/log`             | Recursive search |
|                | `grep -i "fail" file`                  | Case-insensitive search |
| [**`head`**](https://tldr.inbrowser.app/pages/linux/head) | | **Display the first lines of a file** |
|                | `head -n 10 file`                      | Show first 10 lines |
|                | `head -n 20 file.txt`                  | First 20 lines |
|                | `head -c 100 file`                     | First 100 bytes of a file |
| [**`hostname`**](https://tldr.inbrowser.app/pages/common/hostname) | | **Show or set the hostname** |
|                | `hostname newname`                     | Set temporary hostname until reboot |
|                | `hostname -I`                          | Show IP address |
| [**`kill`**](https://tldr.inbrowser.app/pages/linux/kill) | | **Terminate processes by PID or name** |
|                | `kill -9 1234`                         | Forcefully terminate a process by PID |
|                | `kill -TERM 1234`                      | Graceful process termination |
|                | `pkill -f python`                      | Kill processes containing `python` in the command line |
| [**`ping`**](https://tldr.inbrowser.app/pages/common/ping) | | **Check host availability over the network using ICMP requests** |
|                | `ping 8.8.8.8`                         | Check connection to an address |
|                | `ping -c 4 ya.ru`                      | Send 4 pings |
|                | `ping -i 2 1.1.1.1`                    | 2-second interval between pings |
| [**`ps`**](https://tldr.inbrowser.app/pages/common/ps) | | **Display information about running processes** |
|                | `ps aux`                               | List all processes |
|                | `ps -ef \| grep nginx`                 | Find processes by name |
|                | `ps -u $USER`                          | Processes of the current user |
| [**`rsync`**](https://tldr.inbrowser.app/pages/common/rsync) | | **Fast and reliable file/directory synchronization** |
|                | `rsync -av src/ dst/`                  | Synchronize locally |
|                | `rsync -avz user@host:/src /dst`       | Sync with a remote machine |
|                | `rsync --delete src/ dst/`             | Delete in `dst/` files missing in `src/` |
| [**`scp`**](https://tldr.inbrowser.app/pages/common/scp) | | **Secure file transfer between hosts via SSH** |
|                | `scp file user@host:/path`             | Copy file to remote machine via SSH |
|                | `scp user@host:/file.txt .`            | Copy file from remote host |
|                | `scp -r dir user@host:/path`           | Recursively transfer a directory |
| [**`sort`**](https://tldr.inbrowser.app/pages/common/sort) | | **Sort lines of text from a file or input** |
|                | `sort file.txt`                        | Sort lines alphabetically |
|                | `sort -r file.txt`                     | Reverse order |
|                | `sort -n numbers.txt`                  | Numeric sort |
| [**`tail`**](https://tldr.inbrowser.app/pages/common/tail) | | **Show the last lines of a file, follow changes** |
|                | `tail -f logfile.log`                  | Follow file changes in real time |
|                | `tail -n 20 file.txt`                  | Last 20 lines |
|                | `tail -c 100 file.txt`                 | Last 100 bytes |
| [**`tar`**](https://tldr.inbrowser.app/pages/common/tar) | | **Create, view, extract `.tar` archives** |
|                | `tar -czf archive.tgz dir/`            | Create a compressed archive from `dir/` in `.tgz` format |
|                | `tar -xzf archive.tgz`                 | Extract a `.tgz` archive |
|                | `tar -tf archive.tgz`                  | List archive contents without extracting |
| [**`tee`**](https://tldr.inbrowser.app/pages/common/tee) | | **Copy standard output and save it to a file** |
|                | `echo "test" \| tee out.txt`           | Write command output to `out.txt` and display it |
|                | `ls tee \| list.txt`                   | Save `ls` output to file and show in terminal |
|                | `command \| tee -a log.txt`            | Append command output to end of `log.txt` |
| [**`top`**](https://tldr.inbrowser.app/pages/linux/top) | | **Real-time system resource monitoring** |
|                | `top`                                  | Process monitoring |
|                | `htop`                                 | Advanced interactive interface |
|                | `top -o %MEM`                          | Sort processes by memory usage |
| [**`uptime`**](https://tldr.inbrowser.app/pages/common/uptime) | | **Show system uptime and load** |
|                | `uptime -p`                            | Show uptime in readable format |
|                | `uptime -s`                            | Show date/time of last system boot |
| [**`wget`**](https://tldr.inbrowser.app/pages/common/wget) | | **Download files via HTTP, HTTPS, or FTP from terminal** |
|                | `wget https://site.com/file.zip`       | Download file by URL |
|                | `wget -c file.zip`                     | Resume interrupted download |
|                | `wget -O saved.txt URL`                | Download and save with a different name |
| [**`wc`**](https://tldr.inbrowser.app/pages/common/wc) | | **Count lines, words, bytes, or characters in a file** |
|                | `wc -l file`                           | Count number of lines |
|                | `wc -w file`                           | Count number of words |
|                | `wc -m file`                           | Count number of characters |
| [**`uniq`**](https://tldr.inbrowser.app/pages/common/uniq) | | **Remove duplicate lines from a sorted file** |
|                | `uniq file.txt`                        | Remove adjacent duplicate lines |
|                | `sort file \| uniq`                    | Remove all duplicates |
|                | `sort file \| uniq -c`                 | Count occurrences of each line |
| [**`yes`**](https://tldr.inbrowser.app/pages/common/yes) | | **Automatically answer "yes" or other word to prompts** |
|                | `yes "y" \| command`                   | Always answer "y" to command prompts |
|                | `yes \| rm -i *`                       | Auto-confirm deletion |
|                | `yes no \| command`                    | Automatically answer "no" |

---

## 🔧 Advanced commands

| Command               | Example                                           | Description |
|-----------------------|---------------------------------------------------|------------ |
| [**`at`**](https://tldr.inbrowser.app/pages/common/at) |                  | **One-time task scheduler** |
|                       | `at now + 1 minute`                               | Schedule a one-time task that will run in one minute |
|                       | `atq`                                             | View the `at` job queue |
|                       | `atrm`                                            | Remove a job from the `at` queue |
| [**`awk`**](https://tldr.inbrowser.app/pages/common/awk) |                | **Text processing utility line by line: splits lines into fields and allows filtering, extracting, and formatting** |
|                       | `awk '{print $1}' file`                           | Print the first field (word) from each line of a file |
|                       | `ps aux \| awk '$3 > 50'`                         | Show processes with CPU usage over 50% |
|                       | `cat file.txt \| awk '{print $2}'`                | Show the second field from each line of the file |
|                       | `awk '/error/ {print $0}' logfile`                | Show lines containing "error" from the log file |
| [**`crontab`**](https://tldr.inbrowser.app/pages/common/crontab) |        | **Recurring task scheduler** |
|                       | `crontab -e`                                      | Edit cron jobs for the current user |
|                       | `crontab -l`                                      | List cron jobs for the current user |
|                       | `crontab -r`                                      | Remove all cron jobs for the current user |
| [**`cut`**](https://tldr.inbrowser.app/pages/common/cut) |                | **Cut specific fields or columns from text** |
|                       | `cut -d':' -f1 /etc/passwd`                       | Extract the first field (usernames) by `:` delimiter from `/etc/passwd` |
|                       | `echo "a:b:c" \| cut -d':' -f2`                   | Get the second field (`b`) from a colon-separated string |
|                       | `cut -c1-5 filename`                              | Extract the first 5 characters from each line of a file |
| [**`df`**](https://tldr.inbrowser.app/pages/linux/df) |                   | **Filesystem and free space information** |
|                       | `df -h`                                           | Show disk usage and free space in human-readable format |
|                       | `df -T`                                           | Show filesystem type |
|                       | `df /home`                                        | Show information about the filesystem where `/home` resides |
| [**`env`**](https://tldr.inbrowser.app/pages/common/env) |                | **Show current environment variables** |
|                       | `env \| grep PATH`                                | Show environment variables containing `PATH` |
|                       | `env -i bash`                                     | Start a new `bash` session without inherited environment variables |
| [**`export`**](https://tldr.inbrowser.app/pages/linux/export) |           | **Set environment variable (only for current session)** |
|                       | `export VAR=value`                                | Set the variable `VAR` to `value` |
|                       | `export PATH=$PATH:/new/path`                     | Add `/new/path` to the current `PATH` variable |
|                       | `export -p`                                       | List all exported environment variables |
| [**`free`**](https://tldr.inbrowser.app/pages/linux/free) |               | **Show memory usage** |
|                       | `free -m`                                         | Show memory usage in megabytes |
|                       | `free -h`                                         | Show memory usage in human-readable format (e.g., 2G, 512M) |
|                       | `free -s 5`                                       | Update memory usage info every 5 seconds |
| [**`hostnamectl`**](https://tldr.inbrowser.app/pages/linux/hostnamectl) | | **Show detailed hostname and OS information** |
|                       | `hostnamectl status`                              | Show current hostname and related settings |
|                       | `hostnamectl set-hostname newname`                | УSet persistent hostname `newname` (remains after reboot) |
| [**`ifconfig`**](https://tldr.inbrowser.app/pages/common/ifconfig) / [**`ip`**](https://tldr.inbrowser.app/pages/linux/ip) | | **Configure and view network interfaces** |
|                       | `ifconfig`                                        | Show current network interfaces (deprecated command) |
|                       | `ip a`                                            | Show all network interfaces and their IP addresses |
|                       | `ip link set eth0 up`                             | Enable the network interface `eth0` |
| [**`iostat`**](https://tldr.inbrowser.app/pages/linux/iostat) |           | **Input/output statistics per device** |
|                       | `iostat -x 2`                                     | Show extended statistics every 2 seconds |
|                       | `iostat -d 5 3`                                   | Show device statistics: 3 times with 5-second interval |
| [**`iptables`**](https://tldr.inbrowser.app/pages/linux/iptables) |       | **Configure firewall (packet filtering) rules** |
|                       | `iptables -L`                                     | List current firewall rules |
|                       | `iptables -A INPUT -p tcp --dport 22 -j ACCEPT`   | Allow incoming TCP connections on port 22 (SSH) |
|                       | `iptables -F`                                     | Flush all firewall rules |
| [**`journalctl`**](https://tldr.inbrowser.app/pages/linux/journalctl) |   | **View system logs (journals)** |
|                       | `journalctl -xe`                                  | Show recent messages with extended error info |
|                       | `journalctl -u nginx.service`                     | Show logs for the `nginx` service |
|                       | `journalctl --since "2 hours ago"`                | Show logs from the last 2 hours |
| [**`ln`**](https://tldr.inbrowser.app/pages/common/ln) |                  | **Create links to files or directories** |
|                       | `ln -s target link`                               | Create a symbolic link `link` to the file/directory `target` |
|                       | `ln file.txt backup.txt`                          | Create a hard link to `file.txt` named `backup.txt` |
|                       | `ln -sf target link`                              | Force overwrite the symbolic link `link` with `target` |
| [**`sed`**](https://tldr.inbrowser.app/pages/linux/sed) |                 | **Stream editor for search and replace** |
|                       | `sed 's/old/new/g' file`                          | Replace all occurrences of "old" with "new" in a file |
|                       | `sed -n '1,5p' file`                              | Show lines 1 to 5 from a file |
|                       | `sed '/pattern/d' file`                           | Delete lines containing `pattern` |
| [**`systemctl`**](https://tldr.inbrowser.app/pages/linux/systemctl) |     | **Manage system services** |
|                       | `systemctl status nginx`                          | Check the status of the `nginx` service |
|                       | `systemctl start nginx`                           | Start the `nginx` service |
|                       | `systemctl enable nginx`                          | Enable auto-start of `nginx` service on system boot |
| [**`tr`**](https://tldr.inbrowser.app/pages/common/tr) |                  | **Text transformation, e.g., changing character case** |
|                       | `tr a-z A-Z`                                      | Convert lowercase letters to uppercase |
|                       | `echo "hello" \| tr 'h' 'H'`                      | Replace `h` with `H` |
|                       | `echo "abc123" \| tr -d '0-9'`                    | Remove all digits from the string |
| [**`type`**](https://tldr.inbrowser.app/pages/common/type) |              | **Determine command type (built-in, alias, or executable)** |
|                       | `type ls`                                         | Find out where the `ls` command comes from |
|                       | `type cd`                                         | Check if `cd` is a built-in command |
|                       | `type python3`                                    | Locate the path to the `python3` executable |
| [**`ulimit`**](https://tldr.inbrowser.app/pages/common/ulimit) |          | **Show or set resource limits for processes** |
|                       | `ulimit -n`                                       | Show the maximum number of open files |
|                       | `ulimit -c unlimited`                             | Allow unlimited core file size |
|                       | `ulimit -u 4096`                                  | Limit the number of processes to 4096 |
| [**`uptime`**](https://tldr.inbrowser.app/pages/common/uptime) |          | **Show system uptime and load** |
|                       | `uptime -p`                                       | Display system uptime in human-readable format |
|                       | `uptime -s`                                       | Show the date and time of the last system boot |
| [**`xargs`**](https://tldr.inbrowser.app/pages/common/xargs) |            | **Pass arguments from one command to another** |
|                       | `xargs -n 1 echo`                                 | Run `echo` for each argument separately |
|                       | `echo "a b c" \| xargs -n 1`                      | Print each word on a new line |
|                       | `find . -name '*.txt' \| xargs rm`                | Delete all `.txt` files found by `find` |

---

## 🌐 Network commands

| Command                         | Example                                | Description |
| ------------------------------- | -------------------------------------- | ----------- |
| [**`curl`**](https://tldr.inbrowser.app/pages/common/curl) |             | **Send an HTTP request to a server and get a response** |
|                                 | `cyrl -X POST -d "a=1" URL`            | Send a POST request with data |
|                                 | `curl -I URL`                          | Fetch only the HTTP headers from a response |
|                                 | `curl -o file.html URL`                | Download a webpage to a file |
| [**`dig`**](https://tldr.inbrowser.app/pages/common/dig) |               | **DNS query utility** |
|                                 | `dig openai.com`                       | Perform a detailed DNS query for the domain `openai.com` |
|                                 | `dig +short openai.com`                | Quickly show the IP addresses |
|                                 | `dig @8.8.8.8 openai.com`              | Use Google's DNS server for the query |
| [**`ftp`**](https://tldr.inbrowser.app/pages/common/ftp) |               | **Tools for interacting with an FTP server** |
|                                 | `ftp host`                             | Connect to an FTP server |
|                                 | `ftp -n host`                          | Connect without automatic login |
|                                 | `ftp> get file.txt`                    | Download a file in an FTP session |
| [**`ip address`**](https://tldr.inbrowser.app/pages/linux/ip-address) |  | **Show IP addresses assigned to interfaces** |
|                                 | `ip addr show eth0`                    | Show IP addresses for specific interface `eth0` |
|                                 | `ip addr`                              | Display info for all interfaces |
| [**`ip link`**](https://tldr.inbrowser.app/pages/linux/) |               | **List of network interfaces** |
|                                 | `ip link show`                         | Show all interfaces |
|                                 | `ip link set eth0 up`                  | Bring up interface `eth0` |
| [**`ip route`**](https://tldr.inbrowser.app/pages/linux/ip-route) |      | **Show routing table** |
|                                 | `ip route list`                        | List all routes |
|                                 | `ip route add default via 192.168.1.1` | Add default route via 192.168.1.1 |
| [**`nc`**](https://tldr.inbrowser.app/pages/common/nc) |                 | **Universal tool for redirecting input/output over the network** |
|                                 | `nc -zv host 22`                       | Check if port 22 on a host is open (`-z` = no data sent, `-v` = verbose) |
|                                 | `nc -l 1234`                           | Start a listener on port 1234 |
|                                 | `nc host 1234 < file`                  | Send a file's content to a host and port |
| [**`nmap`**](https://tldr.inbrowser.app/pages/common/nmap) |             | **Network scanning and reconnaissance tool** |
|                                 | `nmap -sP 192.168.1.0/24`              | Scan the network to find active hosts |
|                                 | `nmap -sV 192.168.1.1`                 | Detect service versions on a host |
|                                 | `nmap -O 192.168.1.1`                  | Detect operating system of a host |
| [**`nslookup`**](https://tldr.inbrowser.app/pages/common/nslookup) |     | **Query DNS servers for domain records** |
|                                 | `nslookup google.com`                  | Perform a DNS query for `google.com` |
|                                 | `nslookup 8.8.8.8`                     | Find hostname from IP address |
| [**`ssh`**](https://tldr.inbrowser.app/pages/common/ssh) |               | **Secure Shell protocol for remote login** |
|                                 | `ssh user@host`                        | Connect to a remote server via SSH |
|                                 | `ssh -p 2222 user@host`                | Connect to a remote host on a custom port 2222 |
|                                 | `ssh -i ~/.ssh/id_rsa user@host`       | Connect using a private key |
| [**`ss`**](https://tldr.inbrowser.app/pages/linux/ss) |                  | **Socket analysis and network connection display utility** |
|                                 | `ss -tuln`                             | Show all open TCP and UDP ports without resolving names |
|                                 | `ss -s`                                | Summary statistics for sockets |
|                                 | `ss -l`                                | Show only listening sockets |
| [**`telnet`**](https://tldr.inbrowser.app/pages/common/telnet) |         | **Connect to a specified host and port using telnet** |
|                                 | `telnet host 80`                       | Connect to port 80 on a remote host |
|                                 | `telnet example.com 443`               | Check if HTTPS port is open |
|                                 | `telnet localhost 25`                  | Connect to a local SMTP server |
| [**`traceroute`**](https://tldr.inbrowser.app/pages/common/traceroute) | | **Trace the path packets take to a host** |
|                                 | `traceroute 8.8.8.8`                   | Trace route to 8.8.8.8 |
|                                 | `traceroute -m 15 8.8.8.8`             | Limit number of hops to 15 |
| [**`wget`**](https://tldr.inbrowser.app/pages/common/wget) |             | **Download files via HTTP, HTTPS, or FTP from terminal** |
|                                 | `wget -O file.txt URL`                 | Download a URL and save it as `file.txt` |
|                                 | `wget URL`                             | Download a file with its original name |
|                                 | `wget -c URL`                          | Resume an interrupted download |

---

## 🔍 Searching and managing files

| Command        | Example                           | Description |
| -------------- | --------------------------------- | ----------- |
| [**`basename`**](https://tldr.inbrowser.app/pages/common/basename) | | **Get filename from full path** |
|                | `basename /path/to/file`          | Output only the filename |
|                | `basename /path/to/file .txt`     | Remove `.txt` extension from filename |
| [**`dirname`**](https://tldr.inbrowser.app/pages/common/dirname) | | **Get directory path from full path** |
|                | `dirname /path/to/file`           | Output directory path without filename |
|                | `dirname /etc/passwd`             | Output the `/etc` path |
| [**`du`**](https://tldr.inbrowser.app/pages/common/du) | | **Show size of directories and files in human-readable format** |
|                | `du -sh folder/`                  | Show total size of the `folder` directory |
|                | `du -h *`                         | Show sizes of all files and directories in current directory |
|                | `du -c folder1 folder2`           | Show combined size of two directories |
| [**`file`**](https://tldr.inbrowser.app/pages/common/file) | | **Determine file content type** |
|                | `file some.bin`                   | Show file type (e.g., text, binary) |
|                | `file *`                          | Determine types for all files in current directory |
|                | `file -i file.txt`                | Show MIME type of a file |
| [**`find`**](https://tldr.inbrowser.app/pages/common/find) | | **Search for files and directories by specific conditions** |
|                | `find /path -type f -name "*.sh"` | Find all `.sh` files in the `/path` directory |
|                | `find . -size +10M`               | Find files larger than 10 MB |
|                | `find /tmp -mtime -1`             | Find files modified within the last 24 hours |
| [**`locate`**](https://tldr.inbrowser.app/pages/linux/locate) | | **Fast file search by name** |
|                | `locate filename`                 | Search for file or path using a database |
|                | `locate *.conf`                   | Search for all `.conf` files |
|                | `locate -i README`                | Case-insensitive file search |
| [**`realpath`**](https://tldr.inbrowser.app/pages/common/realpath) | | **Show full absolute path of a file** |
|                | `realpath file`                   | Output full file path |
|                | `realpath ../relative/path`       | Get absolute path from a relative one |
| [**`stat`**](https://tldr.inbrowser.app/pages/common/stat) | | **Detailed info about a file or directory** |
|                | `stat file`                       | Display detailed info (owner, permissions, timestamps) |
|                | `stat -c %s file`                 | Show only the file size in bytes |
|                | `stat -f file`                    | Show information about the file system |
| [**`tree`**](https://tldr.inbrowser.app/pages/common/tree) | | **Hierarchical tree view of directories and files** |
|                | `tree`                            | Show directory structure as a tree |
|                | `tree -L 2`                       | Limit tree display depth to 2 levels |
|                | `tree -a`                         | Also show hidden files and directories |

---

## 📊 System monitoring

| Command      | Example                               | Description |
| ------------ | ------------------------------------- | ----------- |
| [**`dmesg`**](https://tldr.inbrowser.app/pages/linux/dmesg) | | **View Linux kernel messages** |
|              | `dmesg \| tail`                       | Show last 10 kernel messages |
|              | `dmesg \| grep usb`                   | Find messages related to USB |
| [**`free`**](https://tldr.inbrowser.app/pages/linux/free) | | **Memory information: free and used** |
|              | `free -h`                             | Display memory in human-readable format (MB, GB) |
|              | `free -m`                             | Display memory in megabytes |
| [**`htop`**](https://tldr.inbrowser.app/pages/common/htop) | | **Interactive process monitoring** |
|              | `htop`                                | Launch interface with processes and resource usage |
|              | (используется клавиши для управления) | Allows sorting and filtering of processes |
| [**`iotop`**](https://tldr.inbrowser.app/pages/common/iotop) | | **Disk I/O monitoring by process** |
|              | `iotop`                               | Display active I/O processes |
|              | `iotop -o`                            | Show only processes with active I/O |
| [**`lsof`**](https://tldr.inbrowser.app/pages/common/lsof) | | **List of open files, including network connections** |
|              | `lsof -i :80`                         | Show processes using port 80 |
|              | `lsof -u username`                    | List open files for user `username` |
| [**`uptime`**](https://tldr.inbrowser.app/pages/common/uptime) | | **Show system uptime and CPU load** |
| [**`vmstat`**](https://tldr.inbrowser.app/pages/linux/vmstat) | | **Memory, process, and system statistics** |
|              | `vmstat 1`                            | Output statistics every second |
|              | `vmstat 5 3`                          | Display 3 reports with 5-second interval |
| [**`watch`**](https://tldr.inbrowser.app/pages/common/watch) | | **Repeat command at regular intervals** |
|              | `watch -n 1 df -h`                    | Repeat `df -h` every second |
|              | `watch -d free -h`                    | Repeat `free -h` with highlighted changes |

---

## 📦 Package management

| Command                        | Example                     | Description |
| ------------------------------ | --------------------------- | ----------- |
| [**`apt`**](https://tldr.inbrowser.app/pages/linux/apt) | | **Package management in Debian/Ubuntu** |
|                                | `apt install curl`          | Install the `curl` package |
|                                | `apt remove curl`           | Remove an installed package |
|                                | `apt update && apt upgrade` | Update the package list and upgrade packages |
| [**`dnf`**](https://tldr.inbrowser.app/pages/linux/dnf) | | **Enhanced `yum`, used in Fedora** |
|                                | `dnf install curl`          | Install the `curl` package |
|                                | `dnf upgrade`               | Upgrade all installed packages |
| [**`rpm`**](https://tldr.inbrowser.app/pages/linux/rpm) | | **Manual installation/removal of `.rpm` packages** |
|                                | `rpm -ivh package.rpm`      | Install a `.rpm` package |
|                                | `rpm -e package`            | Remove an installed `rpm` package |
| [**`snap`**](https://tldr.inbrowser.app/pages/linux/snap) | | **Universal packages for different distributions** |
|                                | `snap install app`          | Install an application via `snap` |
|                                | `snap remove app`           | Remove an installed Snap application |
| [**`yum`**](https://tldr.inbrowser.app/pages/linux/yum) | | **Package manager for CentOS/RHEL** |
|                                | `yum install curl`          | Install the `curl` package |
|                                | `yum remove curl`           | Remove an installed package |

---

## 💽 File systems

| Command                              | Example                | Description |
| ------------------------------------ | ---------------------- | ----------- |
| [**`blkid`**](https://tldr.inbrowser.app/pages/linux/blkid) | | **Information about UUIDs and partition types** |
|                                      | `blkid`                | Show UUIDs and types of all devices |
| [**`df`**](https://tldr.inbrowser.app/pages/linux/df) | | **Disk usage and filesystem types** |
|                                      | `df -Th`               | Show usage and filesystem types |
| [**`fsck`**](https://tldr.inbrowser.app/pages/linux/fsck) | | **Filesystem integrity check** |
|                                      | `fsck /dev/sda1`       | Check and repair `/dev/sda1` |
| [**`lsblk`**](https://tldr.inbrowser.app/pages/linux/lsblk) | | **List block devices** |
|                                      | `lsblk`                | Hierarchical display of disks |
| [**`mkfs`**](https://tldr.inbrowser.app/pages/linux/mkfs) | | **Partition formatting** |
|                                      | `mkfs.ext4 /dev/sdb1`  | Create an ext4 filesystem |
| [**`mount`**](https://tldr.inbrowser.app/pages/linux/mount) | | **Mounting filesystems** |
|                                      | `mount /dev/sdb1 /mnt` | Mount the partition to `/mnt` |
|                                      | `mount \| grep /mnt`   | Check what's mounted |
| [**`parted`**](https://tldr.inbrowser.app/pages/linux/parted) | | **Partition management** |
|                                      | `parted /dev/sdb`      | Open utility to manage `/dev/sdb` |
| [**`umount`**](https://tldr.inbrowser.app/pages/linux/umount) | | **Unmounting filesystems** |
|                                      | `umount /mnt`          | Unmount the `/mnt` partition |

---

## 🤖 Scripts and automation

| Command                                     | Example                   | Description |
| ------------------------------------------- | ------------------------- | ----------- |
| [**`alias`**](https://tldr.inbrowser.app/pages/common/alias) | | **Create aliases** |
|                                             | `alias ll='ls -la'`       | Create alias `ll` |
|                                             | `alias`                   | Show all aliases |
| [**`bash` / `sh`**](https://tldr.inbrowser.app/pages/common/bash) | | **Run scripts** |
|                                             | `bash script.sh`          | Run script using bash |
|                                             | `sh script.sh`            | Alternative way to run a script |
| [**`crontab`**](https://tldr.inbrowser.app/pages/common/crontab) | | **Task scheduler** |
|                                             | `crontab -e`              | Open cron editor |
| [**`read`**](https://tldr.inbrowser.app/pages/common/read) | | **Read input into a variable** |
|                                             | `read name`               | Read value into variable `name` |
| [**`set`**](https://tldr.inbrowser.app/pages/common/set) | | **Change script behavior** |
|                                             | `set -e`                  | Stop execution on error |
| [**`source`**](https://tldr.inbrowser.app/pages/common/source) | | **Load configuration file** |
|                                             | `source ~/.bashrc`        | Apply bash config changes |
| [**`trap`**](https://tldr.inbrowser.app/pages/linux/trap) | | **Signal handling in a script** |
|                                             | `trap "echo 'exit'" EXIT` | Message on script exit |

---

## 🛠 Development and debugging

| Command                                  | Example                | Description |
| ---------------------------------------- | ---------------------- | ----------- |
| [**`gcc`**](https://tldr.inbrowser.app/pages/common/gcc) | | **Compile C programs** |
|                                          | `gcc main.c -o app`    | Compile `main.c` into `app` |
| [**`gdb`**](https://tldr.inbrowser.app/pages/common/gdb) | | **Interactive program debugging** |
|                                          | `gdb ./app`            | Start debugging binary |
| [**`git`**](https://tldr.inbrowser.app/pages/common/git) | | **Version control system** |
|                                          | `git status`           | Current repository status |
|                                          | `git commit -m "msg"`  | Make a commit with a message |
| [**`ltrace`**](https://tldr.inbrowser.app/pages/linux/ltrace) | | **Library call tracing** |
|                                          | `ltrace ./app`         | Show library function calls |
| [**`make`**](https://tldr.inbrowser.app/pages/common/make) | | **Automatic project build** |
|                                          | `make`                 | Run build using Makefile |
| [**`shellcheck`**](https://tldr.inbrowser.app/pages/common/shellcheck) | | **Check bash scripts for errors** |
|                                          | `shellcheck script.sh` | Analyze script for issues |
| [**`strace`**](https://tldr.inbrowser.app/pages/linux/strace) | | **System call debugging** |
|                                          | `strace ./app`         | Trace system calls on execution |
| [**`valgrind`**](https://tldr.inbrowser.app/pages/linux/valgrind) | | **Memory leak detection** |
|                                          | `valgrind ./app`       | Run memory check |
| [**`vim` / `nano`**](https://tldr.inbrowser.app/pages/common/vim) | | **Command-line editors** |
|                                          | `vim file.sh`          | Open file in `vim` |
|                                          | `nano file.sh`         | Open file in `nano` |

---

## 📌 Miscellaneous

| Command                                    | Example                 | Description |
| ------------------------------------------ | ----------------------- | ----------- |
| [**`cal`**](https://tldr.inbrowser.app/pages/linux/cal) | | **Calendar. Show current month** |
|                                            | `cal 2025`              | Calendar for all of 2025 |
|                                            | `cal 08 2025`           | Calendar for August 2025 |
| [**`date`**](https://tldr.inbrowser.app/pages/common/date) | | **Show current date and time** |
|                                            | `date +%T`              | Only current time |
|                                            | `date -d "next friday"` | Date of next Friday |
| [**`factor`**](https://tldr.inbrowser.app/pages/linux/factor) | | **Factor a number into primes** |
|                                            | `factor 100`            | Outputs: 2 2 5 5 |
| [**`man`**](https://tldr.inbrowser.app/pages/common/man) | | **Command help manual** |
|                                            | `man tar`               | Manual for the `tar` command |
|                                            | `man -k copy`           | Search for commands related to copying |
|                                            | `man 5 passwd`          | Description of `/etc/passwd` file format |
| [**`seq`**](https://tldr.inbrowser.app/pages/linux/seq) | | **Generate numeric sequences** |
|                                            | `seq 1 5`               | Output numbers from 1 to 5 |
|                                            | `seq 1 2 9`             | Output numbers with step 2: 1 3 5 7 9 |
|                                            | `seq -s ',' 1 5`        | Output numbers with separator: 1,2,3,4,5 |
| [**`yes`**](https://tldr.inbrowser.app/pages/common/yes) | | **Repeat a string endlessly** |
|                                            | `yes \| rm -r dir`      | Auto-confirm deletion |

---

## Additional resources

📘 **man pages** — detailed manuals for commands:

```bash
man ls
man rm
```

📙 **TLDR** — concise usage examples of popular commands:

🧠 **Tip:** Install `tldr` for cheat-sheet-style help:

```bash
sudo apt install tldr   # or: npm install -g tldr
tldr tar                # example of a short summary for the tar command
```

🌐 Useful links:

**Linux man pages online** — official manual pages, searchable by command name:  
[https://man7.org/linux/man-pages/](https://man7.org/linux/man-pages/)

**Simplified and community-driven man pages** — community-driven help pages with practical examples:  
[https://tldr.sh/](https://tldr.sh/)
