import socket
import sys
from pathlib import Path
import datetime
import os.path

def httpResponse(decodedMessage, addr):
    firstLine = decodedMessage.splitlines()[0]   
    request = firstLine[0 : 3] 
    clientInfo = addr[0] + ":" + str(addr[1]) + ":" + request + "\n"
    print(clientInfo)
    if firstLine.find("GET") != -1:
        file = "." + firstLine[4 : firstLine.find("HTTP") - 1]
        
        filePath = Path(file)
        if filePath.exists():
            response = "HTTP/1.0 200 OK\n"
        else:
            response = "HTTP/1.0 404 Not Found\n"
        
        now = datetime.datetime.now()
        date = now.strftime("Date: %a, %d %b %Y %H:%M:%S EST") + "\n"

        response = response + date

        for x in range(0, len(decodedMessage.splitlines())):
            currentLine = decodedMessage.splitlines()[x]
            if currentLine.find("User-Agent") != -1:
                userAgent = currentLine

        response = response + userAgent

        if os.path.isfile(file):
            f = open(file, "r")
            if f.mode == "r":
                contents = f.read()
                response = response + "\n\n" + contents

    elif firstLine.find("PUT") != -1:
        file = "." + firstLine[4 : firstLine.find("HTTP") - 1]
        filePath = Path(file)
        locationLine = decodedMessage.splitlines()[2]
        fileLocation = locationLine[15 : ]
        rawFile = fileLocation[fileLocation.rfind("/") + 1 : ]
        fileDestination = file + rawFile

        if os.path.isfile(fileLocation):
            f = open(fileLocation, "r")
            if f.mode == "r":
                contents = f.read()
                endRead = True
                f.close()
        else:
            print("PUT requested file does not exist")
            sys.exit()
        
        if endRead:
            f = open(fileDestination, "w+")
            f.write(contents)
            f.close()
            #print(contents)
            #print("\n" + rawFile + " was read from " + fileLocation + " and written to " + fileDestination)
        
        
        if os.path.isfile(fileLocation):
            response = "HTTP/1.0 200 OK\n"
            responseCode = "Response code: " + response[9 : 12] + "\n"
        else:
            response = "HTTP/1.0 606 FAILED File NOT Created\n" 
            responseCode = "Response code: " + response[9 : 12] + "\n"

        response = response + responseCode
        response = response + "Server: Local server\n"


    return response.encode()

    
    
args = sys.argv

if len(args) >= 10000 or len(args) <= 11000:
    port = int(args[1])
elif args > 65536:
    print("Port must be less than 65536")
    sys.exit()
else:
    print("Valid ports are between 10000 - 11000")
    sys.exit()

# Create welcoming socket using the given port
welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSocket.bind(('', port))
welcomeSocket.listen(1)

print("Listening on port {} ...".format(port))

while 1:

    connectionSocket, addr = welcomeSocket.accept()
    print("Client Made Connection")

    clientRequest = connectionSocket.recv(1024)
    decodedMessage = clientRequest.decode()
    print("FROM CLIENT: \n" + decodedMessage)

    response = httpResponse(decodedMessage, addr)

    connectionSocket.send(response)
    print("TO CLIENT: \n" + response.decode())

    connectionSocket.close()
