import sys
import os
from socket import *

#open connection to ftp server and login
print('Please input the name or IP address of the server')
ipad = raw_input('myftp ')#input ip or server name
hostport = (ipad, 21)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(hostport)
print clientSocket.recv(1024)
user = raw_input('Username: ')#input user name
commandS = 'USER ' + user + '\r\n'
clientSocket.send(commandS)
print clientSocket.recv(1024)
password = raw_input('User Password: ')#input user password
commandS = 'PASS ' + password + '\r\n'
clientSocket.send(commandS)
print clientSocket.recv(1024)
address, dataPort = clientSocket.getsockname()

while True:
    inputcom = raw_input('myftp> ') #remind user to input command
    if inputcom.upper() == 'LS': #list files/folders in current directory
        dataPort += 1
        availablePort = False 
        while availablePort == False: #check if local port is available, if not try another port
            try:
                dataSocket = socket(AF_INET,SOCK_STREAM)
                dataSocket.bind(('',dataPort))
                availablePort = True
            except error:
                dataPort += 1
        
        lDataPort = str(int(hex(dataPort)[2:4], 16))
        rDataPort = str(int(hex(dataPort)[4:6], 16))
        arrayAddress = str.split(address, ".")

        commandS = 'PORT ' + arrayAddress[0] + "," + arrayAddress[1] + "," + arrayAddress[2] + "," + arrayAddress[3] + "," + lDataPort + ',' + rDataPort + '\r\n'
        clientSocket.send(commandS) #send port command, telling ftp server which local host port to connect to
        print clientSocket.recv(1024)
        clientSocket.send('LIST\r\n')#command to list files/folders

        dataSocket.listen(1)
        dataConn, addr = dataSocket.accept() 
        print clientSocket.recv(1024)
        print dataConn.recv(1024)
        dataConn.close()
        print clientSocket.recv(1024)
        dataSocket.close()

    elif inputcom[0:3].upper() == 'PUT': #transfer file to ftp server
        dataPort += 1
        availablePort = False
        while availablePort == False:
            try:
                dataSocket = socket(AF_INET,SOCK_STREAM)
                dataSocket.bind(('',dataPort))
                availablePort = True
            except error:
                dataPort += 1
        
        lDataPort = str(int(hex(dataPort)[2:4], 16))
        rDataPort = str(int(hex(dataPort)[4:6], 16))
        arrayAddress = str.split(address, ".")
        commandS = 'PORT ' + arrayAddress[0] + "," + arrayAddress[1] + "," + arrayAddress[2] + "," + arrayAddress[3] + "," + lDataPort + ',' + rDataPort + '\r\n'
        clientSocket.send(commandS)
        print clientSocket.recv(1024)

        commandT = 'STOR ' + inputcom[4:] + '\r\n' #send file transfer command
        clientSocket.send(commandT)

        dataSocket.listen(1)
        dataConn, addr = dataSocket.accept()
        print clientSocket.recv(1024)

        f = open(inputcom[4:]) #open file and transfer it
        transferFile = f.read()
        for i in range(0, len(transferFile)):
            dataConn.send(transferFile[i])
        f.close()

        dataConn.close()
        print clientSocket.recv(1024)
        dataSocket.close()
        ise = os.path.getsize(inputcom[4:])
        print('Successfully transfered '+ str(ise) + ' bytes')


    elif inputcom[0:3].upper() == 'CD ': #change to directory
        commandS = 'CWD ' + inputcom[3:] + '\r\n'
        clientSocket.send(commandS)
        print clientSocket.recv(1024)

    elif inputcom[0:3].upper() == 'GET': #get file from server
        dataPort += 1

        availablePort = False
        while availablePort == False:
            try:
                dataSocket = socket(AF_INET,SOCK_STREAM)
                dataSocket.bind(('',dataPort))
                availablePort = True
            except error:
                dataPort += 1
        
        lDataPort = str(int(hex(dataPort)[2:4], 16))
        rDataPort = str(int(hex(dataPort)[4:6], 16))
        arrayAddress = str.split(address, ".")
        commandT = 'PORT ' + arrayAddress[0] + "," + arrayAddress[1] + "," + arrayAddress[2] + "," + arrayAddress[3] + "," + lDataPort + ',' + rDataPort + '\r\n'
        clientSocket.send(commandT)
        print clientSocket.recv(1024)

        commandS = 'RETR ' + inputcom[4:] + '\r\n' #send get file command to ftp server
        clientSocket.send(commandS)

        dataSocket.listen(1)
        dataConn, addr = dataSocket.accept()
        print clientSocket.recv(1024)

        receiveFile = dataConn.recv(1024) #receive file
        f = open(inputcom[4:], 'w') #open and write file locally
        for line in receiveFile:
            f.write(line)
        f.close()

        dataConn.close()
        print clientSocket.recv(1024)
        dataSocket.close()
        ise = os.path.getsize(inputcom[4:])
        print('Successfully transfered '+ str(ise) + ' bytes')
    
    elif inputcom.upper() == 'QUIT': #close SOCKET connection and quit program
        clientSocket.send('QUIT\r\n')
        print clientSocket.recv(1024)
        clientSocket.close()
        quit()

    elif inputcom[0:6].upper() == 'DELETE': #delete file
        commandS = 'DELE ' + inputcom[7:] + '\r\n'
        clientSocket.send(commandS)
        print clientSocket.recv(1024)
    else:
        print("You can input command as below: \n ls              | List the files in the current directory on the remote server. \n cd              | Change the current directory to -remote-dir- on the remote server.\n get remote-file | Download the file -remote-file- from the remote server to the local machine. \n put             | local-file Upload the file -local-file- from the local machine to the remote server. \n delete file     | Delete the file -remote-file- from the remote server. \n quit            | Quit the FTP client\n")