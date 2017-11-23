from datetime import datetime

class Message(object):
    """description of class"""

    def __init__(self, _desitnation, _port, _type, _content, _sender ):
        self.__destination = _desitnation
        self.__port = _port
        self.__type = _type
        self.__content = _content
        self.__sender = _sender 
        self.__createdTime = str( datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
    # end of declaration of contructor 

    def getDestination(self):
        return self.__destination
    # end of getDestination()

    def getPort(self):
        return self.__port
    # end of getPort()

    def getType(self):
        return self.__type
    # end of getType()

    def getContent(self):
        return self.__content
    # end of getContent()

    def getSender(self):
        return self.__sender 
    # end of getSender() 

    def setSenderName(self, _newName):
        self.__sender = _newName 
    # end of setSenderName()

    def getCreatedTime(self):
        return self.__createdTime 
    # end of CreatedTime()

    def toString(self):
        return "Message Object, " + "Destination: " + self.__destination + " Port: " + self.__port + " Type: " + self.__type + " Content: " +str( self.__content ) + " Sender: " + self.__sender
    # end of toString()