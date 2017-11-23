from pathlib import Path
from Machine import Machine
from Message import Message
import logging 
import sqlite3
import pickle

from SystemDeliveryObjects import *

class Database(object):
    """description of class"""

    def __init__(self):
        self.__machineCount = 0 
        self.__machineList = []  # List
        self.__machineNameList = [] # List
        self.__machineTable_name = {} # hashTable 
        self.__machineTable_ip = {}
        self.__SQLDatabaseSetting()

    def initializeDatabase(self, __debug ):
        self.__setMachineList(__debug) 
        self.__machineCount = len( self.__machineList ) 
    # end of initializeDatabase()

    def __SQLDatabaseSetting(self):
        sql_file = Path('sqlDB.db')

        if sql_file.is_file():
            self.__sqlDB = sqlite3.connect( 'sqlDB.db' )
        else:
            self.__sqlDB = sqlite3.connect( 'sqlDB.db' )

            # create machine_list Table ( name, ip, content )
            self.__sqlDB.execute( 'CREATE TABLE machine_list ( name TEXT PRIMARY KEY NOT NULL, ip TEXT NOT NULL, content BLOB NOT NULL )' )
            # create message_record Table ( time, sender, receiver, content ) 
            self.__sqlDB.execute( 'CREATE TABLE message_record ( time TEXT PRIMARY KEY NOT NULL, sender TEXT NOT NULL, receiver TEXT NOT NULL, content TEXT NOT NULL )' )
            # create  status_record Table ( time, owner, type, content )
            self.__sqlDB.execute( 'CREATE TABLE status_record ( time TEXT PRIMARY KEY NOT NULL, owner text NOT NULL, type TEXT NOT NULL, content TEXT NOT NULL )' )
            # create os_history Table ( time, owner, cpu_usr, cpu_sys, cpu_idle, mem_per )
            self.__sqlDB.execute( 'CREATE TABLE os_history ( time TEXT PRIMARY KEY NOT NULL, owner text NOT NULL, cpu_usr TEXT NOT NULL, cpu_sys TEXT NOT NULL, cpu_idle TEXT NOT NULL, mem_per TEXT NOT NULL )' )


        self.__sqlDB.commit() 
    # end of SQLDatabaseSetting()

    # the function of the user interface should be implemented in this method
    def __setMachineList(self, __debug):
        # Command Line Interface 

        if __debug in ['True', 'true']:
            while True:
                print( "\n\nSetting up slave machines.")
                print( "----------Menu------------")
                print( "d) Use default setting." )
                print( "a) Add a new machine")
                print( "v) View current Machine List" )
                print( "r) Remove Machine" )
                print( "q) Finish" )
            
                cmd = input( "What's your command ?  " )
            
                if cmd == 'd':
                    print( "\nThis is the default setting.")
                    print( "Name:localhost, IP:127.0.0.1, Port:9487")
                    print( "Name:slave1, IP:192.168.249.141, Port:9487")
                    print( "Name:slave2, IP:192.168.249.142, Port:9487")
                    print( "Name:slave3, IP:192.168.249.143, Port:9487")
                
                    cmd = input( "Confirm? y/n  " )
                    if cmd == "y":
                        self.addMachine( Machine( "slave1", "192.168.249.141", "9487" ) )
                        self.addMachine( Machine( "slave2", "192.168.249.142", "9487" ) )
                        self.addMachine( Machine( "slave3", "192.168.249.143", "9487" ) )
                    else:
                        print( "Back to menu")

                elif cmd == 'a':
                    while True:
                        print( "\nAdd a machine" )
                        name = input( "Enter the name of the machine:  " )

                        while name == "q":
                            print( "This is an illegal name. Try another." )
                            name = input( "Enter the name of the machine:  " )

                        ip = input( "Enter the ip address of the machine:  " )
                        port = input( "Enter the port of the machine:  " )

                        print( "\nName:" +name+", IP:"+ip+", Port:"+port )
                        cmd = input( "Confirm? y/n  " )
                        if cmd == "y":
                            print( "Input Accepted" )
                            self.addMachine( Machine( name, ip, port ) )
                            break
                        else:
                            cmd = input( "Re-entering or quit? r/q  " )
                            if cmd == "r":
                                pass
                            else:
                                break
                elif cmd == 'v':
                    machines = self.__sqlDB.execute( 'SELECT name, ip FROM machine_list' )
                    for machine in machines:
                        print( machine ) 
                elif cmd == 'r':
                    while True:

                        machines = self.__sqlDB.execute( 'SELECT name, ip FROM machine_list' )
                        for machine in machines:
                            print( machine ) 
                        # end of for-loop

                        name = input( 'Enter the machine name to remove it or input q to quit  ')
                        if name == 'q':
                            break
                        else:
                            pass

                        try:
                            self.__sqlDB.execute( 'DELETE from machine_list where name = ?', ( name,) )
                            self.__sqlDB.commit()
                        except sqlite3.Error as e:
                            print( e.args[0] )
                    # end of while-loop

                elif cmd == 'q':
                    break
                else:
                    print( "\nIllegal command:" + cmd )
        else:
            pass

        # reload
        rows = self.__sqlDB.execute( 'SELECT name, ip, content FROM machine_list' )
        for row in rows:
            machine = self.__sqlContentToObject( row[2] ) 
            self.__machineTable_name[ row[0] ] = machine
            self.__machineTable_ip[ row[1] ] = row[0] 
            self.__machineList.append( machine ) 
            self.__machineNameList.append( machine.getName() )

    # end of __setMachineList__()

    def addMachine(self, _newMachine):
        # add a machine to the database

        if isinstance( _newMachine, Machine):
            try:
                self.__sqlDB.execute( 'INSERT INTO machine_list (name, ip, content) VALUES (?,?,?)', ( _newMachine.getName(), _newMachine.getIP(), pickle.dumps( _newMachine ), ) ) 
                self.__sqlDB.commit() 
            except sqlite3.Error as e:
                print( 'SQL Error' )
                print( e.args[0] )
        else:
            print( "Argument Error! Argument:_newMachine  ")
    # end of addMachine()

    def getMachineList(self):
        return self.__machineList
    # end of getMachineList()

    def getMachineTable_name(self):
        return self.__machineTable_name
    # end of getMachineTable_name()

    def getMachineTable_ip(self):
        return self.__machineTable_ip
    # end of getMachineTable_ip()

    def getMachineNameList(self):
        return self.__machineNameList 

    def viewMachineList(self):
        # to print all of machines in the database
        machines = self.__sqlDB.execute( 'SELECT name, ip FROM machine_list' )
        for machine in machines:
            print( machine ) 
    # end of viewMachineList()

    def updateMessageRecord(self, _newMessage):
        # message_record Table ( time, sender, receiver, content ) 
        try:
            self.__sqlDB.execute( 'INSERT INTO message_record (time, sender, receiver, content) VALUES ( ?, ?, ?, ? )', ( _newMessage.getCreatedTime(), _newMessage.getSender(), _newMessage.getDestination(), pickle.dumps( _newMessage ) ) ) 
            self.__sqlDB.commit()
        except sqlite3.Error as e:
            print( e.args[0] )
    # end of updateMessageRecord()

    def updateStatusRecord(self, _newStatus):
        # status_record Table ( time, owner, type, content )
        try:
            self.__sqlDB.execute( 'INSERT INTO status_record VALUES ( ?, ?, ?, ? )', ( _newStatus.getChron(), _newStatus.getOwnerName(), _newStatus.getType(), pickle.dumps( _newStatus ) ) ) 
            self.__sqlDB.commit()
        except sqlite3.Error as e:
            print( e.args[0] )
    # end of updateMessageRecord()

    def updateOSHistory(self, _name, _field, _data):
        # create os_history Table ( time, owner, cpu_usr, cpu_sys, cpu_idle, mem_per )
        try:
            if _field == 'cpu':
                self.__sqlDB.execute( 'UPDATE os_history SET cpu_usr=?, cpu_sys=?, cpu_idle=? WHERE owner=?', ( _data[0], _data[1], _data[2], _name, ) )
            else:
                self.__sqlDB.execute( 'UPDATE os_history SET mem_per=? WHERE owner=?', ( _data, _name, ) )
            self.__sqlDB.commit()
        except sqlite3.Error as e:
            print( e.args[0] )
    # end of updateOSHistory()

    def insertOSHistory(self, _OSObj ):
        # create os_history Table ( time, owner, cpu_usr, cpu_sys, cpu_idle, mem_per )
        try:
            time = _OSObj.getChron() 
            owner = _OSObj.getOwnerName()
            cpu_usr = _OSObj.getCPU_usr()
            cpu_sys = _OSObj.getCPU_sys()
            cpu_idle = _OSObj.getCPU_idle()
            mem_per = _OSObj.getMem_percent()

            self.__sqlDB.execute( 'INSERT INTO os_history VALUES (?,?,?,?,?,?)', ( time, owner, cpu_usr, cpu_sys, cpu_idle, mem_per ) ) 
            self.__sqlDB.commit()
        except sqlite3.Error as e:
            print( e.args[0] )
    # end of updateOSHistory()

    def getOSHistoryData(self, _name=None ):
        # create os_history Table ( time, owner, cpu_usr, cpu_sys, cpu_idle, mem_per )
        rtn = {} 
        try:

            if _name == None:
                _name = self.__machineList[0].getName()
            else:
                pass

            result = self.__sqlDB.execute( 'SELECT time, owner, cpu_usr, cpu_sys, cpu_idle, mem_per FROM os_history WHERE owner=?', (_name,) ).fetchone()
            rtn['time'] = result[0]
            rtn['cpu_usr'] = result[2]
            rtn['cpu_sys'] = result[3]
            rtn['cpu_idle'] = result[4]
            rtn['mem_per'] = result[5]
        except sqlite3.Error as e:
            print( e.args[0] )

        return rtn 
    # getOSHistoryData()

    def __sqlContentToObject(self, _sqlContent):
        return pickle.loads( _sqlContent ) 
    # end of sqlContentToObject()

    def getType1Data(self, _number=1, _name=None):
        
        try:
            if _name == None:
                _name = self.__machineList[0].getName()
            else:
                pass

            result = self.__sqlDB.execute( '''SELECT owner, content, time FROM status_record WHERE owner = ? AND type = 'Hardware' ORDER BY time DESC LIMIT ?;''', ( _name, _number,) )
            rtn = []
            for row in result:
                dictionary_name = {}
                obj = self.__sqlContentToObject( row[1] )
                dictionary_name['time'] = obj.getChron()
                dictionary_name['phy_cpu'] = obj.getPhyCPU() 
                dictionary_name['log_cpu'] = obj.getLogCPU()
                dictionary_name['min_cpu_freq'] = obj.getMinCPUFreq()
                dictionary_name['max_cpu_freq'] = obj.getMaxCPUFreq()
                dictionary_name['mem_size'] = obj.getMemSize()
                dictionary_name['boot_time'] = obj.getBootTime()
                rtn.append( dictionary_name )

        except sqlite3.Error as e:
            print( e.args[0] )

        return rtn 
   # end of getType1Data()

    def getType2Data(self, _number=1, _name=None):
        
        rtn = {} # dictionary 
        try:

            if _name == None:
                _name = self.__machineList[0].getName()
            else:
                pass

            result = self.__sqlDB.execute( '''SELECT owner, content, time FROM status_record WHERE owner = ? AND type = 'Software' ORDER BY time DESC LIMIT ?;''', ( _name, _number,) )
            rtn = [] 
            for row in result:
                dictionary_name = {} 
                obj = self.__sqlContentToObject( row[1] )
                dictionary_name['time'] = obj.getChron()
                dictionary_name['cpu_usr'] = obj.getCPU_usr() 
                dictionary_name['cpu_sys'] = obj.getCPU_sys()
                dictionary_name['cpu_idle'] = obj.getCPU_idle()
                dictionary_name['mem_total'] = obj.getMem_total()
                dictionary_name['mem_avai'] = obj.getMem_avai()
                dictionary_name['mem_used'] = obj.getMem_used()
                dictionary_name['mem_percent'] = obj.getMem_percent()
                rtn.append( dictionary_name )
            return rtn 

        except sqlite3.Error as e:
            print( e.args[0] )

        return rtn 
    # end of getType2Data()

    def getType3Data(self, _number=1, _name=None):
        
        try:
            if _name == None:
                _name = self.__machineList[0].getName()
            else:
                pass

            result = self.__sqlDB.execute( '''SELECT owner, content, time FROM status_record WHERE owner = ? AND type = 'Process' ORDER BY time DESC LIMIT ?;''', ( _name, _number,) )
            rtn = []
            for row in result:
                obj = self.__sqlContentToObject( row[1] )
                rtn.append( obj.getProcessList() )
            return rtn 

        except sqlite3.Error as e:
            print( e.args[0] )

        return rtn 
    # end of getType3Data()

   
