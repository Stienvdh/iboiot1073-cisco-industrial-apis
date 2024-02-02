import json, os
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings()

load_dotenv()

# x_tenant_id = os.environ["TENANT_ID"]
# cluster_url = "eu.ciscoiot.com"
# device_eid = os.environ["DEVICE_EID"]

def get_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def set_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def get_devices():
    # url = f"https://{cluster_url}/nbapi/edm/v1/devices"
    # response = requests.get(
    #     url,
    #     headers={
    #         "Accept" : "application/json",
    #         "x-tenant-id" : x_tenant_id,
    #         "Authorization" : f"Bearer {auth.get_access_token()}"
    #     }
    # )
    response = get_json('response.json')
    print(json.dumps(response, indent=2))

def set_device_name(name):
    # url = f"https://{cluster_url}/nbapi/edm/v1/devices"
    # payload = '''[{
    #     "eid" : "DUMMY_DEVICE",
    #     "fields": {
    #         "field:name": "setbyapi"
    #     }
    # }]'''

    # response = requests.put(
    #     url,
    #     headers={
    #         "Accept" : "application/json",
    #         "Content-Type" : "application/json",
    #         "x-tenant-id" : x_tenant_id,
    #         "Authorization" : f"Bearer {auth.get_access_token()}"
    #     }, data = payload
    # )

    devices = get_json('response.json')
    devices['results'][0]['name'] = name
    set_json('response.json', devices)
    

if __name__ == "__main__":
    get_devices()