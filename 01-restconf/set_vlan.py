import requests, urllib3, json, os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

urllib3.disable_warnings()

load_dotenv()

device_ip = os.environ['DEVICE_IP']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

def set_vlan(vlan_number, vlan_description):
    # Craft RESTCONF request to create VLAN
    url = f"https://{device_ip}/restconf/data/Cisco-IOS-XE-native:native/interface/Vlan"
    vlans = {"Cisco-IOS-XE-native:Vlan":[{'name': vlan_number, 'description': vlan_description}]}
    requests.patch(url,
                    auth=HTTPBasicAuth(username, password),
                    headers = {
                        "Accept" : "application/yang-data+json",
                        "Content-Type" : "application/yang-data+json"
                    }, data=json.dumps(vlans), verify=False)

if __name__ == "__main__":
    vlan_number = input("Enter a VLAN number: ")
    vlan_decsription = input("Enter a VLAN description: ")
    set_vlan(vlan_number, vlan_decsription)