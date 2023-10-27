import sys
import paramiko
import click
from queue import Queue, Empty
import threading
import time

# Function to read the SSH channel output and look for the prompt to stop reading.
def read_output(channel, output_queue, prompt, prompt_count):
    counter = 0
    while True:
        if channel.recv_ready():
            # Receive the chunk and decode it to UTF-8
            output_chunk = channel.recv(4096).decode('utf-8')
            print(output_chunk, end='')

            # Split the chunk into lines to scan for prompt
            lines = output_chunk.split("\n")

            # Loop through lines to look for the prompt
            for line in lines:
                if prompt in line:
                    counter += 1
                    if counter >= prompt_count:
                        # Stop reading if the prompt appears a specified number of times
                        output_queue.put("Prompt detected.")
                        return

# CLI configuration using click
@click.command()
@click.option('--host', '-h', required=True, help='SSH Host (ip:port)')
@click.option('--user', '-u', required=True, help='SSH Username')
@click.option('--password', '-p', required=True, help='SSH Password')
@click.option('--cmds', '-c', default='', help='Commands to run, separated by comma')
@click.option('--invoke-shell', is_flag=True, help='Invoke shell before running the command [default=True]')
@click.option('--prompt', default='', help='Prompt to look for before breaking the shell')
@click.option('--prompt-count', default=1, help='Number of prompts to look for before breaking the shell')
@click.option('--timeout', '-t', default=5, help='Command timeout duration in seconds')
@click.option('--auto-add-policy', is_flag=True, default=True, help='Automatically add the host key [default=True]')
@click.option('--look-for-keys', is_flag=True, default=False, help='Look for local SSH key [default=False]')
@click.option('--inter-command-time', '-i', default=1, help='Inter-command time in seconds [default is 1 second]')
def ssh_client(host, user, password, cmds, invoke_shell, prompt, prompt_count, timeout, auto_add_policy, look_for_keys, inter_command_time):
    """
        SSH Client for running remote commands.

        Sample Usage:
        pysshpass -h "172.16.1.101" -u "cisco" -p "cisco" -c "term len 0,show users,show run,show cdp neigh,show int desc" --invoke-shell --prompt "#" --prompt-count 4 -t 15
        """
    # Initialize SSH client
    client = paramiko.SSHClient()

    # Set host key policy based on user input
    if auto_add_policy:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SSH server
    try:
        client.connect(host, username=user, password=password, look_for_keys=look_for_keys)
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"Could not establish SSH connection: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unhandled exception: {str(e)}")
        sys.exit(1)

    # Execute the SSH command in shell mode or directly
    if invoke_shell:
        # Invoking the shell
        try:
            channel = client.invoke_shell()
        except Exception as e:
            print(f"Failed to invoke shell: {str(e)}")
            sys.exit(1)

        # Initialize a queue to store output
        output_queue = Queue()

        # Start a thread to read the SSH channel output
        read_thread = threading.Thread(target=read_output, args=(channel, output_queue, prompt, prompt_count))
        read_thread.daemon = True
        read_thread.start()

        # Execute each command
        command_list = cmds.split(',')
        for cmd in command_list:
            channel.send(cmd + '\n')
            time.sleep(inter_command_time)  # Waiting between commands

        try:
            # Wait for a reason to exit (like a prompt detection), notice the timeout is applied here
            reason = output_queue.get(timeout=timeout)
            print(f"\nExiting: {reason}")
        except Empty:
            print("\nExiting due to timeout.")
            sys.exit()

        # Close the SSH channel
        channel.close()

    else:
        # Execute command and print the result
        stdin, stdout, stderr = client.exec_command(cmds)
        output = stdout.read().decode('utf-8')
        print(output)

    # Close the SSH client
    client.close()

# Entry point
if __name__ == '__main__':
    ssh_client()
