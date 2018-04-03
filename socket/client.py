import socket
import sys

def httpGET(server, port):
    #s = socket.gethostbyname(server)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request = "GET / HTTP/1.0\r\nHost: " + server + "\r\n\r\n"
    s.connect((server,port))
    s.send(request.encode())
    results = s.recv(4096)
    print(results.decode())

#serverInput = input("Enter server: ")
#portInput = input("Enter port: ")
serverInput = 'www.google.com'
portInput = 80
httpGET(serverInput,portInput)

