import socket
import sys

def httpGET(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    path = '/'
    request = "GET / HTTP/1.0\nHost: " + server + "\nPath: " + path + "\n\n"
    s.connect((socket.gethostbyname(server),port))
    s.send(request.encode())
    results = s.recv(4096)
    print(results.decode())

#if __name__ == "__main__":
   # input = sys.argv[1]
   # print(input[0])

serverInput = 'www.cnn.com'
portInput = 80
httpGET(serverInput,portInput)

