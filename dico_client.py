#!/usr/bin/env python3
import sys
import socket


s_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creation socket
host=sys.argv[1] #argument saisi nom du serveur
port=sys.argv[2] #numero de port 

s_client.connect((host,int(port))) #cast de la variable port car argv est une chaine
while(True):
    request=input("") #fonction pour recuperer la saisie du client
    s_client.sendall(request.encode("utf-8"))
    msg_recu=s_client.recv(5000)
    if(len(msg_recu)==0):
        break
    print(msg_recu.decode("utf-8"))
    break
s_client.close()
