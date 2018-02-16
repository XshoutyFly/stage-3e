# CiscoSparkPython

## What can I do with this framework ?
You can easily create CiscoSpark bot via CLI, and quickly start bots projects.

This will create for you project files and defaults commands with examples of classic functionnalities. You will also be able to easily run your projects.

## Available functionnalities:
1. Create bot
2. Run it with few defaults commands
3. Stop it
4. Delete it
5. Get informations about all your bots
6. Get status of CiscoSparkPython

## How does it work ?

### Install the framework
1. Create a folder that will contain all the CSP files and all the source files of your bots
2. Clone this repository in the folder without creating a special folder `git clone https://cto-github.cisco.com/adt-emear/CiscoSparkPython .`
3. This library cannot (for the moment) be globally installed on your computer/server. All the commands available with this library will be callable only in the directory and beginning with `python initBot.py <command>`.
4. Run `python initBot.py install`to install all requirements


### Create and manage bots
```bash
Usage:
  initBot.py create
  initBot.py delete <name>
  initBot.py run <name> <port>
  initBot.py reload <name>
  initBot.py stop <name>
  initBot.py <name> info
  initBot.py list
  initBot.py status


Options:
  -h --help     Show this screen.
  -V --version  Show version
```


1. Create your bot with `python initBot.py create`
2. Enter all the required informations (user token - you can fin it on `https://developer.ciscospark.com/` -, name, email, logo and if you want to integrate it with DialogFlow/API.AI - web platform that parse natural language into json file, really good to create natural language speaking bots, see here : `https://dialogflow.com/` -)
3. Run it with `python initBot.py run <MyBotName> <MyBotPort>`
4. Play with your bot in `<MyBotName>/Compute.py`, you are already in development mode
5. Stop your bot with `python initBot.py stop <MyBotName>`
6. If you want, you can delete it with `python initBot.py delete <MyBotName>`. This won't delete your source files

