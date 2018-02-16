import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()

class Request:
    def __init__(self, json,api):
        self.api =api
        self.json = json
        self.messId = json['data']['id']
        self.roomId = json['data']['roomId']
        self.personId = json['data']['personId']
        self.personEmail = json['data']['personEmail']
        self.data = json['data']['created']
        self.me = self.api.people.me()
        self.MyEmail = self.me.emails[0]


    def Answer(self,**data):
        """
        Answer() function send the response to the room
        """
        try:
            self.api.messages.create(self.roomId, **data)
            self.success = True
        except:
            self.success=False
        return self.success

    def getDetails(self):
        """
        getDetails() function get the content of the message
        """
        details = self.api.messages.get(messageId=self.messId)
        message = details.text
        message = message.replace( "XshoutyFly","")
        if (message[0]==" "):
            message=message[1:len(details.text)]
        if (message[-1]==" "):
            message=message[0:len(details.text)-1]
        details.plainText=message
        return (details,message)

    def PrintFeedback(self,message,answer,success,understood):
        """
        PrintFeedback() function print the feedback of the action in Python console
        """

        logger.info("Request by : "+ self.personEmail)
        logger.info("Content of the request : "+message)
        if (understood):
            logger.info("Request understood by the Bot")
        else:
            logger.info("Request not understood by the bot")
        logger.info("Answer sent : "+answer)
        if (success):
            logger.info("Answer successfully sent to the room")
        else:
            logger.info("Answer not successfully sent to the room")