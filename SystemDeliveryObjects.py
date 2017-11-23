class Status(object):
    """description of class"""
    def __init__(self, _name, _chron, _data, _type = '-1' ):
        self.__machineName = _name 
        self.__type = _type 
        chron = str(_chron).split( " " )
        
        try:
            self.__date = chron[0]
            self.__time = chron[1]
        except IndexError:
            pass

        self.fields = _data
    # end of the declaration of constructor

    def getOwnerName(self):
        return self.__machineName 
    # end of getName()

    def getTime(self):
        return self.__time 
    # end of getTime()

    def getDate(self):
        return self.__date
    # end of getDate()

    def getChron(self):
        return str( self.__date + " " + self.__time )
    # end of getChron()

    def getType(self):
        return self.__type 
    # end of getType()
# end of the discrption of class Status

class Status_Hardware(Status):

    def __init__(self, _name, _chron, _data ):
        Status.__init__( self, _name, _chron, _data, 'Hardware' )
    # end of the declaration of constructor

    # [self.physical_cpu, self.logical_cpu, self.cpu_min_freq, self.cpu_max_freq, self.mem_size, self.boot_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    def getPhyCPU(self):
        try:
            return self.fields[0]
        except IndexError:
            pass
    # end of getPhyCPU()

    def getLogCPU(self):
        try:
            return self.fields[1]
        except IndexError:
            pass 
    # end of getLogCPU()

    def getMinCPUFreq(self):
        try:
            return self.fields[2]
        except IndexError:
            pass 
    # end of getMinCPUFreq(self)

    def getMaxCPUFreq(self):
        try:
            return self.fields[3]
        except IndexError:
            pass 
    # end of getMaxCPUFreq()

    def getMemSize(self):
        try:
            return str( self.fields[4] )
        except IndexError:
            pass 
    # end of getMemSize()

    def getBootTime(self):
        try:
            return str( self.fields[5] )
        except IndexError:
            pass 
    # end of getBootTime()

    def toString(self):
        return "Time: " + self.getChron() + "\nCore Number: " + str(self.fields[0]) + "\nThread Number: " + str(self.fields[1]) + "\nMin Frequency: " + str(self.fields[2]) + "\nMax Frequency: " + str(self.fields[3]) + "\nMemory Size(MB): " + str( ( int(self.fields[4])/(1024*1024) ) )
    # end of toString()
# end of the discription of class Status_Hardware

class Status_Software(Status):

    def __init__(self, _name, _chron, _data ):
        Status.__init__( self, _name, _chron, _data, 'Software' )
    # end of the declaration of constructor

    #CPU usage: user, system, idle and Memory usage: total, available, used, percentage used in sequence
    def getCPU_usr(self):
        try:
            return self.fields[0]
        except IndexError:
            pass
    # end of getCPU_usr()

    def getCPU_sys(self):
        try:
            return self.fields[1]
        except IndexError:
            pass
    # end of getCPU_sys()

    def getCPU_idle(self):
        try:
            return self.fields[2]
        except IndexError:
            pass
    # end of getCPU_idle()

    def getMem_total(self):
        try:
            return self.fields[3]
        except IndexError:
            pass
    # end of getMem_total()

    def getMem_avai(self):
        try:
            return self.fields[4]
        except IndexError:
            pass
    # end of getMem_ava(self):

    def getMem_used(self):
        try:
            return self.fields[5]
        except IndexError:
            pass
    # end of getMem_used()

    def getMem_percent(self):
        try:
            return self.fields[6]
        except IndexError:
            pass
    # end of getMem_percent()

    def toString(self):
        return "Time: " + self.getChron() + "\nCore User Percentage: " + str(self.fields[0]) + "\nCPU System Percentage: " + str(self.fields[1]) + "\CPU Idle Percentage: " + str(self.fields[2]) + "RAM Total: " + str( ( int(self.fields[3])/(1024*1024) ) ) + "\nRAM Available(MB): " + str( ( int(self.fields[4])/(1024*1024) ) ) + "\nRAM Used(MB):" + str( ( int(self.fields[5])/(1024*1024) ) )  + "\nRAM Used Percentage: " + str( self.fields[6] )
    # end of toString()
# end of the discription of class Status_Hardware

class Status_Processes(Status):

    def __init__(self, _name, _chron, _data ):
        
        Status.__init__( self, _name, _chron, _data, 'Process' )

        self.__processList_byName = {}
        self.__processList_byPID = {}

        self.fields = self.fields[0] 
        # ['pid', 'name', 'username', 'cpu_percent', 'memory_percent']
        for p in self.fields:
             self.__processList_byName[ p['name'] ] = p
             self.__processList_byPID[ p['pid'] ] = p
    # end of the declaration of constructor

    def getProcessByName( self, _name ):
        if _name in self.__processList_byName:
            return self.__processList_byName[ _name ]
        else:
            return None 
    # end of getProcessByName()

    def getProcessByPID( self, _pid ):
        if _pid in self.__processList_byPID:
            return self.__processList_byPID[ _pid ]
        else: 
            return None 
    # end of getProcessByPID()

    def getProcessList(self):
        return self.fields
    # end of getProcessList()

    def toString(self):
        return "Process count: " + str( len( self.fields ) )
    # end of toString()


class SystemCall(object):

    def __init__(self, _sender, _content):
        self.__sender = _sender
        self.__type = 'System'

        data = _content.split( " " )

        if data[0] == "clock":
            self.__content = [ str( str( data[0] ) + " " + str( data[1] ) ), str( data[2] ) ]
        else:
            self.__content = _content
    # end of the declaration of constructor

    def getOwnerName(self):
        return self.__sender
    # end of getOwnerName()

    def getContent(self):
        return self.__content
    # end of getContent()
    def toString(self):
        return "Sender: " + self.__sender + "\nContent: " + self.__content
    # end of toString()    
     
# end of the discription of class SystemCall