import json, os

def get_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def set_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def set_vlan(vlan_number, vlan_description):
    # Craft RESTCONF request to create VLAN
    # url = f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native/interface/Vlan"
    
    vlans = {"Cisco-IOS-XE-native:Vlan":[{'name': vlan_number, 'description': vlan_description}]}

    # requests.patch(url,
    #                 auth=HTTPBasicAuth(username, password),
    #                 headers = {
    #                     "Accept" : "application/yang-data+json",
    #                     "Content-Type" : "application/yang-data+json"
    #                 }, data=json.dumps(vlans), verify=False)

    current_vlans = get_json('vlan_response.json')['Cisco-IOS-XE-native:Vlan']
    new_vlans = {'Cisco-IOS-XE-native:Vlan': current_vlans + vlans['Cisco-IOS-XE-native:Vlan']}
    set_json('vlan_response.json', new_vlans)

if __name__ == "__main__":
    vlan_number = input("Enter a VLAN number: ")
    vlan_decsription = input("Enter a VLAN description: ")
    set_vlan(vlan_number, vlan_decsription)