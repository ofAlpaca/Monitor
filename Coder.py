from Machine import Machine


class Coder(object):
    """description of class"""

    def __init__(self, _localHost, _machineTable ):
        self.msgLastMessage = None

        self.dictionary = _machineTable
        self.localHost = _localHost
    # end of the declaration of constructor
         
    def updateLastMsg(self, _referenceMsg ):
        self.msgLastMessage = _referenceMsg 
    # end of updateLastMessage()

    def getLastMsg(self):
        return self.msgLastMessage 
    # end of updateLastMessage()

    

from Message import Message

class Encoder(Coder):
    """description of class"""

    def __init__(self, _localHost, _reference ):    
        Coder.__init__( self, _localHost, _reference )

    # end of the declaration of contructor

    def encodeMsg_out( self, _msgtype, _msgContent, _msgTarget ):
        # create Message Object from the host 

        # _msgTarget should be a string 
        target = self.dictionary[_msgTarget]; # for master

        newMsg = Message( target.getIP(), target.getPort(), _msgtype, _msgContent, self.localHost.getIP() )

        self.updateLastMsg( newMsg )
        return newMsg
    # end of encodeMsg_out()

    def encodeMsg_in( self, _msgtype, _msgContent, _msgSender ):
        # this method should be called only by the messageCenter
        # create Message Object from received data

        target = self.dictionary[_msgSender]; # for master

        newMsg = Message( self.localHost.getIP(), self.localHost.getPort(), _msgtype, _msgContent, target ) 

        self.updateLastMsg( newMsg )
        return newMsg
    # end of encodeMsg_in()


from SystemDeliveryObjects import *

class Decoder(Coder):

    def __init__(self, _localhost, _machineTable ):
        Coder.__init__( self, _localhost, _machineTable ) 
    # end of the declaration of constructor

    def decodeMessage( self, _newMsg:Message ):
        # to decode the message
        # make Message Object be translated to SystemDeliveryObjects

        type = _newMsg.getType()
        content = _newMsg.getContent()
        sender = _newMsg.getSender()

        if type == "sys":
            rtn = SystemCall( sender, content ) 
        elif type == "status_h":
            rtn = Status_Hardware( sender, content.pop(), content.pop() )
        elif type == "status_os":
            rtn = Status_Software( sender, content.pop(), content.pop() )
        elif type == "status_os/p":
            # content = [ data_os, data_p ]
            data_p = content.pop()
            data_os = content.pop()
            rtn = [ Status_Software( sender, data_os.pop(), data_os ), Status_Processes( sender, data_p.pop(), data_p ) ]
        elif type == "status_all":
            # content = [ data_h, data2_os, data3_p ]
            data_p = content.pop()
            data_os = content.pop()
            data_h = content.pop()
            rtn = [ Status_Hardware( sender, data_h.pop(), data_h), Status_Software( sender, data_os.pop(), data_os), Status_Processes( sender, data_p.pop(), data_p ) ]
        elif type == "status_p":
            rtn = Status_Processes( sender, content.pop(), content )
        else:
            type = "trash"
            rtn = None 
        return type, rtn 

    # end of decodeMessage()

# for testing objects
# main starts here


