#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

import requests
import os

loginURL = 'http://docs.python-requests.org/en/latest/user/quickstart/'
r = requests.get(loginURL)
#cookies = r.cookies

print r.content

url = 'http://jigsaw.w3.org/css-validator/validator'

path = os.path.dirname(os.path.realpath(__file__)) + '\\'
file_path = path + 'data\\testStyle.css'

print file_path

files = {'file': open(file_path, 'rb')}
#response = requests.post(url, files=files, cookies=cookies)

response = requests.post(url, files=files)
print response.content
