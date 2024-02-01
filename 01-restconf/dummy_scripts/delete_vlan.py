import json

def get_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def set_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def delete_vlan(vlan_number):
    current_vlans = get_json('vlan_response.json')['Cisco-IOS-XE-native:Vlan']
    new_vlans = []
    for vlan in current_vlans:
        if vlan['name'] != vlan_number:
            new_vlans += [vlan]
    new_vlan_response = {'Cisco-IOS-XE-native:Vlan': new_vlans}
    set_json('vlan_response.json', new_vlan_response)

if __name__ == "__main__":
    # vlan_number = input("Enter VLAN number to delete: ")

    # Connect to network device
    # device = {
    #     "device_type": "cisco_ios",
    #     "host": device_ip,
    #     "username": username,
    #     "password": password
    # }
    # net_connect = ConnectHandler(**device)
    # Issue CLI commands to delete given VLAN
    # net_connect.enable()
    # net_connect.send_command(f"conf t", expect_string='#')
    # net_connect.send_command(f"no int vlan {vlan_number}", expect_string='#')
    # net_connect.disconnect()
    
    vlan_number = input("Enter VLAN number to delete: ")
    delete_vlan(vlan_number)