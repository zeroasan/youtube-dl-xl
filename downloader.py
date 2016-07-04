import dl_info_service
import subprocess

def download(url, dist):
    print 'start downloading: ' + url
    process = subprocess.Popen(['youtube-dl', "-o c:/downloads/video/%(uploader)s/%(title)s-%(id)s.%(ext)s", url], stdout=subprocess.PIPE)
    process.wait()
    print 'xxx'


download("http://v.youku.com/v_show/id_XMTYyOTg3OTU2NA==?from=y1.3-dv-2016new-239-23143.225965.1-3", 'c:/video/')
