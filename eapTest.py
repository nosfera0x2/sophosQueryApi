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


def eapSuccessEmail():

   config = configparser.ConfigParser()
   config.read('config.ini')
   mail_id = config['microsoft365']['client_id']
   mail_secret = config['microsoft365']['client_secret']
   credentials = (mail_id, mail_secret)
   mail_tenant_id = config['microsoft365']['tenant_id']
   account = Account(credentials, auth_flow_type='credentials', tenant_id=mail_tenant_id)
   account.authenticate()
   mail = account.new_message(resource='emailsendingfrom@email.domain')
   mail.to.add('emailsendingto@email.domain')
   mail.subject = 'EAP Email Test'
   mail.body = "This email is to infrom that device(s) in Early Access Program"
   mail.send()

if __name__ == '__main__':

   id = eapQuery()
   time.sleep(30)
   queryResult = getQueryResult(id) #looking at jsonResult["items"]
   print(queryResult)

   for d in queryResult:
       if d['data'] == 'BETA': #for each dictionary in items, look at 'data' key
           print("Device(s) in EAP")
           eapSuccessEmail()
           break
   
 
