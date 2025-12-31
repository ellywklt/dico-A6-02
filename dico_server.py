#!/usr/bin/env python3
import socket
import sys
import select
import protocol_dico
import dico_server_maitre #serveur maitre dans un autre fichier.


if(len(sys.argv)>2): #pour lancer serveur maitre on ouvre un terminal on tape ./dico_server.py 7777 master host1(ou 127.0.0.1) 8888
    if(sys.argv[2]=="master"):
        dico_server_maitre.launch_dico_maitre(sys.argv[4])

#dans un autre terminal on lance serveur1 ./dico_server.py 7777
s_serveur=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #on crée la socket serveur
host="127.0.0.1"
port=sys.argv[1]
s_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permet de réutiliser l'adresse immédiatement
s_serveur.bind((host, int(port))) #on affecte notre socket au port 7777 et l'adresse 127.0.0.1
s_serveur.listen(1)
print(f"esclave fonctionne sur {port}")
aide="'Usage dico_client.py: [dico_file] [command]'\n"+"'[get] [key] : Récupère la valeur associée à la clé. Affiche 'Key not found' si la clé n'existe pas.'\n"+"'[pref] [prefixe]: Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.'\n" #aide pour les commandes sur serveur esclave

l=[]#liste des socket client
while(True):
    s_ready,_,_=select.select([s_serveur]+l,[],[])
    for sock in s_ready:
        if sock==s_serveur: #si sock est la socket serveur c'est que c'est une nouvelle connexion donc on cree une nouvelle socket client et on l'ajoute a la liste
            new_sock_client, adresse=s_serveur.accept()
            l.append(new_sock_client)
            print("Nouveau client connecte", new_sock_client)
        else:
            request_client=sock.recv(1500).decode("utf-8").strip()#on enleve les espaces de fin de chaine # on traitre le message reçu pour séparer les différentes parties
            print(request_client)
            if(len(request_client)==0): #avec ca si client fait CTRL C ca crash pas le serveur
                sock.close()
                l.remove(sock)
                break
            args=request_client.split("]")
            if(args[0].strip("[")=="help"):# cas particulier de la commande help
                sock.sendall(aide.encode("utf-8"))
            if(len(args)<2):# securiter si un client saisit seulement 1 une lettre car on après on va essayer d'accéder à args[1]
                sock.sendall(f"invalid command\n{aide}\n".encode("utf-8"))
                sock.close()
                l.remove(sock)
                break
            dico=args[0].strip("[")
            dico_path="data/"+dico #chemin vers le dossier data 
            command=args[1].strip(" [")
            if(command=="GET" or command=="get"):
                cle=args[2].strip(" [") #attention à enlever l'espace
                cle=protocol_dico.get(dico_path,cle)# on utilise la fonction get qui est dans le fichier protocol_dico
                if(cle=="clé non trouvée"): #si la cle n'est pas trouvé on va interroger le serveur maitre
                    resp_maitre=protocol_dico.intero_maitre(request_client) #fonction intero maitre defini dans protocol_dico.py pour jouer le role de client
                    sock.sendall(f"{resp_maitre}\n".encode("utf-8"))
                else:
                    sock.sendall(f"{cle}\n".encode("utf-8"))#on afficher la clé trouvé
            elif(command=="pref" or command=="PREF"):
                prefixe=args[2].strip(" [")
                result=protocol_dico.pref (dico_path,prefixe)
                if(result=="aucune clé de trouvée avec ce préfixe"): #si la cle n'est pas trouvé on va interroger le serveur maitre
                    resp_maitre=protocol_dico.intero_maitre(request_client) 
                    sock.sendall(f"{resp_maitre}\n".encode("utf-8"))
                else:
                    sock.sendall(f"{result}\n".encode("utf-8"))
            else:
                sock.sendall(f"invalid command\n{aide}\n".encode("utf-8"))
