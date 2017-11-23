import pickle
from pathlib import Path
import time 
import threading 
import logging

# custom
from MessageCenter import MessageCenter
from Machine import Machine
from Coder import * 
from DataGetter import DataGetter
from SystemDeliveryObjects import SystemCall

# initial logger
logger = logging.getLogger('MonitorApplication')

class SendingStatus(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, _messageCenter, _encoder, _clock, _request ):
        super(SendingStatus, self).__init__()
        self.__stop = False 
        self.__messageCenter = _messageCenter 
        self.__encoder = _encoder
        self.__clock = _clock 
        self.__dg = DataGetter()
        self.__request = _request
    # end of the declaration of contructor

    def run(self):

        data = self.__dg.getData( 1 ) 
        msgType = "status_h" 
        msg = self.__encoder.encodeMsg_out( msgType , data, "master" ) 
        logger.debug( msg.toString() )
        self.__messageCenter.sendNewMessage( msg ) 

        while True:

            if self.__stop == True:
                msg = self.__encoder.encodeMsg_out( "sys", "stop transmitting", "master" ) 
                self.__messageCenter.sendNewMessage( msg ) 
                break
            else:
                pass

            if self.__request == 1:
                # get Hardware data
                data = self.__dg.getData(1)
                msgType = "status_h"
            elif self.__request == 2:
                # get OS data
                data = self.__dg.getData(2)
                msgType = "status_os"
            elif self.__request == 3:
                # get None-zero cpu ussage processes
                data = self.__dg.getData(3)
                msgType = "status_p"
            elif self.__request == 4:
                # get OS data and Processes data
                data = [self.__dg.getData(2), self.__dg.getData(3)]
                msgType = "status_os/p"
            elif self.__request == 5:
                # get all data
                data = [ self.__dg.getData(1), self.__dg.getData(2), self.__dg.getData(3) ]
                msgType = "status_all"
            else: 
                data = self.__dg.getData(2)
                msgType = "status_os"

            
            msg = self.__encoder.encodeMsg_out( msgType, data, "master" ) 
            self.__messageCenter.sendNewMessage( msg ) 
            # print( msg.toString() )

            time.sleep( self.__clock) 
    # end of run()

    def setStop(self): 
        self.__stop = True 
    # end of setStop()

    def updateClock(self, _clock ):
        self.__clock = float( _clock ) 
    # end of updateClock()

    def updateRequest(self, _request ):
        self.__request = _request 
    # end of updateRequest()

# end of class StatusSending


