# _*_ utf-8 _*_
import os
from socket import *

#Please use server ip address
HOST = "127.0.0.0"

PORT = 39576
ADDR = (HOST,PORT)

client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)
try:
	os.remove("./file.7z")
	print("Delete old file succeed.")
except:
	print("Delete old file succeed.")
finally:
	with open("./file.7z","ab") as f:
		while True:
			data = client.recv(1024)
			if not data:
				break;
			f.write(data)
	f.close()
	print("Received new file succeed.")
	client.close()
