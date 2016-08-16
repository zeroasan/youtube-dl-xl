import os

path = os.path.expanduser('C:\work\99-Temp\Task_pics')
print path


ydl_option = {
    'writethumbnail' : True,
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': ''
}


ydl_option['outtmpl'] = 'C:\work\99-Temp\Task_pics'
print ydl_option['outtmpl']