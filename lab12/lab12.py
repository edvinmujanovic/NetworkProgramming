import firebase_admin
from firebase_admin import db
import tkinter as tk
import tkinter.scrolledtext as tksctxt

cred = firebase_admin.credentials.Certificate('lab12/lab12-firebase.json')  
firebase_admin.initialize_app(cred, {'databaseURL': 'https://lab12-5e3f9-default-rtdb.europe-west1.firebasedatabase.app/'})  
ref = firebase_admin.db.reference('/')

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")

        self.nameLbl = tk.Label(self.groupCon, text='Name', padx=10)
        self.nameLbl.pack(side="left")

        self.name = tk.Entry(self.groupCon, width=20)
        self.name.insert(tk.END, "")
        self.name.pack(side="left")

        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")

        self.msgText = tksctxt.ScrolledText(height=15, width=42, state=tk.DISABLED)
        self.msgText.pack(side="top")

        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")

        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")

        self.textIn = tk.Entry(self.groupSend, width=38)
        self.textIn.bind('<Return>', lambda event: self.sendMessage())
        self.textIn.pack(side="left")

        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")

        self.sendButton = tk.Button(self.groupSend, text='send', command=self.sendButtonClick)
        self.sendButton.pack(side="left")

    def clearButtonClick(self):
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.delete(1.0, tk.END)
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)

    def sendButtonClick(self):
        self.sendMessage()

    def handleMessage(self, message):
        self.printToMessages(f"{message['name']}: {message['text']}")

    def streamHandler(self, incomingData):
        if incomingData.event_type == 'put':
            if incomingData.path == '/':
                if incomingData.data is not None:
                    for key in incomingData.data:
                        message = incomingData.data[key]
                        self.handleMessage(message)
            else:
                message = incomingData.data
                self.handleMessage(message)

    def printToMessages(self, message):
        print(message)
        self.msgText.configure(state=tk.NORMAL)
        self.msgText.insert(tk.END, message + '\n')
        self.msgText.see(tk.END)
        self.msgText.configure(state=tk.DISABLED)

    def on_closing(self):
        self.myQuit()

    def myQuit(self):
        g_root.destroy()
        messages_stream.close()

    def sendMessage(self):
        newMessage = {'name': self.name.get(), 'text': self.textIn.get()}
        ref.child('messages').push(newMessage)

g_root = tk.Tk()
g_app = Application(master=g_root)

messages_stream = ref.child('messages').listen(g_app.streamHandler)

g_root.protocol("WM_DELETE_WINDOW", g_app.on_closing)

g_app.mainloop()
