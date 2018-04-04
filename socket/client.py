import socket
import sys

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

def parseResponse(results):
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
        if x == len(results.splitlines()) - 1:
            if responseLevel == 2:
                print("index.html was stored in \"response.txt\"")
        
if __name__ == "__main__":
    input = sys.argv[1]
    if http in input:
        noHTTP = input[input.find('/') + 2 : ]
        #print("RAW INPUT:    " + input)
        #print("NO HTTP:      " + noHTTP)

        #check for path
        if noHTTP.rfind("/") == -1:
            path = "/"
            #print("PATH:         " + path)
            pathlessURL = noHTTP
        else:
            path = noHTTP[noHTTP.find("/") : noHTTP.rfind("/") + 1]
            #print("PATH:         " + path)
            pathlessURL = noHTTP[0 : noHTTP.find("/")]
        
        #print("PATHLESS URL: " + pathlessURL)

        #check for port
        if pathlessURL.rfind(":") == -1:        
            port = 80
            #print("PORT:         {}".format(port))
            serverInput = pathlessURL
        else:
            serverInput = pathlessURL[0 : noHTTP.rfind(':')]
            port = int(pathlessURL[pathlessURL.find(":") + 1 : ])
            #print("HOSTNAME:     " + serverInput)
            #print("PORT:         {}".format(port))

    else:
        print("Invalid URL: Must be HTTP")

results = httpGET(serverInput, int(port), path)
parseResponse(results)





