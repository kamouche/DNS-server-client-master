
import sys, threading, os, random
from socket import *
def main():
	host = "localhost" # Hostname.
	port = 5001 # Port number.
#-------------------------------------------------------------------------------------------------
													#Configuration de Socket
	#create a socket object, SOCK_STREAM for TCP:
	mySock=socket(AF_INET,SOCK_STREAM)

	mySock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)# to tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire. Otherwise, the server can't be reopen in a short time after exit.
	#mySock.setsock
	#bind socket to the current address on port 5001:
	mySock.bind((host,port))#bind local IP addresses which is 127.0.0.1 and port which is 5001
	mySock.listen(20)#Listen on the given socket maximum number of connections queued is 20

	while 1:
		#Accepter la conection a un client connecté au port 5001
		connectionSock, addr = mySock.accept()
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
		#open a thread pour accepter thread de plusieur client
		server.start()
#----------------------------------------------------------------------------------------------------
					#Recevoir la requette de la part de client
def dnsQuery(connectionSock, srcAddress):
	print ('Accept new connection from %s...\n' %srcAddress)
	domainName=connectionSock.recv(1024).decode()
	if len(domainName)==0:
		print("Connection Closed.\n")
		connectionSock.close()
		return

	flag=1#  flag est utilisé pour judger whether the local Walid DNS (file) have the address queried. flag==1 means not found
	#ouvrir  local cache file
	try:
		f=open('Walid DNS.txt','r+') #open the local cache file for both reading and writing
	except IOError:
		print('file cache doesn\'t exist, creat a new one\n')
		os.mknod('Walid DNS.txt') #creer file s'il  n exist pas
		f=open('Walid DNS.txt','r+')#ouvrir  local cache file
	# read the Walid DNS file by line and try to find the IP address that client queried
	for line in f.readlines():
		loc=line.find(domainName+":")
		if loc == -1:# if the domain name is not found in that line
			flag=1
		else:
			if loc==0:# if the domain name is found in that line
				flag=0# flag==0 means answer found
				addStr=line[-(len(line)-len(domainName)-1):-1]#addStr is the address in the cache file
				if addStr.find(":")!=-1:# if there are multiple addresses
					alladdr=addStr.split(":")# split the multiple addresses
					addStr=alladdr[0]# choose the first one of the multiple addresses as the answer
				print('IP Found')
				IPanswer="Local DNS:"+domainName+":"+addStr+"\n"# IPanswer is the answer to the client's query
				connectionSock.send(IPanswer.encode())# send the answer
				print('      Address sent.\n')
				connectionSock.close()# close the socket
				f.close()# close the file
				break
	if flag == 1:
		f.close()
		print('No address of this domain name in Walid DNS\n')  # !!!!!!temp delet later
		IPanswer = "Host not found. SVP Ressayer\n"
		connectionSock.send(IPanswer.encode())  # send the answer
		print('      Address sent.\n')
		connectionSock.close()  # close the socket

def monitorQuit(mySock): # pour fermer si tapez exit
	while 1:
		sentence = input()# read the input from
		if sentence == "exit":
			mySock.close()# close the socket opened. if not the port will still be occupied.
			print("Server Shut Down.")
			os.kill(os.getpid(),9)# find the parent's PID and kill the precess tree.
			exit(0);#exit
		else:
			print("Invalid command. Please input \"exit\" to shut down the server.")

main() #la principal fonction pour  l'executer les program
