import socket

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print(f"Server is listening on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # hämtar clientens request
        request = client_socket.recv(1024).decode("ASCII")
        print("Client Request:")
        print(request)

        #responsen
        response = "HTTP/1.1 200 OK\n"
        response += "Content-Type: text/html\n\n"
        response += "<html>\n"
        response += "<pre>\n"
        response += request 
        response += "\n</pre>\n"
        response += "</html>\n"

        #skickar responsen
        client_socket.sendall(bytearray(response, "ASCII"))

    
        client_socket.close()

if __name__ == '__main__':
    port = 8080  
    start_server(port)
