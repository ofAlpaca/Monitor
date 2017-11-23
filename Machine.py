class Machine(object):
    """description of class"""

    def __init__(self, _name, _ip, _port):
        self.name = _name 
        self.ip = _ip 
        self.port = _port 

    def getName(self):
        return self.name 
    # end of getName()

    def getIP(self):
        return self.ip
    # end of getIP()

    def getPort(self):
        return self.port
    # end of getPort()

    def toString(self):
        return  "Name: " + self.name + ", IP: " + self.ip + ", Port: " + self.port 
    # end of toString()

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%s" % (self.name, self.ip, self.port )
