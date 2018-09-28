# _*_ utf-8 _*_
from __future__ import division
import os
import zipfile
from socket import *
import sys,time

def unZip(filePath,unzipPath):
    file = zipfile.ZipFile(filePath)
    file.extractall(unzipPath)

j = '|█'
def set_bar(num):
	global j
	if num%3 == 0:
		j += '█'
	if num == 100:
		sys.stdout.write(str(num)+'% '+j+'|'+ "\r")
	else:
		sys.stdout.write(str(num)+'% '+j+'->'+ "\r")
	sys.stdout.flush()

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
RecevDataLen = 0
glnum = 0
num = 0
size_data = client.recv(1024)
strdata = size_data.decode()
file_size = int(strdata)
count = int(file_size/100)
#print(count)
with open("./ReceivedFiles.zip","ab") as f:
	while True:
		data = client.recv(1024)
		if not data:
			if PrintRecvLog == True:
				AllowedRecvData = False
				print('Server cancle send files.')
			break;
		else:
			RecevDataLen = RecevDataLen + len(data)
			#print(RecevDataLen)
			if RecevDataLen > count:
				num = int(RecevDataLen/count)
				if(num > glnum):
					glnum = num
					set_bar(glnum)
			if PrintRecvLog == True:
				print("Receving files...")
				PrintRecvLog = False
		f.write(data)
f.close()
if AllowedRecvData == True:
	unZip(r'' + os.getcwd() + '\\ReceivedFiles.zip',r''+folder)
	print("\n")
	print("Received files succeed.")
if os.path.isfile('ReceivedFiles.zip') == True:
	os.remove("./ReceivedFiles.zip")
client.close()
