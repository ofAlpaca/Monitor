"""CPU usage requirement should not be called too frequently, each should have at least 1 second interval"""

import psutil, re, sys
from datetime import datetime

class DataGetter(object):

    def __init__(self):
        self.physical_cpu = psutil.cpu_count(False) #quantity of cpu
        self.logical_cpu = psutil.cpu_count()
        self.sys_platform = sys.platform
        if self.sys_platform != 'linux' :
                self.cpu_min_freq = re.split('\(|\)|, |=', str(psutil.cpu_freq()))[4] #Mhz
                self.cpu_max_freq = re.split('\(|\)|, |=', str(psutil.cpu_freq()))[6]
        self.mem_size = re.split('\(|\)|, |=', str(psutil.virtual_memory()))[2] #bytes
        self.boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        self.getData(1)
        self.getData(2)
        self.getData(3)

        # further required data can be added here
    # __init__()

    def getData(self, _type):
        
        if _type == 1: # Machine Spec
            if self.sys_platform != 'linux' :
                rtn = [self.physical_cpu, self.logical_cpu, self.cpu_min_freq, self.cpu_max_freq, self.mem_size, self.boot_time ]
            else :
                rtn = [self.physical_cpu, self.logical_cpu, 'linux is not supported', 'linux is not supported.', self.mem_size, self.boot_time]
        elif _type == 2: # CPU and Memory Usage
            cpuu = re.split('\(|\)|, |=', str(psutil.cpu_times_percent()))
            memu = re.split('\(|\)|, |=', str(psutil.virtual_memory()))
            rtn = [cpuu[2], cpuu[4], cpuu[6], memu[2], memu[4], memu[8], memu[6] ] #CPU usage: user, system, idle and Memory usage: total, available, used, percentage used in sequence
        elif _type == 3: # list all process
            processes_info = []
            for proc in psutil.process_iter():
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent'])
                    pinfo['cpu_percent'] = pinfo['cpu_percent']/psutil.cpu_count()
                    if pinfo['cpu_percent'] > 0.0 :
                        processes_info.append(pinfo)
                    else:
                        pass
                except psutil.NoSuchProcess:
                    pass

            rtn = processes_info 

       

        return [ rtn, datetime.now().strftime("%Y-%m-%d %H:%M:%S") ]
        # more data type can be added here
    # getData()

if __name__ == '__main__':
    try:
        while(True):
            dg = DataGetter()
            print(dg.getData(1))
            print(dg.getData(2))
            print(dg.getData(3))
            input("PRESS ENTER TO CONTINUE OR CTRL + C TO QUIT")
    except KeyboardInterrupt:
        pass
