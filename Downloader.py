import threading
import thread
from subprocess import call
import sys
import time

from utilites import log

class Downloader(threading.Thread):
    data_url = ""

    def __init__(self, data_url):
        threading.Thread.__init__(self)
        log('Init downloader')
        self.data_url = data_url


    def run(self):
        self.download()

        while True:
            #log('Aligner loop')
            #self.download()
            log('Wait for download in Thread '+ str(threading.current_thread()))
            time.sleep(2)


    def makeCommandList(self):

        end_file = '- > NUL'
        if sys.platform == 'darwin':
            end_file = 'download_'+str(threading.current_thread())+'.out'

        return  ["wget/"+sys.platform+"/wget", self.data_url, "-t 0",  "-o wget.log" ,"-O" ,end_file]

    def download(self):
        if not self.data_url:
            log('Data url is null')
            return False

        command = self.makeCommandList()

        def _download_process():
            log("download with parameters "+" ".join(command));
            call(command)

        thread.start_new_thread(_download_process, () )

