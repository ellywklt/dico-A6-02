#!/usr/bin/env python3
import sys
import socket
import ssl


context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH) #mode SSL
context.load_verify_locations("certif/ca.pem")

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creation socket
host=sys.argv[1] 
port=sys.argv[2] 

s_client=context.wrap_socket(s, server_hostname="127.0.0.1")
s_client.connect((host,int(port))) #cast de la variable port car argv est une chaine
while(True):
    request=input("") #fonction pour recuperer la saisie du client
    s_client.sendall(request.encode("utf-8"))
    msg_recu=s_client.recv(5000)
    print(msg_recu.decode("utf-8"))
    if(len(msg_recu)==0):
        break

s_client.close()