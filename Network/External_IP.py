import requests

def Get_IP():

    try:
        r = requests.get(r'http://jsonip.com')
        ip = r.json()['ip']
        return ip
    except requests.exceptions.ConnectionError:
        return "no connection found"
