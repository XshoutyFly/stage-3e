from utils.Compute import Compute
import logging
from logging.handlers import RotatingFileHandler
import mysql.connector as mc

logger = logging.getLogger()
######################################################################################
#You can modify run() method of MyBot class to implement your algorithm on this bot !#
######################################################################################
class XshoutyFly(Compute):
    def spark(self):
        #Your code here
        request = self.req
        roomId = request['originalRequest']['data']['data']['roomId']
        action = request['result']['action']
        
        

       
        if (action=='UsersList'):
            try:
                connection = mc.connect (host = "localhost",
                                        user = "root",
                                        passwd = "root",
                                        db = "thomas")
            except mc.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))

            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users") 
            print('''Result of "SELECT * FROM users":''')
            result = cursor.fetchall() 
            i=0
            answer = "Voici la liste des utilisateurs: \r\n"
                    
            for r in result:
                i+=1
                answer += "{}. Prenom : {}, Nom : {}, Age : {} ans, Genre : {}, Nourriture : {}, Pays : {}\r\n".format(i,r[1],r[2],r[3],r[4],r[5],r[6])
            
            self.answer(roomId, markdown=answer)
            cursor.close()
            connection.close()
            return ""
        elif(action == "Goodbye"):
            return "See you!"
        elif (action=="List"):
            answer = "1. Say hello when you say 'Hi' \r\n2. Say goodbye when you say 'Goodbye' \r\n3. And show you an image when you say 'Image'"
            self.answer(roomId, text='Here is a list of what I can do : ')
            self.answer(roomId, markdown=answer)
            return ""
        elif (action =="Image"):
            self.answer(roomId, markdown="Here is an Image",files=["https://www.cisco.com/web/fw/i/logo-open-graph.gif"])
            return ""
        else:
            return "I didn't understood, sorry!"

    def Webhook(self):
        #Your code Here
        logger.info(self.request)