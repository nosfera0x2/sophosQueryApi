# sophosQueryApi

This python script will connect to Sophos Central API, run live discover query to look for registry key signifying that device is in BETA ('EAP'). 
It will then connect to an M365 account, to send an email to inform the recipient, that device(s) are in EAP. 
