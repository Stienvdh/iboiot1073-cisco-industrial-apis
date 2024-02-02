import requests, os, urllib3
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

urllib3.disable_warnings()

load_dotenv()

cluster_url = "eu.ciscoiot.com"
api_secret = os.environ['API_SECRET']
api_id = os.environ['CLIENT_ID']
tenant_name = os.environ['TENANT_NAME']

def get_access_token():
    url = f"https://{cluster_url}/iam/auth/token"
    response = requests.post(
        url,
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        },
        json={
            "client_id": f"{tenant_name}->{api_id}",
            "client_secret": api_secret,
            "grant_type": "client_credentials"
        }
    )
    return response.json()['access_token']
    