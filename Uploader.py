import requests
import logging

sessionCookies = None

def login(url, username, password):
    payload = {'username': username, 'password': password}
    resp = requests.post(url, data=payload);
    global sessionCookies
    sessionCookies = resp.cookies

def uploadFile(url, fileName, filePath, fileInfo):
    files = {'file': open(filePath, 'rb')}
    resp = requests.post(url, cookies=sessionCookies, files=files, data=fileInfo)
    logging.info('[Uploader] Upload file [%s] completed.', fileName)
