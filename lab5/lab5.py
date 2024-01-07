import socket

wins4win = 3
enemyScore = 0
myScore = 0

def serversideGetPlaySocket():
    socketServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    socketServer.bind(("127.0.0.1", 60002))
    socketServer.listen(1)
    (socketClient, addr) = socketServer.accept()
    print("Connection from {}".format(addr))
    gameLoop(socketClient)
    socketClient.close()
    socketServer.close()

def clientsideGetPlayerSocket(host):
    socketClient = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    socketClient.connect((host, 60002))
    gameLoop(socketClient)
    socketClient.close()

def checkInput(myMove, enemyMove):
    global myScore
    global enemyScore
    if (myMove == "R" and enemyMove == "S") or (myMove == "P" and enemyMove == "R") or (myMove == "S" and enemyMove == "P"):
        myScore += 1
    if (enemyMove == "R" and myMove == "S") or (enemyMove == "P" and myMove == "R") or (enemyMove == "S" and myMove == "P"):
        enemyScore += 1

def inputValidation():
    inputValue = ""
    while inputValue not in {"R", "S", "P"}:
        print("The only valid moves are P, S, and R")
        inputValue = input("Make Move: ").upper()
    return inputValue

def gameLoop(socket):
    global myMove
    global enemyMove
    while True:
        myMove = inputValidation()
        socket.sendall(bytearray(myMove, "ascii"))
        print("Sent:", myMove)
        enemyMove = socket.recv(1024).decode("ascii")
        print("Received:", enemyMove)
        checkInput(myMove, enemyMove)
        print("Your move:", myMove)
        print("Opponent's move:", enemyMove)
        print("Your score:", myScore)
        print("Opponent's score:", enemyScore)
        if myScore == wins4win:
            print("You Won")
            break
        elif enemyScore == wins4win:
            print("Enemy Won")
            break

def onStart():
    ans = "?"
    while ans not in {"C", "S"}:
        ans = input("Do you want to be server (S) or client (C): ")
        if ans == "S":
            serversideGetPlaySocket()
        elif ans == "C":
            host = input("Enter the server's name or IP: ")
            clientsideGetPlayerSocket(host)

if __name__ == '__main__':
    onStart()

