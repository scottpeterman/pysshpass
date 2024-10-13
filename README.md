# pysshpass: A Multiplatform SSH Automation Utility

### Overview

`pysshpass` is a Python-based SSH client designed to offer a multiplatform alternative to `sshpass`. It aims to address two key challenges:

1. **Windows Compatibility**: Native `sshpass` options are limited on Windows. `pysshpass` serves as a versatile replacement.
2. **Specialized Devices Support**: Network devices like Palo Alto Firewalls, CloudGenix SD-WAN routers, and F5 load balancers often have unique command-line interfaces and large outputs, which are not fully supported by libraries like Netmiko.
3. **Vendor and OS Agnostic**: Whether you're managing Cisco, Aruba, Palo Alto, or other network devices, `pysshpass` allows seamless automation and parsing, making it ideal for mixed-vendor environments.

### Key Features

- **Comma-Delimited Commands**: Execute multiple commands in sequence using comma-separated values.
- **Prompt Controls**: The script supports custom prompts and prompt counts, offering precise control over when to exit the shell.
- **Timeout Management**: A timeout feature ensures that the utility doesn't hang while waiting for device responses.
- **Quiet Mode**: A `quiet` flag suppresses printed output when running as a library, but retains output in CLI mode.
- **Cross-Platform**: Works across Linux, macOS, and Windows.

### Example CLI Usage

```bash
pysshpass -h "172.16.1.101" -u "cisco" -p "cisco" -c "term len 0,show users,show run" --invoke-shell --prompt "#" --prompt-count 4 -t 15
```

This command runs multiple commands in sequence on an SSH device (IOS), waits for four prompts, and applies a 15-second timeout.

### Use Cases

- Automating tasks on network devices with large configuration outputs.
- Managing multi-modal command-line interfaces.
- Gathering information during network audits.
- Mixed vendor network environment tooling.
- Linux or IoT automation.

---

## CLI Usage

```bash
pysshpass --help
Usage: pysshpass [OPTIONS]

  SSH Client for running remote commands.

Options:
  -h, --host TEXT                   SSH Host (ip:port) [required]
  -u, --user TEXT                   SSH Username [required]
  -p, --password TEXT               SSH Password
  -c, --cmds TEXT                   Commands to run, separated by comma
  --invoke-shell/--no-invoke-shell  Invoke shell before running the command
                                    [default=True]
  --prompt TEXT                     Prompt to look for before breaking the shell
  --prompt-count INTEGER            Number of prompts to look for before breaking the shell
  -t, --timeout INTEGER             Command timeout duration in seconds [default=360]
  --disable-auto-add-policy         Disable automatically adding the host key [default=False]
  --look-for-keys                   Look for local SSH key [default=False]
  -d, --delay FLOAT                 Delay between sending commands in seconds [default=0.5]
  --quiet                           Suppress output when running as a library
  --help                            Show this message and exit.
```

### Flags Explanation

- `--host`: SSH target (IP or hostname).
- `--user`: SSH username.
- `--password`: SSH password (can be skipped if `PYSSH_PASS` environment variable is set).
- `--cmds`: Comma-separated commands to run.
- `--invoke-shell`: Create an interactive SSH session (default is `True`).
- `--prompt`: Specify the shell prompt to look for.
- `--prompt-count`: How many times the prompt should be matched before breaking the shell.
- `--timeout`: Duration in seconds before the command times out.
- `--disable-auto-add-policy`: Disable the auto-add of SSH keys.
- `--look-for-keys`: Enable local key lookup for SSH authentication.
- `--delay`: Time delay between sending commands.
- `--quiet`: Suppress output when running as a library.

---

### Environment Variable Support for Passwords

For added convenience and security, `pysshpass` allows you to provide the SSH password through an environment variable, avoiding the need to pass it directly via the command line.

- Set the environment variable `PYSSH_PASS` to the desired password:

```bash
export PYSSH_PASS="yourpassword"
```

- If the `--password` option is omitted, `pysshpass` will automatically check for the `PYSSH_PASS` environment variable. This feature is especially useful when running automation scripts where you want to avoid exposing sensitive credentials in the command history.

### Example:

```bash
export PYSSH_PASS="cisco"
pysshpass -h "172.16.101.100" -u "cisco" -c "show version,show inventory" --invoke-shell --prompt "#" --prompt-count 3 -t 10
```

If a password is provided both in the environment variable and the command-line option, the command-line value will take precedence.

---

## More Usage Examples

### 1. Cisco Router

```bash
pysshpass -h "192.168.1.1" -u "admin" -p "password" -c "terminal length 0,show version" --invoke-shell --prompt "#" --prompt-count 3 -t 10
```

### 2. Aruba Switch

```bash
pysshpass -h "192.168.1.2" -u "admin" -p "password" -c "no paging,show interfaces brief" --invoke-shell --prompt ">" --prompt-count 2 -t 10
```

### 3. Palo Alto Firewall

```bash
pysshpass -h "192.168.1.3" -u "admin" -p "password" -c "set cli pager off,show system info,," --invoke-shell --prompt ">" --prompt-count 2 -t 10
```

---

### Library Usage

In addition to being used as a CLI tool, `pysshpass` can also be used as a library:

