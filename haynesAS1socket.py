import select
import socket

TIMEOUT = 10     # unit in seconds
BUF_SIZE = 2048  # unit in bytes

# sample code at isidore resources
class TCPsocket:
    # list our instance variables
    # constructor

    def __init__(self):
        self.sock = None  # each object's instacne variable
        self.host = ""  # remote host name
        print ("create an object of TCP socket")

        # add another method!
        # create a TCP socket

    def createSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #print ("create a TCP socket")
        except socket.error as e:
            print("Failed to create TCP socket ()".format(e))
            self.sock = None

    # how to figure out a remote server's IP?
    # www.google.com --> host name
    # given host name, how to get its ip address

    def getIP(self, hostname):
        self.host = hostname
        try:
            ip = socket.gethostbyname(hostname)  # ip is local
        except socket.gaierror:
            print ("Failed to gethostname")
            return None
        return ip

    # connect to a remote server: IP address, port

    def connect(self, ip, port):
        if self.sock is None or ip is None:
            return
        try:
            self.sock.connect((ip, port))  # server address is defined by (ip, port)
            print ("successfully connect to host", ip)
        except socket.error as e:
            print ("Failed to connect: ()".format(e))
            self.sock.close()
            self.sock = None

    # return the number of bytes sent
    def send(self, request):
        bytesSent = 0  # bytesSent is a local variable
        if self.sock is None:
            return 0
        try:
            bytesSent = self.sock.sendall(request.encode())  # encode (): convert string to bytes
        except socket.error as e:
            print("socket error in send ()".format(e))
            self.sock.close()
            self.sock = None
        return bytesSent

    def receive(self):
        if self.sock is None:
            return ""
        reply = bytearray()  # b'', local variable, bytearray is mutable
        bytesRecd = 0  # local integer

        self.sock.setblocking(0)  # flag 0 to set non-blocking mode of the socket
        ready = select.select([self.sock], [], [], TIMEOUT)  # https://docs.python.org/3/library/select.html
        if ready[0] == []:  # timeout
            print("Timeout on", self.host)
            return ""
        # else reader has data to read
        try:
            while True:  # use a loop to receive data until we recevie all data
                data = self.sock.recv(BUF_SIZE)  # returned chunk of data with max lenght BUF_SIZE is in bytes
                if data == b'':  # if empty bytes
                    break
                else:
                    reply += data  # append to reply
                    bytesRecd += len(data)
        except socket.error as e:
            print("socket error in receive: {}".format(e))
            self.sock.close()
            self.sock = None
        return reply

    # Close socket
    def close(self):
        if not (self.sock is None):
            self.sock.close()

    def crawl(self, host, port, message): # host string, port string, message
        self.createSocket()
        ip = self.getIP(host)
        self.connect(ip, port)
        self.send(message)
        reply = self.receive()
        print("received bytes: ", len(reply))
        if len(reply) > 0:
            for line in reply.decode('utf-8').split('\n'):
                print(line)
        self.close()
