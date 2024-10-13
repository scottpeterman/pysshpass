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
        quiet=True
    )

    # Connect to the device
    ssh_client.connect()

    # Step 1: Run the 'show version' command
    ssh_client.cmds = "term len 0,show version"
    version_output = ssh_client.run_commands()

    # print("Show Version Output:\n", version_output)

    # Step 2: Use TTP to parse the version output
    version_template_file = './templates/show_version.ttp'  # Path to the TTP template for show version
    version_parser = TTPParserHelper(ttp_template_file=version_template_file)
    parsed_version = version_parser.parse(version_output)
    print("Parsed Version Output:\n", parsed_version)

    # Step 3: Run the 'show inventory' command
    ssh_client.prompt_count = 1
    ssh_client.cmds = "show inventory"
    # ssh_client.
    inventory_output = ssh_client.run_commands()
    # print("Show Inventory Output:\n", inventory_output)

    # Step 4: Use TTP to parse the inventory output
    inventory_template_file = './templates/show_inventory.ttp'  # Path to the TTP template for show inventory
    inventory_parser = TTPParserHelper(ttp_template_file=inventory_template_file)
    parsed_inventory = inventory_parser.parse(inventory_output)
    print("Parsed Inventory Output:\n", parsed_inventory)

    # Close the connection
    ssh_client.close()

if __name__ == "__main__":
    test_ssh_client_with_ttp()
