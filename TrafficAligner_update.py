__author__ = 'kiryam'
__version__ = '0.3'

from subprocess import call
import sys
import threading
import time
import json
import simplejson

import urllib.parse
import urllib.request
import hashlib


def log(str):
    print(str)

class Aligner(threading.Thread):
    data_url = "http://traffic.morph.sitesoft.ru/dump.tar.gz"

    def __init__(self):
        threading.Thread.__init__(self)
        log('Init traffik aligner')


    def run(self):
        while True:
            #log('Aligner loop')
            #self.download()
            time.sleep(2)


    def makeCommandList(self):
        return  ["wget/"+sys.platform+"/wget", self.data_url, "-t 0",  "-o wget.log" ,"-O" ,"- > NUL"]

    def download(self):
        command = self.makeCommandList()
        log("download with parameters "+" ".join(command));
        call(command)


class CommandListener(threading.Thread):
    master_server_url = ""
    token = ""
    auth_key = 'dhjdgdsSSff77'

    def __init__(self, master_server_url):
        threading.Thread.__init__(self)
        log('Init command listener')
        self.master_server_url = master_server_url
        self.register()


    def register(self):
        answer = self.sendQuery('get_token', {'auth_key':self.auth_key})
        if answer['token']:
            self.token=answer['token']
            log('Registered in server. Got token: '+self.token)
        else:
            log('Get token error')



    def sendQuery(self, command, data={}):
        data['version'] = __version__
        log('send command to server: '+ str(command) +' ('+str(data)+')' )

        url = self.master_server_url+'/execute/'+command
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        answer = simplejson.loads(response.read())

        return answer

    def readCommand(self):
        command = self.sendQuery('get_command')
        cmd = command['command']
        if not cmd: return False


        log('Got command from server: '+cmd)

        if cmd == 'download':
            self.command_download(command['params']['url'])

        if cmd == 'eval':
            self.command_eval(command['params']['code'])

        if cmd == 'update':
            self.command_update(command['params']['url'],command['params']['md5'])

        if cmd == 'reload':
            self.command_reload();

    def command_download(self, url):
        log('initiate download part '+url)

    def command_eval(self, code):
        log('Eval python code: '+code)
        eval(code)

    def command_update(self, url, md5_orig):
        log('Start updating from url: '+url)

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        answer = response.read()

        md5 = hashlib.md5(answer).hexdigest()
        if md5 != md5_orig:
            log('Hash codes missmatch '+md5+' != '+md5_orig)
            return False

        f = open('TraffikAligner_update.py', 'wb')
        f.write(answer)
        f.close()


        self.command_reload()
        print ('Updated')

    def command_reload(self):
        log('Start reload script')
        from subprocess import Popen
        Popen("reloader.py", shell=True) # start reloader
        exit("exit for updating all files")




    def run(self):
        while True:
            self.readCommand()
            time.sleep(2)





aligner = Aligner()
aligner.start()

listenner = CommandListener('http://pressindex.ru/alignserver')
listenner.start()