```python
from PySSHPass.pysshpass import SSHClientWrapper

def automate_device():
    ssh_client = SSHClientWrapper(
        host="192.168.1.1",
        user="admin",
        password="password",
        cmds="show version",
        invoke_shell=True,
        prompt="#",
        prompt_count=1,
        timeout=10,
        quiet=True  # Suppress output
    )
    
    ssh_client.connect()
    output = ssh_client.run_commands()
    ssh_client.close()
    return output
```

### Quiet Mode

The `--quiet` flag suppresses printed output, making it useful for script-based automation where log files are preferred over console output.

---

## Appendix A: Example Using TTP with `pysshpass`

This appendix provides a detailed example of how to use the `pysshpass` library with a TTP (Template Text Parser) helper to parse structured output from network devices. This example demonstrates how to run incremental SSH commands, gather output, and parse it using TTP templates for structured data extraction.

### Overview

In this example, the `SSHClientWrapper` class is used to:
1. Connect to a Cisco router.
2. Execute the `show version` command and parse the version information using a TTP template.
3. Execute the `show inventory` command and parse the inventory details.

The `TTPParserHelper` class is a utility that loads TTP templates and parses raw SSH output into structured data.

### Script Example

```python
from time import sleep
from PySSHPass.pysshpass import SSHClientWrapper
from PySSHPass.helpers.ttp_helper import TTPParserHelper

def test_ssh_client_with_ttp():
    # Replace with appropriate SSH credentials and commands
    ssh_client = SSHClientWrapper(
        host="172.16.101.100",
        user="cisco",
        password="cisco",
        invoke_shell=True,
        prompt="#",
        prompt_count=3,
        timeout=5,
        delay=0.5,
        quiet=True  # Suppress console output in quiet mode
    )

    # Step 1: Connect to the device
    ssh_client.connect()

    # Step 2: Run 'show version' command and capture output
    ssh_client.cmds = "term len 0,show version"
    version_output = ssh_client.run_commands()

    # Step 3: Parse the 'show version' output using TTP
    version_template_file = './templates/show_version.ttp'  # Path to the TTP template for show version
    version_parser = TTPParserHelper(ttp_template_file=version_template_file)
    parsed_version = version_parser.parse(version_output)
    print("Parsed Version Output:\n", parsed_version)

    # Step 4: Run 'show inventory' command and capture output
    ssh_client.prompt_count = 1
    ssh_client.cmds = "show inventory"
    inventory_output = ssh_client.run_commands()

    # Step 5: Parse the 'show inventory' output using TTP
    inventory_template_file = './templates/show_inventory.ttp'  # Path to the TTP template for show inventory
    inventory_parser = TTPParserHelper(ttp_template_file=inventory_template_file)
    parsed_inventory = inventory_parser.parse(inventory_output)
    print("Parsed Inventory Output:\n", parsed_inventory)

    # Step 6: Close the

 connection
    ssh_client.close()

if __name__ == "__main__":
    test_ssh_client_with_ttp()
```

### Key Components

1. **SSHClientWrapper**: 
   - Manages the SSH connection and command execution.
   - `invoke_shell=True` enables interactive sessions, necessary for running multiple commands like `show version` and `show inventory`.
   - The `quiet=True` flag suppresses verbose output during library usage.

2. **TTPParserHelper**:
   - Parses SSH output using predefined TTP templates.
   - In this example, the `show_version.ttp` and `show_inventory.ttp` templates are used to extract structured data from the device output.

---

### TTP Templates

To parse the output, we need two TTP templates: one for the `show version` command and one for the `show inventory` command. Below are examples of these templates:

#### 1. TTP Template for `show version`
**File: `show_version.ttp`**
```ttp
Version: {{ version }}
```

This template extracts the version information from the output of the `show version` command.

#### 2. TTP Template for `show inventory`
**File: `show_inventory.ttp`**
```ttp
NAME: "{{ inventory_name }}", DESCR: "{{ description }}"
PID: {{ product_id }}, VID: {{ version_id }}, SN: {{ serial_number }}
```

This template extracts details from the `show inventory` command, such as the product ID, version ID, and serial number.

---

## Appendix B: Build Instructions

To build and test `pysshpass` locally, follow the steps below:

### Step 1: Install Build Tools

Before you can build the package, ensure that `setuptools` and `wheel` are installed:

```bash
pip install setuptools wheel
```

### Step 2: Build the Package

To build the wheel file, run the following command:

```bash
python setup.py bdist_wheel
```

This will generate a `.whl` file in the `dist/` directory.

### Step 3: Test the Wheel Locally

To test the built package locally, run:

```bash
pip install dist/pysshpass-0.2.0-py3-none-any.whl
```

### Step 4: Upload the Package to TestPyPI

For testing purposes, you can upload the wheel to TestPyPI:

```bash
pip install twine
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### Step 5: Upload the Package to PyPI

Once satisfied with testing, upload the package to PyPI:

```bash
twine upload dist/*
```

Make sure to configure your credentials in `~/.pypirc` for automated authentication.

---

## License

PySSHPass is licensed under the **GNU General Public License v3 (GPLv3)**. For more details, see the [LICENSE](LICENSE) file.
