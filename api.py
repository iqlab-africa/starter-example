import requests
API_KEY = 'my4yJcvbVxiaqxxxomkzFVrBbv4oMIhLKy50epnO6P9snhRKFCC6GmajQPypPwvTdvkCAVCzU1TR57A8bMSIZWMnsSjEN3dmXKLaNlWd6aRqIDexjSJHpPBTPqDJJ57yo'
WORKSPACE_ID = '926b8a1c-1df9-4643-b253-739cab73e459'
PROCESS_ID = 'VideoSearch'
ENDPOINT_URL = "https://cloud.robocorp.com/api/v1/"

# APi's to use 
# 
def start():
    ''' Start Bot via API'''
    print('Call Video Bot via http: ')
    
    response = requests.get(f'{ENDPOINT_URL}')
