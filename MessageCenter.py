import socket
import threading
import traceback
import queue
import pickle
import logging
from Coder import Encoder

# initial logger
# logger = logging.getLogger(__name__)

class MessageCenter(threading.Thread):
    def __init__(self, _localhost, _refer_hashtable):
        threading.Thread.__init__(self, daemon=True)
        self.logger = logging.getLogger('MonitorApplication')
        self._qMessageQueue = queue.Queue()
        self.localHost = _localhost
        self.reference = _refer_hashtable
        self.encoder = Encoder(self.localHost, self.reference)
        # use to shutdown server.
        self.shutdown = False

    def run(self):
        s = self.__makeserversocket()
        # set connection timeout for 2 seconds.
        # s.settimeout(5)
        #logging.getLogger('Server start at: {}'.format(self.localHost))
        self.logger.debug('Server start: {} {}:{}'.format(self.localHost.getName(), self.localHost.getIP(), self.localHost.getPort()))
        # logging.getLogger('Server start: {} {}:{}'.format(self.localHost.getName(), self.localHost.getIP(), self.localHost.getPort()))

        while not self.shutdown:
            try:
                # when new connection is coming.
                clt_sock, clt_addr = s.accept()
                self.logger.debug('A new connection coming...')
                clt_sock.settimeout(None)

                # make a thread to let it handle the msg.
                t = threading.Thread(target=self.__handleconnection, args=[clt_sock])
                self.logger.debug('Start a new thread')
                t.daemon = True
                t.start()
            except KeyboardInterrupt:
                self.shutdown = True
                continue
            except:
                if True:
                    traceback.print_exc()
                continue

        self.logger.debug('Main loop exiting...')
        s.close()

    def __makeserversocket(self, backlog=5):
        # specify the connection type, here is (use internet, TCP connection).
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        # set the socket port can be reused.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # prepare the socket and port.
        s.bind((self.localHost.getIP(), int(self.localHost.getPort())))
        # start listening the socket and allow the 'backlog' number of connection.
        s.listen(backlog)
        return s

    def __handleconnection(self, clientsocket, reply=None):
        # get the ip and port number of client(peer) side .
        # sender_host, sender_port = clientsocket.getpeername()
        
        # create a ConnectionPort to receive and reply to the connection.
        msgconn = ConnectionPort(None, None, clientsocket) # the value of host and port doesnt matter as long as you have socket.
        try:
            # accept the msg.
            newmsg = msgconn.recv_data()
            sender_host = newmsg.getSender()
            sender_port = newmsg.getPort()
            # is the msg in the ip hash table ? no corresponding key should return None.
            sender_name = self.reference.get(sender_host)
            if sender_name != None:
                self.encoder.encodeMsg_in(newmsg.getType(), newmsg.getContent(), sender_host)
                self.logger.debug('{} receive msg from {} {}:{} : {}'.format(self.localHost.getName(), sender_name, sender_host, sender_port, newmsg.getContent()))
                if reply:
                    # repsonse should be a msg object which you want to reply.
                    msgconn.send_data(reply)
                
                # saving msg.
                newmsg.setSenderName( sender_name )
                self._qMessageQueue.put(newmsg)
            else:
                # discard the msg .
                self.logger.debug('The message from {} {} is not acceptable.'.format(sender_name, sender_host))
        except :
            if True:
                traceback.print_exc()

        self.logger.debug('Disconnecting' + str(clientsocket.getpeername()))
        msgconn.close()

    def getNewMessage(self):
        # pop msg once a time.
        try:
            msg = self._qMessageQueue.get(False)
            return msg
        except queue.Empty:
            return None

    def sendNewMessage(self, _newMsg ):
        # suppose A sends to B 
        host = _newMsg.getDestination() # B's ip
        port = _newMsg.getPort() # B's por
        pid = _newMsg.getSender()  # A's IP

        # send msg to a host and get its reply.
        msgreply = []
        try:
            # make connection to the the other peer side.
            msgconn = ConnectionPort(host, port)
            msgconn.send_data(_newMsg)
            self.logger.debug('{} sent msg to {}:{} : {}'.format(pid, host, port, _newMsg))
            # accept the reply.
            replymsg = msgconn.recv_data()
            while replymsg != None:
                msgreply.append(replymsg)
                self.logger.debug('{} got reply from {}:{} : {}'.format(pid, host, port, replymsg))
                replymsg = msgconn.recv_data()
        except KeyboardInterrupt:
            raise
        except socket.error as e:
            self.logger.debug(str(e))
            return None
        except:
            if True:
                traceback.print_exc()

        return msgreply

    def isQueueEmpty(self):
    # is the msg queue empty ?
        if self._qMessageQueue.empty():
            return True
        else:
            return False


class ConnectionPort():
    def __init__(self, host, port, sock=None):
        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = sock

    def __makemsg(self, msg_obj):
        # make the data into pickle format.
        # msg_data = [msgtype, msgdata]
        msg = pickle.dumps(msg_obj)
        return msg

    def __readmsg(self, recvmsg):
        msg = pickle.loads(recvmsg)
        return msg

    def recv_data(self):
        try:
            msg = self.__readmsg(self.s.recv(4096))
            return msg
        except KeyboardInterrupt:
            raise
        except EOFError:
            # out of msg
            return None
        except :
            if True:
                traceback.print_exc()
            return None
            
    def send_data(self, msg_obj):
        try:
            msg = self.__makemsg(msg_obj)
            self.s.send(msg)
        except KeyboardInterrupt:
            raise
        except:
            if True:
                traceback.print_exc()
            return False
        return True

    def close(self):
        self.s.close()
        self.s = None
    


