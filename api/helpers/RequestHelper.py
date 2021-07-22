import requests

class RequestHelper:

    @staticmethod
    def get(url, params=None):
        r = requests.get(url = url, params = params) 
        return r.json() 

    @staticmethod
    def post(url, data):
        r = requests.post(url = url, json = data)
        return r.json()

    @staticmethod
    def download(url, path, params=None):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
