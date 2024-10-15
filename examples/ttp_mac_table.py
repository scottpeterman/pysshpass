# Requires tablulate
# pip install tabulate

import traceback
from time import sleep
from PySSHPass.pysshpass import SSHClientWrapper
from PySSHPass.helpers.ttp_helper import TTPParserHelper
from tabulate import tabulate  # Import tabulate for CLI table output

def test_ssh_client_with_ttp():
    # Replace with appropriate SSH credentials and commands
    ssh_client = SSHClientWrapper(
        host="172.16.101.1",
        user="cisco",
        password="cisco",
        invoke_shell=True,
        prompt="",  # Empty prompt to dynamically find the prompt
        prompt_count=3,
        timeout=5,
        delay=0.5,
        quiet=True
    )

    # Connect to the device
    ssh_client.connect()

    # Dynamically find the prompt if not specified
    if not ssh_client.prompt:
        detected_prompt = ssh_client.find_prompt(ends_with=('#', '>'))
        if detected_prompt:
            print(f"Detected prompt: {detected_prompt}")
        else:
            print("Failed to detect prompt. Proceeding without prompt detection.")

    # Step 1: Run the 'show version' command
    ssh_client.cmds = "term len 0,show version"
    version_output = ssh_client.run_commands()

    # Step 2: Use TTP to parse the version output
    version_template_file = './templates/ios_xe_virtual_show_version.ttp'  # Path to the TTP template for show version
    version_parser = TTPParserHelper(ttp_template_file=version_template_file)
    parsed_version = version_parser.parse(version_output)

    # Display parsed version output in a table format
    print("Parsed Version Output:")
    version_table = [[k, v] for k, v in parsed_version[0].items()]
    print(tabulate(version_table, headers=["Field", "Value"], tablefmt="pretty"))

    try:
        if parsed_version[0]['platform'] == 'vios_l2':
            # Step 3: Run the 'show mac address-table' command
            ssh_client.prompt_count = 1  # Adjust the prompt count for this command
            ssh_client.cmds = "show mac address-table"
            mac_output = ssh_client.run_commands()

            # Step 4: Use TTP to parse the mac table output
            mac_template = './templates/ios_xe_virtual_show_mac.ttp'
            mac_parser = TTPParserHelper(ttp_template_file=mac_template)
            parsed_mac_table = mac_parser.parse(mac_output)

            # Display parsed mac table output in a table format
            print("Parsed MAC Table Output:")
            mac_table = []
            for entry in parsed_mac_table[0]:
                row = [entry['vlan_id'], entry['mac_address'], entry['interface']]
                mac_table.append(row)
            print(tabulate(mac_table, headers=["VLAN", "MAC Address", "Interface"], tablefmt="grid"))

        else:
            print(f"Unable to verify platform")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()

    # Close the connection
    ssh_client.close()

if __name__ == "__main__":
    test_ssh_client_with_ttp()
