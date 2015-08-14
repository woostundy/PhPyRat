import socket
import threading
import logging

allConnections = []
allAddresses = []
clientCount = 0
    
def main():
    threadCommand = threading.Thread(target=getCommand)
    threadCommand.start()
    threadService = threading.Thread(target=service)
    threadService.start()
    
def getCommand():
    while 1:
        command = raw_input("> ")
        if(command == "list"):
            print "pk------address-----------------port"
            pk = 1
            for i in allAddresses:
                print str(pk) +"------" + str(i[0]) + "---------" + str(i[1])
                pk += 1
        elif(command.startswith("c")):
            try:
                pk = int(command[2:])-1
                while 1:
                    try:
                        msg = raw_input("control %s:%s> " %(allAddresses[pk][0],allAddresses[pk][1]))
                        if(msg=="exit"):
                            break
                        allConnections[pk].send(msg)
                    except Exception , e:
                        print "error:" + e
                        continue
                            
            except:
                print "usage:c client_pk,exp:c 1"
                

def service():
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    port = 1937
    sock.bind( ('',port))
    sock.listen(5)
    while 1:
        try:
            conn, addr = sock.accept()
            conn.setblocking(1)
            print "Connected with " + addr[0] + ":" + str(addr[1])
            print "Totle Client: %d" %clientCount 
            allConnections.append(conn)
            allAddresses.append(addr)
        except:
            break


def sendMessage(msg,conn):
    try:
        conn.send(msg)
        return 1
    except:
        return 0    
    
            
main()
