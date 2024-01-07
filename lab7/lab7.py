import socket
import select

PORT = 60004
sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockServer.bind(("", PORT))
sockServer.listen(1)

listOfSockets = [sockServer]

print("Listening on port {}".format(PORT))

while True:
    readable, _, _ = select.select(listOfSockets, [], [])

    for sock in readable:
        if sock == sockServer:
            (sockC, addr) = sockServer.accept()
            listOfSockets.append(sockC)
            for s in listOfSockets:
                if s != sockServer and s != sockC:
                    s.send(f"[{addr[0]}:{addr[1]}] (connected)\n".encode()) #hostnumber och portnumber 
        else: #disconnect
            data = sock.recv(1024) 
            if not data: 
                print(f"Client disconnected: {sock.getpeername()}")
                listOfSockets.remove(sock)
                sock.close() 
                for s in listOfSockets:
                    if s != sockServer:
                        s.send(f"[{sock.getpeername()}] (disconnected)\n".encode()) #skickar meddelande till clients
            else:  
                for s in listOfSockets:
                    if s != sockServer:
                        s.send(f"[{sock.getpeername()}] {data.decode()}".encode()) 
