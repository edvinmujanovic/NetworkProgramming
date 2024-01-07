import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
import socket

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        #
        self.ipPortLbl = tk.Label(self.groupCon, text='IP:port', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.ipPort = tk.Entry(self.groupCon, width=20)
        self.ipPort.insert(tk.END, 'localhost:60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.ipPort.bind('<Return>', connectHandler)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon,
            command=connectButtonClick, width=10)
        self.connectButton.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command=clearButtonClick)
        self.clearButton.pack(side="left")
        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")
        
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text='send',
            command=sendButtonClick)
        self.sendButton.pack(side="left")

        # set the focus on the IP and Port text field
        self.ipPort.focus_set()

def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

def connectButtonClick():
    connectHandler(g_app)

def sendButtonClick():
    sendMessage(g_app)

def connectHandler(master):
    if g_bConnected:
        disconnect()
    else:
        tryToConnect()

def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

def on_closing():
    if g_bConnected:
        if tkmsgbox.askokcancel("Quit",
            "You are still connected. If you quit you will be"
            + " disconnected."):
            myQuit()
    else:
        myQuit()

def myQuit():
    disconnect()
    g_root.destroy()

def myAddrFormat(addr):
    return '{}:{}'.format(addr[0], addr[1])

def disconnect():
    global g_bConnected
    global g_sock

    if g_bConnected:
        g_sock.close()
        g_bConnected = False
    g_app.connectButton["text"] = "connect"

def tryToConnect():
    global g_bConnected
    global g_sock

    ip, port = g_app.ipPort.get().split(":")
    g_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    g_sock.settimeout(0.1)
    try:
        g_sock.connect((ip, int(port)))
        g_bConnected = True
        g_app.connectButton["text"] = "disconnect"
        printToMessages("connected" + myAddrFormat(g_sock.getpeername()))
    except socket.error as e:
        printToMessages("could not" + ip + ":" + port)
        g_sock.close()
        g_sock = None
        g_bConnected = False

def sendMessage(master):
    input = g_app.textIn.get()
    if input:
        g_app.textIn.delete(0, tk.END)
        try:
            g_sock.sendall(input.encode("ascii"))
        except socket.error as e:
            printToMessages("No message got send")
            disconnect()

def pollMessages():
    g_root.after(g_pollFreq, pollMessages)
    while g_sock:
        try:
            g_sock.setblocking(False)
            data = g_sock.recv(1024)
            if not data:
                break
            printToMessages(data.decode("ascii"))
        except:
            break

g_bConnected = False
g_sock = None
g_pollFreq = 200

g_root = tk.Tk()
g_app = Application(master=g_root)

disconnect()

g_root.after(g_pollFreq, pollMessages)
g_root.protocol("WM_DELETE_WINDOW", on_closing)
g_app.mainloop()
