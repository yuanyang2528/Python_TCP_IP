# _*_ coding:utf-8 _*_
import os
import zipfile
from socket import *
import _thread

def tcplinkdata(skt,addr):
	#print(skt)
	createZip(r'' + folder + '\\')
	print(addr,"Connected succeed.")
	print('Sending files...')
	with open('./SendFiles.zip', 'rb') as f:
		for data in f:
		#print(data)
			skt.send(data)
	f.close()
	skt.close()
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
    fileList=[]
    target = 'SendFiles.zip'
    newZip = zipfile.ZipFile(target,'w')
    for dirpath,dirnames,filenames in os.walk(filePath):
        for filename in filenames:
            fileList.append(os.path.join(dirpath,filename))
    for tar in fileList:
        newZip.write(tar,tar[len(filePath):])#tar为写入的文件，tar[len(filePath)]为保存的文件名
    newZip.close()

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
