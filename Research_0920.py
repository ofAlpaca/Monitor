import logging
import logging.config
import pickle
from pathlib import Path
import threading
import sys
import signal
from functools import partial
# custom
from Database import Database
from Coder import Encoder, Decoder 
from Message import Message
from MessageCenter import MessageCenter
from Machine import Machine
from Analyzer import Analyzer
from MyGUIHandler import MyGUIHandler

# initial logger
root = logging.getLogger('MonitorApplication')

def dbInitial(__debug):
    db = Database() 
    db.initializeDatabase(__debug) 
    return db
# end of initialDB()

def dumpLocalMachine( _machine, _dir ):
   with open( _dir, 'wb') as handle:
        pickle.dump( _machine, handle, protocol=pickle.HIGHEST_PROTOCOL )
# end of dumpLocalMachine()

def loadLocalMachine( _my_file ):
    with open(_my_file, 'rb') as handle:
        machine = pickle.load(handle)
    return machine
# end of loadLocalMachine()

def settingUpLocalMachine( _dir ):
    while True:
        root.debug( "Setting up..." )
        name = input( "Enter the machine name: " ) 
        ip = input( "Enter the machine IP address: " )
        port = input( "Enter the connection port: " )

        print( "\nName:" +name+", IP:"+ip+", Port:"+port + "\n" )
        cmd = input( "Confirm ? y/n  " )
        if cmd == "y":
             break

    localMachine = Machine( name, ip, port )
    dumpLocalMachine( localMachine, _dir )
    return localMachine
# end of settingUpLocalMachine()

def machineInitial( __debug ):
    my_path = "./machineFile.plk" 
    my_file = Path(my_path)

    if my_file.is_file():
        localmachine = loadLocalMachine( my_path ) 
        if __debug in ['True', 'true']:
            print( "\nLocal machine details: " )
            print( localmachine.toString() + "\n" )
            cmd = input( "Confirm ?  y/n  ") 
            if cmd == "y":
                pass
            else:
                localmachine = settingUpLocalMachine( my_path ) 
    else:
        localmachine = settingUpLocalMachine( my_path )

    return localmachine
# end of initialDB()


def initialStage():

    # logInitailize()
    root.setLevel(logging.DEBUG)
    fh = logging.FileHandler('master.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    root.addHandler(fh)
    
    # logging.config.fileConfig('logging.conf')
    
    # reading config for debug
    __debug = 'True'
    try:
        with open("debugsetting.cfg", 'r') as cfgfile:
            __debug = cfgfile.read().split(":")[1]
    except FileNotFoundError:
        with open("debugsetting.cfg", 'w+') as cfgfile:
            cfgfile.write('debug:True')
            __debug = 'True'

    if __debug in ['True', 'true']:
        std = logging.StreamHandler(sys.stdout)
        root.addHandler(std)
    
    
    root.debug( "Initializing ..." ) 

    # Initialize local machine
    root.debug( "Local machine check..." )
    localmachine = machineInitial( __debug )
    root.debug( "Local machine is confirmed.")

    # Initialize Database 
    root.debug( "Database check..." )
    db = dbInitial(__debug)
    root.debug( "Database is confirmed." )

    # initialize MessageCenter 
    root.debug( "Message center check..." )
    table = db.getMachineTable_ip()
    table[ localmachine.getIP() ] = localmachine.getName()
    msgCenter = MessageCenter( localmachine, table )
    msgCenter.start()
    root.debug( "Message Center is confirmed." )


    # Initialize Encoder
    root.debug( "Encoder check..." )
    ec = Encoder( localmachine, db.getMachineTable_name() ) 
    root.debug( "Encoder is confirmed." )

    # initialize Decoder
    root.debug( "Decoder check..." )
    dc = Decoder( localmachine, db.getMachineTable_name() )
    root.debug( "Dncoder is confirmed." )

    # Connection test
    root.debug( "Connection test" )
    slaveList = db.getMachineList()
    '''
    for slName in slaveList:
        newMsg = ec.encodeMsg_out( "Sys", ["test", "test"], slName.getName() ) 
        if isinstance( newMsg, Message ):
            msgCenter.sendNewMessage( newMsg ) 
        else :
            root.debug( slName + ", cannot find the corresponed IP.")
    '''
    root.debug( "Connections are confirmed.")

    ay = Analyzer( db )

    # initialize GUI
    myGUI = MyGUIHandler( ec, msgCenter, db )


    return localmachine, db, msgCenter, ec, dc, ay, myGUI 



def signal_handler(self, signum, frame):
    self.restart()
# end of signal_handler

if __name__ == "__main__":
    localmachine, db, msgCenter, ec, dc, ay, myGUI = initialStage()
    root.debug( "Initialization successed")
    #print( signal.SIGHUP )
    signal.signal(signal.SIGINT, partial( signal_handler, myGUI ) )
    p = False 
    while True:

        while not msgCenter.isQueueEmpty():
            p = not p 
            newMsg = msgCenter.getNewMessage()
            root.debug( newMsg.getSender() )
            type, obj = dc.decodeMessage( newMsg ) 
            
            if type == "status_os/p" or type == "status_all":
                for o in obj:
                    db.updateStatusRecord( o )
            elif type == "status_h" or type == "status_os" or type == "status_p":
                db.updateStatusRecord( obj )

            ay.analyzeData( obj )
            db.updateMessageRecord( newMsg )

        if p:
            print( "OS_History")
            print( db.getOSHistoryData() )
            print( "END\n\n" )

            
            print( "Type1")
            print( db.getType1Data())
            print( "END\n\n" )

            print( "Type2")
            print( db.getType2Data() )
            print( "END\n\n" )
            
            print( "Type3")
            print( db.getType3Data() )
            print( "END\n\n" )
            p = not p

    cmd = input( "Wait")
