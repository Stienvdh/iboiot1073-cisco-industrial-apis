from netmiko import ConnectHandler
from dotenv import load_dotenv
import os

load_dotenv()

device_ip = os.environ['DEVICE_IP']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

if __name__ == "__main__":
    vlan_number = input("Enter VLAN number to delete: ")

    # Connect to network device
    device = {
        "device_type": "cisco_ios",
        "host": device_ip,
        "username": username,
        "password": password
    }
    net_connect = ConnectHandler(**device)

    # Issue CLI commands to delete given VLAN
    net_connect.enable()
    net_connect.send_command(f"conf t", expect_string='#')
    net_connect.send_command(f"no int vlan {vlan_number}", expect_string='#')
    net_connect.disconnect()