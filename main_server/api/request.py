import requests
apiURL = 'http://localhost:8124'

def callGet(path='', params=None):
    response = requests.get(apiURL + path, params)
    print(response)
    return response.json()
