import sys
from socket import *

def main():
	while 1:
		host = "localhost" # Remote hostname. It can be changed to anything you desire.
		port = 5001 # Port number.

		mySock = socket(AF_INET, SOCK_STREAM)
		mySock.connect((host, port))

		st = input("Entrer un nom de dommaine : ")  # Get input from users.

		while 1:

			if st == "":
				continue
			else:
				break
		if st == "exit" or  st == "exit":
			mySock.close()
			sys.exit(1) # If input is "q" or "Q", quit the program.
		mySock.send(st.encode()) # Otherwise, send the input to server.
		#And encode is to canvert unicode ot another format
		data = mySock.recv(1024).decode() # Receive from server.#py3 specific
		print("      Received:", data) # Print out the result.

main()
