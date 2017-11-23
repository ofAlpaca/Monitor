from Database import Database
from SystemDeliveryObjects import Status_Software

class Analyzer(object):
    """description of class"""
    def __init__(self, _db ):
        self.__db = _db
        self.__update = False
        self.__historyData = self.__db.getOSHistoryData()
    # end of the declaration of constructor

    def analyzeData(self, _obj ):

        if isinstance( _obj, Status_Software ):
            name = _obj.getOwnerName() 
            if name in self.__historyData:
                cpuTotal_record = float( self.__historyData[name]['cpu_sys'] ) + float( self.__historyData[name]['cpu_usr'] )
                cpuTotel_current = float( _obj.getCPU_sys() ) + float( _obj.getCPU_usr() )

                if cpuTotel_current > cpuTotal_record:
                    self.__update = True
                    self.__db.updateOSHistory( name, 'cpu', [ _obj.getCPU_usr(), _obj.getCPU_sys(),_obj.getCPU_idle()] )
                else:
                    pass

                if float( _obj.getMem_percent() ) > float( self.__historyData[name]['mem_per'] ):
                    self.__update = True
                    self.__db.updateOSHistory( name, 'mem_per', _obj.getMem_percent() )
                else:
                    pass

            else:
                self.__db.insertOSHistory( _obj )
                self.__update = True

            if self.__update:
                self.__historyData = self.__db.getOSHistoryData()
                self.__update = False
            else:
                pass
        else:
            pass
    # end of analyzeData()