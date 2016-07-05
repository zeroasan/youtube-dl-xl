import dl_info_service
import subprocess
import threading
import time

def download(url, dist):
    print 'start downloading: ' + url
    try:
        process = subprocess.check_output(['youtube-dl', "-o downloads/video/%(uploader)s/%(title)s-%(id)s.%(ext)s", url], stderr=subprocess.STDOUT,shell=True)
    except subprocess.CalledProcessError as e:
        print "exception: " + e.output
    else:
        print 'xxx'


#download("https://www.youtube.com/watch?v=HNOT_feL27Y", '')
#download("http://v.youku.com/v_show/id_XMTYyOTg3OTU2NA==?from=y1.3-dv-2016new-239-23143.225965.1-3", '')
download("http://www.baidu.com", '')
print 'after download'
