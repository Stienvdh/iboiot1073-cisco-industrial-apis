import requests, time, urllib3, os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

urllib3.disable_warnings()

load_dotenv()

device_ip = os.environ['DEVICE_IP']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

def get_vlans():
    # Craft RESTCONF request for list of VLANs
    url = f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native/interface/Vlan"
    response = requests.get(url,
                            auth=HTTPBasicAuth(username, password),
                            headers = {
                                "Accept" : "application/yang-data+json"
                            }, verify=False).json()

    # Parse and print RESTCONF response for VLAN number + description
    print('------------------')
    for vlan in response['Cisco-IOS-XE-native:Vlan']:
        if not 'description' in vlan:
            print(f"{vlan['name']}: No description")
        else:
            print(f"{vlan['name']}: {vlan['description']}")

if __name__ == "__main__":
    # Infinite loop executing RESTCONF GET requests
    while True:
        get_vlans()
        time.sleep(2)