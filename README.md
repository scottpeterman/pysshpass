## pysshpass: A Multiplatform SSH Automation Utility

### Overview

`pysshpass` is a Python-based SSH client designed to offer a multiplatform alternative to `sshpass`. This utility aims to address two core challenges:

1. **Windows Compatibility**: Native `sshpass` options are limited on Windows, and `pysshpass` serves as a versatile replacement.
2. **Specialized Devices Support**: Network devices like PaloAlto Firewalls, Cloudgenix SD-WAN routers, and F5 load balancers often have unique command-line interfaces and large outputs, which are not fully supported by libraries like Netmiko.

### Key Features

- **Comma-Delimited Commands**: The utility allows for executing multiple commands in sequence, ideal for devices requiring a series of commands for configuration or data retrieval.
  
- **Prompt Controls**: The script supports custom prompts and prompt counts, offering more control over when to exit the shell. This is particularly useful for devices with multi-modal interfaces (e.g., F5's tmsh, bash, and imsh).

- **Timeout Management**: A timeout feature ensures that the utility doesn't hang while waiting for device responses, making it more robust and production-ready.

### Example usage

```commandline
pysshpass -h "172.16.1.101" -u "cisco" -p "cisco" -c "term len 0,show users,show run,show cdp neigh,show int desc" --invoke-shell --prompt "#" --
prompt-count 4 -t 15

Home Network on GNS3 - Where Scott Plays

usa1-rtr-1#term len 0
usa1-rtr-1#show users
    Line       User       Host(s)              Idle       Location
   0 con 0                idle                 10:38:21
*  2 vty 0     cisco      idle                 00:00:00 10.0.0.191

  Interface    User               Mode         Idle     Peer Address

usa1-rtr-1#show run
Building configuration...

Current configuration : 2137 bytes
!
! Last configuration change at 18:32:41 UTC Sun Oct 22 2023 by cisco
upgrade fpd auto
<output truncated>
```

### Use-Cases

This utility is particularly useful for:

- Automating tasks on devices with large configuration outputs
- Working with multi-modal command-line interfaces
- Gathering information during network audits, especially for devices not well-supported by existing automation libraries

---
### CLI Usage

```commandline
pysshpass --help
Usage: pysshpass [OPTIONS]

  SSH Client for running remote commands.

  Sample Usage: pysshpass -h "172.16.1.101" -u "cisco" -p "cisco" -c "term len
  0,show users,show run,show cdp neigh,show int desc" --invoke-shell --prompt
  "#" --prompt-count 4 -t 15

Options:
  -h, --host TEXT                 SSH Host (ip:port)  [required]
  -u, --user TEXT                 SSH Username  [required]
  -p, --password TEXT             SSH Password  [required]
  -c, --cmds TEXT                 Commands to run, separated by comma
  --invoke-shell                  Invoke shell before running the command
                                  [default=True]
  --prompt TEXT                   Prompt to look for before breaking the shell
  --prompt-count INTEGER          Number of prompts to look for before
                                  breaking the shell
  -t, --timeout INTEGER           Command timeout duration in seconds
  --auto-add-policy               Automatically add the host key
                                  [default=True]
  --look-for-keys                 Look for local SSH key [default=False]
  -i, --inter-command-time INTEGER
                                  Inter-command time in seconds [default is 1
                                  second]
  --help                          Show this message and exit.


```
---
### Function `read_output`

- This function reads the output of the SSH session in real-time and prints it to the standard output.
- It also checks for a user-defined prompt (e.g., `$`, `#`, etc.) to decide when to stop reading the output and exit the loop.

### Function `ssh_client`

- It accepts multiple command-line arguments, such as host, username, and password, using the `click` library.
- The `invoke_shell` flag specifies whether to create an interactive SSH session or just execute commands.
- The `prompt` and `prompt_count` options are useful when `invoke_shell` is set, allowing the script to break the shell after a specific number of prompts.

### Thread usage

- A daemon thread (`read_thread`) runs in the background to handle the reading of output from the SSH session.

### User Prompt Management

- The code uses a queue (`output_queue`) to communicate between the main function and the thread that reads the SSH output.
- A timer (`timeout`) ensures the script doesn't hang indefinitely waiting for a prompt.

---
