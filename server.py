# _*_ coding:utf-8 _*_

from socket import *
import _thread

def tcplink(skt,addr):
  print(skt)
  print(addr,"Connected succeed.")
  print('Start send file...')
  with open('./Project2.exe', 'rb') as f:
    for data in f:
      #print(data)
      skt.send(data)
  f.close()
  skt.close()

def get_host_ip():
	try:
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(('8.8.8.8', 9998))
		ip = s.getsockname()[0]
	finally:
		s.close()
	print(ip)
	return ip

HOST = get_host_ip()
PORT = 39576
ADDR = (HOST,PORT)

server = socket(AF_INET,SOCK_STREAM)
server.bind(ADDR)
server.listen(5)

while True:
  print("Wait connect...")
  skt,addr = server.accept()
  print(skt)
  try:
    _thread.start_new_thread(tcplink,(skt,addr))
  except:
    print("Can't start thread.")
server.close()
