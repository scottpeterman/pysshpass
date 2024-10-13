from PySSHPass.pysshpass import SSHClientWrapper

def test_ssh_client():
    # Replace with appropriate SSH credentials and commands
    ssh_client = SSHClientWrapper(
        host="172.16.101.100",
        user="cisco",
        password="cisco",
        cmds="term len 0,show users,,",
        invoke_shell=True,
        prompt="#",
        prompt_count=2,
        timeout=15,
        delay=.5
    )

    ssh_client.connect()

    # Run the first batch of commands
    output = ssh_client.run_commands()  # Runs the commands and returns the output
    print(output)

    print("-------- next commands --------------")

    # Update commands for the second batch
    ssh_client.prompt_count = 3
    ssh_client.cmds = "show users,show users,,"

    # Run the second batch of commands
    output = ssh_client.run_commands()
    print(output)

    # Close the connection
    ssh_client.close()

if __name__ == "__main__":
    test_ssh_client()
