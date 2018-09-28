# _*_ coding:utf-8 _*_
from __future__ import division
from socket import *
import os
import zipfile
import _thread
import sys
import time

file_size = 0
BarSymbol = '█'
OutputSymbol = '|'
SendDataLen = 0
AloneBarNum = 0
#percent 0 - 100
def set_bar(percent):
	global BarSymbol
	global OutputSymbol
	OutputSymbol = '|'
	if percent <= 100:
		index = percent
		while index > 0:
			index = index - 3
			OutputSymbol = OutputSymbol + BarSymbol
	if percent < 100 and percent >= 0:
		sys.stdout.write(str(percent)+'% '+OutputSymbol+'->'+ "\r")
	elif percent ==100:
		sys.stdout.write(str(percent)+'% '+OutputSymbol+'|'+ "\r")
	else:
		pass
	sys.stdout.flush()

def tcplinkdata(skt,addr):
	global BarSymbol
	global AloneBarNum
	global SendDataLen
	global file_size
	print('Zip files...')
	createZip(r'' + folder + '\\')
	skt.send(bytes(str(file_size),encoding='utf-8'))
	print(addr,"Connected succeed.")
	print('Sending files...')
	with open('./SendFiles.zip', 'rb') as f:
		for data in f:
			SendDataLen = SendDataLen + len(data)
			bar_num = int(float(SendDataLen)/float(file_size) * 100)
			if bar_num > AloneBarNum:
				AloneBarNum = bar_num
				set_bar(bar_num)
			skt.send(data)
	f.close()
	skt.close()
	print("\n")
	print("Send files succeed.\n")
	PrepareFile()
	print("Wait client connect...")
	
def get_host_ip():
	try:
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(('8.8.8.8', 9998))
		ip = s.getsockname()[0]
	finally:
		s.close()
	print('server ip:',ip)
	return ip

def createZip(filePath):
	global file_size
	fileList=[]
	target = 'SendFiles.zip'
	newZip = zipfile.ZipFile(target,'w')
	for dirpath,dirnames,filenames in os.walk(filePath):
		for filename in filenames:
			fileList.append(os.path.join(dirpath,filename))
	for tar in fileList:
		newZip.write(tar,tar[len(filePath):])
	newZip.close()
	file_size = os.path.getsize('./SendFiles.zip')
	#print(file_size)

def PrepareFile():
	if os.path.isfile('SendFiles.zip') == True:
		os.remove("./SendFiles.zip")
	
	if not os.path.exists(folder):
		os.makedirs(folder)
		print('SendFiles folder is empty!')
		exit()
	if not os.listdir(folder):
		print('SendFiles folder is empty!')
		exit()


folder = os.getcwd() + '\SendFiles'

HOST = get_host_ip()
PORT = 39576
ADDR = (HOST,PORT)

server = socket(AF_INET,SOCK_STREAM)
server.bind(ADDR)
server.listen(5)
PrepareFile()
print("Wait client connect...")
while True:
	skt,addr = server.accept()
	#print(addr)
	straddr  = str(addr)
	AllowedSendData = input(straddr + ' request data,Y/N?\n')
	#print(skt)
	if AllowedSendData == 'Y' or AllowedSendData == 'y':
		try:
			_thread.start_new_thread(tcplinkdata,(skt,addr))
		except:
			print("Can't start thread.")
	else:
		skt.close()
		print('Cancle send files.')
		PrepareFile()
		print("Wait client connect...")
server.close()
