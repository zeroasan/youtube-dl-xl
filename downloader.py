import dl_info_service
import subprocess

def download(url, dist):
    print 'start downloading: ' + url
    try:
        process = subprocess.check_output(['youtube-dl', "-o downloads/video/%(uploader)s/%(title)s-%(id)s.%(ext)s", url], stderr=subprocess.STDOUT,shell=True)
    except subprocess.CalledProcessError as e:
        print "exception: " + e.output
    else:
        print 'xxx'


download("https://www.youtube.com/watch?v=HNOT_feL27Y", '')
