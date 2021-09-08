import json
import requests


def transliterate(text, reverse=False):
    symbols = (u"абвгдежзийклмнопрстуфхцчшщъыьюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdejzijklmnoprstufhzcss_y_uaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

    if reverse==True:
        tr = {ord(b):ord(a) for a, b in zip(*symbols)}
    else:
        tr = {ord(a):ord(b) for a, b in zip(*symbols)}
    return text.translate(tr)

def call_fast_api(data, endpoint, port=4990, action='GET', host = '127.0.0.1'):
    if not isinstance(data, str):
        data=json.dumps(data)
        
    api_url = f'http://{host}:{port}/{endpoint}'

    if action=='GET':
        response = requests.get(api_url, data=data)
    elif action=='POST':
        response = requests.post(api_url, data=data)
        
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return response