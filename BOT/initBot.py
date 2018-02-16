"""initBot

Usage:
  initBot.py create
  initBot.py delete <name>
  initBot.py run <name> <port>
  initBot.py launch <name> <port>
  initBot.py reload <name>
  initBot.py stop <name>
  initBot.py <name> info
  initBot.py list
  initBot.py status
  initBot.py install


Options:
  -h --help     Show this screen.
  -V --version  Show version

"""

from __future__ import print_function
from ciscosparkapi import CiscoSparkAPI
from utils.CreateBot import ApplicationAPI, Application
from jinja2 import Environment, FileSystemLoader
import os, errno
from docopt import docopt
from utils.ThreadNGrok import threadNgrok
import time
from subprocess import Popen,check_output,PIPE
import requests
import json
import traceback
import psutil
from ngrok import NgrokAPI
import shutil




env = Environment(loader=FileSystemLoader('Templates'))

def CreateBot(name,email,logo,api):
    ciscoapi = ApplicationAPI(api._session)
    try:
        bot = ciscoapi.create(name, email, "bot",logo)
        return bot
    except:
        print("This isn't working, sorry. This might be because the bot name or email are already used!")
        return "error"


def InitBot():
    UserToken = str(raw_input("Please enter your CiscoSpark access token : "))
    BotName = str(raw_input("Please enter the bot name : "))
    BotEmailDef=BotName+"@sparkbot.io"
    BotEmail = str(raw_input("Please enter the bot email (default : "+BotEmailDef+") : "))
    if (BotEmail==""):
        BotEmail=BotEmailDef
    BotLogoDef = "http://i.imgur.com/HQTF5FK.png"
    BotLogo = str(raw_input("Please enter the bot logo (default : http://i.imgur.com/HQTF5FK.png) : "))
    if (BotLogo==""):
        BotLogo=BotLogoDef
    isAPI = str(raw_input("Do you want your bot to be integrated with API.AI ? [y/n] : "))
    while (isAPI!="y"and isAPI!="n"):
        isAPI = str(raw_input("Do you want your bot to be integrated with API.AI ? [y/n] : "))
    print("Creating your bot ...")
    api = CiscoSparkAPI(UserToken)
    #try :
    bot = CreateBot(BotName,BotEmail,BotLogo,api)
    if (bot!="error"):
        print("Creating your test room ...")
        TestRoom = api.rooms.create('Test room for your bot : ' + bot.name)
        print("Adding your bot to the room ...")
        api.memberships.create(TestRoom.id, personEmail=bot.botEmail)
        Botapi = CiscoSparkAPI(bot.botToken)
        print("Sending first message ...")
        Botapi.messages.create(TestRoom.id, text="Hi! I'm your new bot " + bot.name)
        CreateProject(bot.botToken,bot.name,bot.id,UserToken,TestRoom.id,bot.botEmail,isAPI)
        print("Bot successfully created: [name : '"+bot.name+"', email: '"+bot.botEmail+"', id: '"+bot.id+"', token: '"+bot.botToken+"']")
        print("")
        if (isAPI=="y"):
            print("To begin with " + BotName + ", run it with : python initBot.py launch " + BotName + " <BotPort>")
        else :
            print("To begin with " + BotName + ", run it with : python initBot.py run " + BotName + " <BotPort>")
        print("")
        return ("Your bot was successfully created, and a TestRoom was created with your bot!")
    #except:
        #return "Sorry, we were unable to complete this task"

