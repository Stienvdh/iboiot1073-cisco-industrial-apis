import auth, requests, json, os
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings()

load_dotenv()

x_tenant_id = os.environ["TENANT_ID"]
cluster_url = "eu.ciscoiot.com"
device_eid = os.environ["DEVICE_EID"]

def get_devices():
    # 1. Craft API payload and request
    url = f"https://{cluster_url}/nbapi/edm/v1/devices"
    response = requests.get(
        url,
        headers={
            "Accept" : "application/json",
            "x-tenant-id" : x_tenant_id,
            "Authorization" : f"Bearer {auth.get_access_token()}"
        }
    )
    # Parse API request output
    print(json.dumps(response.json(), indent=2))

def set_device_name(name):
    # 1. Craft API payload and request
    url = f"https://{cluster_url}/nbapi/edm/v1/devices"
    payload = '''[{
        "eid" : ''' + f"\"{device_eid}\"" + ''',
        "fields": {
            "field:name": ''' + f"\"{name}\"" + '''
        }
    }]'''

    # 2. Execute API request
    response = requests.put(
        url,
        headers={
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "x-tenant-id" : x_tenant_id,
            "Authorization" : f"Bearer {auth.get_access_token()}"
        }, data = payload
    )
    if int(response.status_code) == 200:
        print("Succesfully updated device name!")

if __name__ == "__main__":
    name_to_set = input("Enter a new name for your device: ")
    set_device_name(name_to_set)