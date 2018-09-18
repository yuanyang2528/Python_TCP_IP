# _*_ utf-8 _*_
import os
import zipfile
from socket import *

def unZip(filePath,unzipPath):
    file = zipfile.ZipFile(filePath)
    file.extractall(unzipPath)
	
#Please use server ip address
#HOST = "127.0.0.0"

PORT = 39576
ADDR = (HOST,PORT)

client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)
folder = os.getcwd() + '\ReceivedFiles'

AllowedRecvData = True
PrintRecvLog = True
if not os.path.exists(folder):
	os.makedirs(folder)
	
if os.path.isfile('ReceivedFiles.zip') == True:
	os.remove("./ReceivedFiles.zip")


with open("./ReceivedFiles.zip","ab") as f:
	while True:
		data = client.recv(1024)
		if not data:
			if PrintRecvLog == True:
				AllowedRecvData = False
				print('Server cancle send files.')
			break;
		else:
			if PrintRecvLog == True:
				print("Receving files...")
				PrintRecvLog = False
		f.write(data)
f.close()
if AllowedRecvData == True:
	unZip(r'' + os.getcwd() + '\\ReceivedFiles.zip',r''+folder)
	print("Received files succeed.")
if os.path.isfile('ReceivedFiles.zip') == True:
	os.remove("./ReceivedFiles.zip")
client.close()
