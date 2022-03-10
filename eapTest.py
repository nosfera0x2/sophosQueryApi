import requests
import sys
import json
import oauth_central 
import configparser
import time


config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['sophosCentral']['client_id']
client_secret = config['sophosCentral']['client_secret']

jwt, tenant_id, tenant_type, data_region = oauth_central.Authenticate.auth(client_id,client_secret)


def eapQuery():
  
    requestUrl = f"{data_region}/live-discover/v1/queries/runs"

    requestHeaders = {

                "Authorization": f'Bearer {jwt}',
                'X-Tenant-ID': f'{tenant_id}'
                    
            }
            
    requestData = {
        
        "matchEndpoints": {

            "all": True
            #"filters": [{"type": ["computer"]}],
            #"filters": [{"type": ["server"]}]

        },
        "adHocQuery": {
            "name": "Test-Query",
            "template": "SELECT data FROM registry WHERE path LIKE 'HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Sophos\\AutoUpdate\\Service\\CloudSubscriptions\\Base\\tag'"
        }
    }

    data = json.dumps(requestData, indent=2)

    r = requests.post(requestUrl, headers=requestHeaders, data=data)

    result = r.json()

    return result['id']
   
def getQueryResult(id):
    
    time.sleep(45)

    requestUrl = f"{data_region}/live-discover/v1/queries/runs/{id}/results?maxSize=1000"
  
    requestHeaders = {


                "Authorization": f'Bearer {jwt}',
                "Content-Type": "application/json",
                'X-Tenant-ID': f'{tenant_id}'
                    
            }
    r = requests.get(requestUrl, headers=requestHeaders)

    jsonResult = r.json()
    return jsonResult["items"]


if __name__ == '__main__':

   id = eapQuery()
   time.sleep(10)
   queryResult = getQueryResult(id)

   for d in queryResult:
       if d['data'] == 'BETA':
           print("Device(s) in EAP")
           break
 
