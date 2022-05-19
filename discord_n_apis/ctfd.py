import requests
import random
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict



def register_user(user):
    # domain = 'http://localhost:4000/'
    domain = 'https://ctf.devclub.in/'
    res = requests.get(domain)
    tex = bs(res.content).find_all('script')[0].text
    nonce = json.loads(tex[tex.find('{'):tex.find('}')+1].strip().replace('\t','').replace("'",'"'))['csrfNonce']
    sessCookie = res.headers['Set-Cookie'][:res.headers['Set-Cookie'].find(';')]

    url = f"{domain}registerfa833321nds"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["Accept-Language"] = "en-GB,en;q=0.9"
    headers["Cache-Control"] = "max-age=0"
    headers["Connection"] = "keep-alive"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    headers["Cookie"] = sessCookie#"session=3c687d64-e4ed-4624-a7e8-6f5b990ae61d.6sU5FNd9MmYkiOyj-O83svUulGU"
    headers["Origin"] = "http://127.0.0.1:4000"
    headers["Referer"] = "http://127.0.0.1:4000/login"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "same-origin"
    headers["Sec-Fetch-User"] = "?1"
    headers["Sec-GPC"] = "1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"

    name = user['name']#f'TestUser{i}'
    email = user['email']#f'testuser{i}@gmail.com'
    #generate random password
    import string
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    phone_number = user['phone_num']
    user['password'] = password
    data = f"name={name}&email={email}&password={password}&nonce={nonce}&fields%5B1%5D={phone_number}&registration_code=qnrobuv4qan8pzzclftv&_submit=Submit"
    

    resp = requests.post(url, headers=headers, data=data)

    print(resp.status_code)
    return user['password']