class Slave(threading.Thread):

    def __init__(self):
        super(Slave, self).__init__()
        logger.debug( "Initializing ...\n" ) 

        # Initialize local machine
        logger.debug( "\nLocal machine check..." )
        my_file = "./LocalMachineFile.plk"
        self.__localMachine = self.__machineInitial( my_file, "local" )
        logger.debug( "Local machine is confirmed." )

        # Initializa master machine 
        logger.debug( "\nMaster machine check..." )
        my_file = "./MasterMachineFile.plk"
        self.__masterMachine = self.__machineInitial( my_file, "master" )
        logger.debug( "Master machine is confirmed." )

        reference_coder = {}
        reference_coder[self.__masterMachine.getName()] = self.__masterMachine
        reference_coder[self.__localMachine.getName()] = self.__localMachine

        # initialize encoder
        logger.debug( "\nEncoder check..." )
        self.__ec = Encoder( self.__localMachine, reference_coder ) 
        logger.debug( "Encoder is confirmed." )

        # initialize decoder 
        logger.debug( "\nDecoder check..." )
        self.__dc = Decoder( self.__localMachine, reference_coder )
        logger.debug( "Decoder is confirmed." )

        # initialize Message Center 
        logger.debug( "\nMessage center check ..." )
        reference_mc = {}
        reference_mc[self.__masterMachine.getIP()] = self.__masterMachine.getName()
        reference_mc[self.__localMachine.getIP()] = self.__localMachine.getName()
        self.__msgCenter = MessageCenter( self.__localMachine, reference_mc ) 
        self.__msgCenter.start()
        logger.debug( "Message center is confirmed." )

        self.__st = None 
    # end of the declaration of constructor

    
    def __dumpMachine( self, _machine, _dir ):
        with open( str(_dir), 'wb') as handle:
            pickle.dump( _machine, handle, protocol=pickle.HIGHEST_PROTOCOL )
    # end of dumpMachine()

    def __loadMachine( self, _dir ):
        with open( str(_dir), 'rb') as handle:
            machine = pickle.load(handle)
        return machine
    # end of loadMachine()

    def __settingUpMachine( self, _dir ):
        while True:
            print( "\nSetting up..." )
            name = input( "Enter the machine name: " ) 
            ip = input( "Enter the machine IP address: " )
            port = input( "Enter the connection port: " )

            print( "\nName:" +name+", IP:"+ip+", Port:"+port + "\n" )
            cmd = input( "Confirm ? y/n  " )
            if cmd == "y":
                break

        machine = Machine( name, ip, port )
        self.__dumpMachine( machine, _dir )
        return machine
    # end of settingUpMachine()

    def __machineInitial( self, _path, _type ):
        my_file = Path( _path )
        if my_file.is_file():
            machine = self.__loadMachine( _path ) 
            if _type == "local":
                print( "\nLocal machine details: " )
            else:
                print( "\nMaster machine details: " )

            print( machine.toString() + "\n" )
            cmd = input( "Confirm ?  y/n  ") 
            if cmd == "y":
                pass
            else:
                machine = self.__settingUpMachine( _path ) 
        else:
            machine = self.__settingUpMachine( _path )

        return machine
    # end of __machineInitial()

    def __msgProcess(self):
        while not self.__msgCenter.isQueueEmpty():
            msg = self.__msgCenter.getNewMessage()
            type, obj = self.__dc.decodeMessage( msg )
            if type == "sys":
                rtn = self.__sysCMDProcess( obj )
                if rtn == "cmd accepted, terminating.":
                    return rtn 
            else:
                pass
    # end of msgProcess() 

    def __sysCMDProcess(self, _obj ):
        if isinstance( _obj, SystemCall ):
            content = _obj.getContent()

            if isinstance( content, str ):
                content = content 
            else:
                content_2 = content[1] 
                content = content[0]


            if content == "start transmit":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass 

                return "cmd accepted, start transmitting."
            elif content == "stop transmit":
                if self.__st != None:
                    self.__st.setStop()
                else:
                    pass

                return "cmd accepted, stop transmitting."
            elif content == "terminate":
                if self.__st != None:
                    while self.__st.is_alive():
                        self.__st.setStop()
                else:
                    pass

                return "cmd accepted, terminating."
            elif content == "request type1":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass

                self.__st.updateRequest( 1 )
                return "cmd accepted, switch to type 1"

            elif content == "request type2":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass

                self.__st.updateRequest( 2 )
                return "cmd accepted, switch to type 2"
            elif content == "request type3":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass

                self.__st.updateRequest( 3 )
                return "cmd accepted, switch to type 3"
            elif content == "request type4":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass

                self.__st.updateRequest( 4 )
                return "cmd accepted, switch to type 4"
            elif content == "request type5":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass

                self.__st.updateRequest( 5 )
                return "cmd accepted, switch to type 5"
            elif content == "clock change":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass
                self.__st.updateClock( content_2 ) 
			elif content == "kill process by pid":
                if self.__st == None or not self.__st.is_alive():
                    self.__startTransmit()
                else:
                    pass
                
                try :
                    psutil.Process(int(input("please enter the pid you want to kill:"))).kill()
                    return "process killed"
                except psutil.NoSuchProcess:
                    return "process not found"
        else:
            pass
    # end of __sysCMDProcess()

    def __startTransmit(self):
        clock = 2
        defaultRequest = 4
        self.__st = SendingStatus( self.__msgCenter, self.__ec, clock, defaultRequest ) 
        self.__st.start()


    def run(self):
        while True:
            if self.__msgCenter.isQueueEmpty():
                rtn = "continue"
                # print( "There is no message in this cycle." )
            else:
                rtn = self.__msgProcess()
        
            if rtn == "cmd accepted, terminating.":
                break
            else:
                time.sleep(5)
    #  end of run()

    def getMsgCenter(self):
        return self.__msgCenter
    # end of  getMsgCenter()

    def getEncoder(self):
        return self.__ec 
    # end of getEncoder()

    def getLocalMachine(self):
        return self.__localMachine
    # end of getLocalMachine()

    def getMasterMachine(self):
        return self.__masterMachine
    # end of getMasterMacine()

