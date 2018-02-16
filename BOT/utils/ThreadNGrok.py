from threading import Thread
import subprocess
import time
from ngrok import NgrokAPI
from subprocess import Popen,check_output,PIPE
import logging
logger = logging.getLogger()
import traceback


class threadNgrok(Thread):

    def __init__(self,port,name,webhook):
        Thread.__init__(self)
        self.port = port
        self.API = NgrokAPI()
        self.name=name
        self.webhook = webhook

    def run(self):
        try:
            p = Popen(['ps', '-A'], stdout=PIPE)
            out, err = p.communicate()
            running=False
            for line in out.splitlines():
                if ("ngrok start --none") in line:
                    running=True
            if (running):
                try:
                    tunnel = self.API.tunnel.create(name="Webhook for bot on port " + self.port, proto="http",addr=self.port)
                    if (not self.webhook):
                        print("URL on the internet : "+tunnel.public_url)
                except:
                    print("Tunnel seems to be already up")
                #traceback.print_exc()
            else :
                pro = subprocess.Popen("ngrok start --none > /tmp/null &", shell=True)
                time.sleep(1)
                tunnel = self.API.tunnel.create(name="Webhook for bot on port " + self.port, proto="http", addr=self.port)
                print("URL on the internet : " + tunnel.public_url)
        except:
            print("NGrok isn't running due to an error")