def CreateProject(token,name,id,usertoken,roomId,email,isAPI):
    api = CiscoSparkAPI(token)
    if (isAPI=="y"):
        templateMain = env.get_template('mainAPI.py.j2')
        templateClass = env.get_template('tempClassAPI.py.j2')
        templateCompute = env.get_template('ComputeAPI.py.j2')
    else :
        templateMain = env.get_template('main.py.j2')
        templateCompute = env.get_template('Compute.py.j2')
        templateClass= env.get_template('tempClass.py.j2')
    templateRequestClass = env.get_template('RequestClass.py.j2')
    outputMain = templateMain.render(token=token,name=name)
    outputClass = templateClass.render(name=name)
    outputRequest = templateRequestClass.render(name=name)
    outputCompute = templateCompute.render(email=email)
    webhook = api.webhooks.create(name="Webhook for project "+name,targetUrl="http://www.cisco.com",resource="messages",event="created")
    webhookRooms = api.webhooks.create(name="Webhook rooms for project " + name, targetUrl="http://www.cisco.com",resource="rooms", event="created")
    ProjectInfo={"name":name,"token":token,"Webhookname":webhook.name,"Webhookid":webhook.id,"Webhookroomsname":webhookRooms.name,"webhookroomsid":webhookRooms.id,"Id":id,"userToken":usertoken,"Port":None,"PythonProcess":None,"NGrokProcess":None,"roomId":roomId}
    print("Adding data to local storage ...")
    with open('.config.txt') as json_file:
        data = json.load(json_file)
        bots = data['bots']
        bots.append(ProjectInfo)
        newdata={"bots":bots}
        with open('.tmp.txt', 'w') as outfile:
            json.dump(newdata, outfile)
    os.remove('.config.txt');
    os.rename('.tmp.txt','.config.txt')
    print("Creating your project files ...")
    try:
        os.makedirs(name)
        os.makedirs(name+'/utils')
        with open(name+'/main.py', 'w') as main:
            main.write(outputMain)
        with open(name+'/'+name+'.py', 'w') as clas:
            clas.write(outputClass)
        with open(name+'/utils/RequestClass.py',"w") as request:
            request.write(outputRequest)
        with open(name+'/utils/Compute.py',"w") as compute:
            compute.write(outputCompute)
        with open(name + '/utils/__init__.py', 'w') as init:
            init.write("")
        if (isAPI=="y"):
            shutil.copy('utils/DefaultAgent.zip', name)

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def StartProject(name,port,webhook):
    try:
        with open('.config.txt') as json_file:
            data = json.load(json_file)
            bots = data['bots']
            for bot in bots:
                if (bot["name"]==name):
                    token = bot['token']
                    webhookname = bot['Webhookname']
                    webhookid = bot['Webhookid']
                    roomname =bot['Webhookroomsname']
                    roomid = bot['webhookroomsid']
    except:
        print("Bot not found")
    #traceback.print_exc()
    try:
        storePort(name, port)
        thread_1 = threadNgrok(port, name,webhook)
        thread_1.start()
        time.sleep(2)
        set_pid()
        url = GetTunnelURL(port)
        if (webhook):
            UpdateWebhook(url, token, webhookname, webhookid,roomname,roomid)
        # launch = Popen(["python", name+"/main.py "+port])
        try:
            launch = Popen("python " + name + "/main.py ", shell=True)
        except:
            print("The bot isn't running")

        # StorePIDs(ngrok_pid,launch.pid,name,port)
        storePID(launch.pid, name)
        print(name + " is running")
        return ("NGrok is running")
    except:
        try:
            ngrok = NgrokAPI()
            ngrok.tunnel.delete(name="Webhook for bot on port " + port)
        except:
            pass
        print("An error occured ! The port "+port+" may already be in use !")
    #traceback.print_exc()


def GetTunnelURL(port):
    url = "http://127.0.0.1:4040/api/tunnels"
    response = requests.get( url)
    response = json.loads(response.text)
    search = "localhost:"+str(port)
    for tunnel in response['tunnels']:
        if tunnel['config']['addr']==search and tunnel['proto']=='https':
            return (tunnel['public_url'])

def UpdateWebhook(url,botToken,webhookName,webhookId,webroom,webid):
    api = CiscoSparkAPI(botToken)
    api.webhooks.update(webid, name=webroom, targetUrl=url+'/added')
    return api.webhooks.update(webhookId, name=webhookName, targetUrl=url)

def Info(name):
    try :
        with open('.config.txt') as json_file:
            found =False
            data = json.load(json_file)
            bots = data['bots']
            for bot in bots:
                if (bot["name"] == name):
                    found=True
                    token = bot['token']
                    webhookname = bot['Webhookname']
                    webhookid = bot['Webhookid']
                    pypro = bot['PythonProcess']
                    ngpro = bot['NGrokProcess']
                    port = bot['Port']
        if found:
            print("")
            print('Project name : ' + name)
            print('Bot token : ' + token)
            print('Webhook id : ' + webhookid)
            print('Webhook name : ' + webhookname)
            print('Last python process : ' ,pypro)
            print('Last NGrok process : ' ,ngpro)
            print('Last port used : ' ,port)
            print("")
        else :
            print("Sorry, I wasn't able to find this bot !")

    except:
        print("")
        print("Sorry, I wasn't able to find the others informations")
        print("")


