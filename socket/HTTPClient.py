import socket
import sys
import os.path
import codecs

http = "http://"

def httpGET(server, port, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    userAgent = 'VCU-CMSC491'
    request = "GET {} HTTP/1.0\r\nHost: ".format(path) + server + "\nUser-Agent: " + userAgent + "\r\n\r\n"
    print("GET request:\n")
    print(request)
    s.settimeout(5)
    try:
        s.connect((socket.gethostbyname(server),port))
    except socket.error:
        print("Error: Port not available or not open, exiting program")
        sys.exit()
    s.send(request.encode())
    results = s.recv(4096)
    #print(results.decode())
    return results.decode()

def GETResponse(results):
    html = False
    for x in range(0,len(results.splitlines())):
        currentLine = results.splitlines()[x]
        if x == 0:
            responseCode = currentLine[9 : ]
            print("Response code: " + responseCode)
            responseLevel =int(responseCode[0])
            print("Size of response: {} bytes".format(sys.getsizeof(results)))      
        if currentLine.find("Location") != -1:
            if responseLevel == 3:
                print(currentLine)
        if currentLine.find("Server") != -1:
            print(currentLine)
        if currentLine.find("Date") != -1:
            if responseLevel == 2:
                print("Last Modified " + currentLine)

        if html:
            f = open("response.txt", "a+")
            f.write(currentLine)
            f.close()   
    
        if currentLine.find("doctype") != -1:
            f = open("response.txt", "w+")
            f.write(currentLine)
            f.close()
            html = True
        if x == len(results.splitlines()) - 1 and html == True:
            if responseLevel == 2:
                print("index.html was stored in \"response.txt\"")

    
        
def httpPUT(server, port, path, desiredFilePath):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    userAgent = 'VCU-CMSC491'
    rawFile = desiredFilePath[desiredFilePath.rfind("/") + 1 : ]
    f = open(desiredFilePath, "r")
    if f.mode == "r":
        contents = f.read()
        f.close()

    request = "PUT {} HTTP/1.0\r\nHost: ".format(path) + server + "\nFile-Location: " + desiredFilePath + "\nUser-Agent: " + userAgent + "\nContents-of: {}\n".format(rawFile) + contents + "\r\n\r\n"
    print("PUT request:\n")
    print(request)
    s.settimeout(5)
    s.connect((socket.gethostbyname(server),port))
    s.send(request.encode())
    results = s.recv(4096)
    print("FROM SERVER: \n" + results.decode())
    return results.decode()


if __name__ == "__main__":
    if sys.argv[1] == "PUT":
        input = sys.argv[2]
        if os.path.isfile(sys.argv[3]):
            desiredFilePath = sys.argv[3]
            putRequest = True
        else:
            print("No valid file path, path must start with '.'")
            sys.exit()
    else:
        input = sys.argv[1]
        putRequest = False
    if http in input:
        noHTTP = input[input.find('/') + 2 : ]

        if noHTTP.rfind("/") == -1:
            path = "/"
            pathlessURL = noHTTP
        else:
            path = noHTTP[noHTTP.find("/") : ]
            pathlessURL = noHTTP[0 : noHTTP.find("/")]

        if pathlessURL.rfind(":") == -1:        
            port = 80
            serverInput = pathlessURL
        else:
            serverInput = pathlessURL[0 : noHTTP.rfind(':')]
            port = int(pathlessURL[pathlessURL.find(":") + 1 : ])
    else:
        print("Invalid URL: Must be HTTP, not HTTPS")


if putRequest:
    results = httpPUT(serverInput, int(port), path, desiredFilePath)
elif not putRequest: 
    results = httpGET(serverInput, int(port), path)
    print("FROM SERVER: \n")
    GETResponse(results)
    





