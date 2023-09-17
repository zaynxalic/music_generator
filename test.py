import requests

LANG = "en"
VIDEOID
url = f'http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}'


headers = {
    'User-Agent': 'Mozilla/5.0',
    
}

data = {
    "s" : "PAPISM",
    "offset" : "0",
    "limit" : "1",
    "type" : "1",
}

response = requests.post(url, headers=headers, data=data)

print(response.text)