def get_pid(port):
    p = Popen(['ps', '-A'], stdout=PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if ("ngrok http "+port) in line:
            pid = int(line.split(None, 1)[0])
            return pid


def storePID(pid,name):
    with open('.config.txt') as json_file:
        data = json.load(json_file)
        bots = data['bots']
        for bot in bots:
            if (bot['name']==name):
                bot['PythonProcess'] = pid
        newdata = {"bots": bots}
        with open('.tmp.txt', 'w') as outfile:
            json.dump(newdata, outfile)
    os.remove('.config.txt');
    os.rename('.tmp.txt', '.config.txt')

def storePort(name,port):
    with open('.config.txt') as json_file:
        data = json.load(json_file)
        bots = data['bots']
        for bot in bots:
            if (bot['name']==name):
                bot['Port']=port
        newdata = {"bots": bots}
        with open('.tmp.txt', 'w') as outfile:
            json.dump(newdata, outfile)
    os.remove('.config.txt');
    os.rename('.tmp.txt', '.config.txt')

def Stop(name):
    try:
        with open('.config.txt') as json_file:
            data = json.load(json_file)
            bots = data['bots']
            for bot in bots:
                if (bot['name'] == name):
                    python_pid = bot['PythonProcess']
                    port = bot['Port']
        ngrok = NgrokAPI()
        #os.killpg(os.getpgid(int(python_pid)), signal.SIGKILL)
        #os.kill(int(python_pid), signal.SIGKILL)
        requests.post('http://localhost:'+port+'/shutdown')
        time.sleep(2)
        #Status()
        ngrok.tunnel.delete(name="Webhook for bot on port " + port)
    except:
        print("")
        print("Stop failed because bot may not be running")
        print("")
        #traceback.print_exc()




def Delete(name):
    try:
        with open('.config.txt') as json_file:
            data = json.load(json_file)
            bots = data['bots']
            newBot=[]
            for bot in bots:
                if (bot['name']==name):
                    token=bot['token']
                    id= bot['Id']
                    userToken=bot['userToken']
                    roomId=bot['roomId']
                else:
                    newBot.append(bot)
            newDoc = {"bots":[]}
            with open('.tmp.txt', 'w') as outfile:
                json.dump(newDoc, outfile)
            os.remove('.config.txt');
            os.rename('.tmp.txt', '.config.txt')
        apiBot=CiscoSparkAPI(token)
        apiBot.rooms.delete(roomId)
        apiUser =CiscoSparkAPI(userToken)
        user = ApplicationAPI(apiUser._session)
        print(id)
        user.delete(id=id)
    except:
        print("Error")
    #traceback.print_exc()

def set_pid():
    p = Popen(['ps', '-A'], stdout=PIPE)
    out, err = p.communicate()
    running = False
    for line in out.splitlines():
        if ("ngrok start --none") in line:
            proid = int(line.split(None, 1)[0])
    with open('.config.txt') as json_file:
        data = json.load(json_file)
        bots = data['bots']
        try:
            for bot in bots:
                bot['NGrokProcess'] = proid
        except:
            pass

        newdata = {"bots": bots}
        with open('.tmp.txt', 'w') as outfile:
            json.dump(newdata, outfile)
    os.remove('.config.txt');
    os.rename('.tmp.txt', '.config.txt')

def List():
    print("Bots existing :")
    with open('.config.txt') as json_file:
        data = json.load(json_file)
        bots = data['bots']
        for bot in bots:
            print(bot['name'])
    return ("list")


def Status():
    with open('.config.txt') as json_file:
        data = json.load(json_file)
        bots = data['bots']
        print("")
        print("####   NGrok   ####")
        print("")
        try:
            ngrokid = bots[0]["NGrokProcess"]
            proc = psutil.Process(ngrokid)
            print("NGrok is working")
        except:

            print("NGrok isn't working")
            print("")
            print("###################")
        print("")
        print("######   Bots   ######")

        API = NgrokAPI()
        if (len(bots) == 0):
            print("")
            print("No bots found")

        for bot in bots:

            try:
                proc = psutil.Process(bot['PythonProcess'])
                print("")
                print(bot['name'] + " is working")
                try:
                    tunnel = API.tunnel.get(name=("Webhook for bot on port " + str(bot['Port'])))

                    print("Tunnel for bot "+bot['name']+ " is working")
                    print("url : "+ tunnel.public_url)
                    print("name : "+tunnel.name)
                except:
                    print("Tunnel for bot " + bot['name'] + " isn't working")
            except:
                print("")
                print(bot['name']+" isn't working")
    print("")
    print("######################")
    print("")
    #traceback.print_exc()


def InstallRequirements():
    import pip
    required = ['docopt', 'ciscosparkapi', 'jinja2', 'requests', 'flask', 'psutil']
    for require in required:
        pip.main(['install', require])
    pip.main(['install', 'git+https://cto-github.cisco.com/gladhuie/ngork.git'])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1')
    if (arguments['run']):
        StartProject(arguments['<name>'],arguments['<port>'],True)
    elif (arguments['launch']):
        StartProject(arguments['<name>'], arguments['<port>'], False)
    elif (arguments['create']):
        InitBot()
    elif(arguments['delete']):
        Delete(arguments['<name>'])
    elif (arguments['reload']):
        print("rel")
    elif(arguments['stop']):
        Stop(arguments['<name>'])
    elif(arguments['info']):
        Info(arguments['<name>'])
    elif (arguments['list']):
        List()
    elif (arguments['install']):
        InstallRequirements()
    elif (arguments['status']):
        Status()


