from PyQt5 import QtCore, QtWidgets, QtGui
from Monitor_ui import Ui_MainWindow
from Fre_dialog_ui import Frequence_Dialog
from Database import Database
import sys
import threading
import time

class MyForm (QtWidgets.QMainWindow):
    def __init__(self, _ec=None, _mc=None, _db=None, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # communication components set up
        self.__ec = _ec 
        self.__messagecenter = _mc
        self.__db = _db

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # hardware_tree set up
        self.ui.hardware_tree.setHeaderLabels(["HostName","Value"])
        self.load_hardware_status()
        self.ui.hardware_tree.expandAll()
        self.ui.hardware_tree.resizeColumnToContents(0)
        self.ui.hardware_tree.setContextMenuPolicy(3)
        self.ui.hardware_tree.customContextMenuRequested.connect(self.slave_cmd_menu)
        self.ui.hardware_tree.itemClicked.connect(self.tree_click_handler)
        # menu bar set up
        self.ui.menuMaster.triggered.connect(self.menubar_handler)
        # process table menu set up
        self.load_process_table(None)
        self.ui.process_table.setContextMenuPolicy(3)
        self.ui.process_table.customContextMenuRequested.connect(self.process_cmd_menu)
        


    # click the top level of tree and laod the Os table and process table.
    def tree_click_handler(self, item, col):
        if not item.parent():
            # print(item.text(0))
            self.ui.label_hostnmae.setText(item.text(0))
            # start to laod OS table and Process table here.
            self.load_OS_table(item.text(0))
            self.load_process_table(item.text(0))


    # get the hardware msg from getter.
    def load_hardware_status(self):
        # get the hardware msg from getter.
        '''
        machineList = self.__db.getMachineNameList()

        for name in machineList:
            parent = QtWidgets.QTreeWidgetItem(self.ui.hardware_tree)
            parent.setText(0, name )
            HWData = self.__db.getType1Data(1, name)
            ls = ["Physical CPU","Logical CPU","Min CPU frequence","Max CPU frequence","Memory size","Boost time"]
            for x in ls:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, x)
                if x == "Physical CPU":
                    child.setText(1, HWData['phy_cpu'])
                elif x == "Logical CPU":
                    child.setText(1, HWData['log_cpu'])
                elif x == "Min CPU frequence":
                    child.setText(1, HWData['min_cpu_freq'])
                elif x == "Max CPU frequence":
                    child.setText(1, HWData['max_cpu_freq'])
                elif x == "Memory size":
                    child.setText(1, HWData['mem_size'])
                elif x == "Boost time":
                    child.setText(1, HWData['boot_time'])
        '''
        machineList = ['s1','s2','s3']

        for name in machineList:
            parent = QtWidgets.QTreeWidgetItem(self.ui.hardware_tree)
            parent.setText(0, name )
            ls = ["Physical CPU","Logical CPU","Min CPU frequence","Max CPU frequence","Memory size","Boost time"]
            for x in ls:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, x)
                child.setText(1, "text~~")

    
    # change last update time evey while loading table.
    def load_update_time(self):
        t = time.asctime()
        self.ui.label_time.setText(t)

    # laod the OS status here.
    def load_OS_table(self, _hostname):
        self.load_update_time()
        senser = []
        value = []
        Max = []
        Min = []
        max_stats = __db.getOSHistoryData( _hostname, 'max' )
        min_stats = __db.getOSHistoryData( _hostname, 'min' )
        cur_stats = __db.getType2Data(_name = _hostname)[0]
        senser = ['cpu_usr', 'cpu_sys', 'cpu_idle', 'mem_per']
        value = [cur_stats['cpu_usr'], cur_stats['cpu_sys'], cur_stats['cpu_idle'], cur_stats['mem_percent']]
        Max = [max_stats['cpu_usr'], max_stats['cpu_sys'], max_stats['cpu_idle'], max_stats['mem_per']]
        Min = [min_stats['cpu_usr'], min_stats['cpu_sys'], min_stats['cpu_idle'], min_stats['mem_per']]

        self.ui.OS_table.setRowCount(4)
        for row in range(4):
            item_senser = QtWidgets.QTableWidgetItem(senser[row])
            item_value = QtWidgets.QTableWidgetItem(value[row])
            item_max = QtWidgets.QTableWidgetItem(Max[row])
            item_min = QtWidgets.QTableWidgetItem(Min[row])
            # setItem(row num, column num, table_Item)
            self.ui.OS_table.setItem( row, 0, item_senser )
            self.ui.OS_table.setItem( row, 1, item_value )
            self.ui.OS_table.setItem( row, 2, item_max )
            self.ui.OS_table.setItem( row, 3, item_min )

    # load process status here.
    def load_process_table(self, _hostname):
        self.load_update_time()
        ''' 
        pid = []
        name = []
        username = []
        cpu_usg = []
        mem_usg = []
        i = 0
        for p in __db.getType3Data(_name = _hostname)[0]:
            pid.append(p['pid'])
            name.append(p['name'])
            username.append(p['username'])
            cpu_usg.append(p['cpu_percent'])
            mem_usg.append(p['memory_percent'])
            i = i + 1

        self.ui.process_table.setRowCount(i)
        for row in range(i):
            item_pid = QtWidgets.QTableWidgetItem(pid[row])
            item_name = QtWidgets.QTableWidgetItem(name[row])
            item_username = QtWidgets.QTableWidgetItem(username[row])
            item_cpu_usg = QtWidgets.QTableWidgetItem(cpu_usg[row])
            item_mem_usg = QtWidgets.QTableWidgetItem(mem_usg[row])
            # setItem(row num, column num, table_Item)
            self.ui.process_table.setItem( row, 0, item_pid )
            self.ui.process_table.setItem( row, 1, item_name )
            self.ui.process_table.setItem( row, 2, item_username )
            self.ui.process_table.setItem( row, 3, item_cpu_usg )
            self.ui.process_table.setItem( row, 4, item_mem_usg )
        '''
        pid = ['0001', '0012']
        name = ['python3', 'Adobe CS6']
        username = ['Tom', 'Jack']
        cpu_usg = ['10%', '25%']
        mem_usg = ['0.5%','1.2%']
        self.ui.process_table.setRowCount(2)
        for row in range(2):
            item_pid = QtWidgets.QTableWidgetItem(pid[row])
            item_name = QtWidgets.QTableWidgetItem(name[row])
            item_username = QtWidgets.QTableWidgetItem(username[row])
            item_cpu_usg = QtWidgets.QTableWidgetItem(cpu_usg[row])
            item_mem_usg = QtWidgets.QTableWidgetItem(mem_usg[row])
            # setItem(row num, column num, table_Item)
            self.ui.process_table.setItem( row, 0, item_pid )
            self.ui.process_table.setItem( row, 1, item_name )
            self.ui.process_table.setItem( row, 2, item_username )
            self.ui.process_table.setItem( row, 3, item_cpu_usg )
            self.ui.process_table.setItem( row, 4, item_mem_usg )

    def slave_cmd_menu(self, pos):
        index = self.ui.hardware_tree.indexAt(pos)        
        item = self.ui.hardware_tree.itemAt(pos)
        # only parent can be right clicked
        if index.parent().isValid() or item == None:
            return
        host_name = item.text(0)

        menu = QtWidgets.QMenu()
        freq = menu.addAction('Set update frequence' )
        start = menu.addAction('Send start transmit message to "' + host_name +'"')
        stop = menu.addAction('Send stop transmit message to "' + host_name +'"' )
        menu.addSeparator()
        term = menu.addAction('Send terminate message to "' + host_name +'"')
        action = menu.exec_(self.ui.hardware_tree.mapToGlobal(pos))
        if action == freq:
            widget = FrequenceDialog()
            widget.setWindowTitle('Set frequence')
            widget.exec_()
            if widget.fre != None:
                print(widget.fre)
        elif action == start:
            msg = self.__ec.encodeMsg_out( "sys", "start transmit", host_name )
            self.__messagecenter.sendNewMessage( msg )
        elif action == stop:
            msg = self.__ec.encodeMsg_out( "sys", "stop transmit", host_name )
            self.__messagecenter.sendNewMessage( msg )
        elif action == term:
            msg = self.__ec.encodeMsg_out( "sys", "terminate", host_name )
            self.__messagecenter.sendNewMessage( msg )

    def process_cmd_menu(self, pos):
        try:
            index = self.ui.process_table.itemAt(pos).row()
        except AttributeError:
            return
        pid = self.ui.process_table.item(index,0).text()

        menu = QtWidgets.QMenu()
        kill = menu.addAction('Kill process')
        action = menu.exec_(self.ui.process_table.mapToGlobal(pos))
        if action == kill:
            print('kill cmd in row{}, pid{}'.format(index, pid))

    def menubar_handler(self, action):
        print(action.text())
        


class GuiThread(threading.Thread):
    def __init__(self, _ec, _mc, _db ):
        threading.Thread.__init__(self, daemon=True)
        self.__ec = _ec # encoder
        self.__messageCenter = _mc # messageCenter
        self.__db = _db # database

    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        form = MyForm( self.__ec, self.__messageCenter, self.__db )
        form.setWindowTitle('Main Title here !')
        form.show()
        sys.exit(app.exec_())

class FrequenceDialog(QtWidgets.QDialog, Frequence_Dialog):
    def __init__(self, parent=None):
        super(FrequenceDialog, self).__init__(parent)
        self.fre = None
        self.setupUi(self)
        self.btn_submit.clicked.connect(self.submit)

    def submit(self):
        self.fre = self.text_freq.text()
        self.accept()
    


if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        form = MyForm()
        form.setWindowTitle('Main Title here !')
        form.show()
        sys.exit(app.exec_())

