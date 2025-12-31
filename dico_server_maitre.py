#!/usr/bin/env python3
import socket
import select
import protocol_dico
import ssl

def launch_dico_maitre(port):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH) # mis en place du context ssl
    context.load_cert_chain('certif/server.pem', 'certif/server.key') # le serveur charge les fichier correspondants
    s_serveur=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #on crée la socket serveur
    s_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permet de réutiliser l'adresse immédiatement
    s_serveur.bind(("127.0.0.1", int(port))) #on affecte notre socket au port 8888 et l'adresse 127.0.0.1
    s_serveur.listen(1) # notre socket serveur ecoute
    print(f"admin marche sur '127.0.0.1' {port}")
    aide="'Usage dico_client.py: [dico_file] [command]'\n"+"'[get] [key] : Récupère la valeur associée à la clé. Affiche 'clé non trouvée' si la clé n'existe pas.'\n"+"'[pref] [prefixe]: Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.'\n"
    aide= aide+"'[set] [key} [value] : Définit la valeur associée à la clé.'\n"+"'[del] [key] : Supprime la clé du dictionnaire. Affiche 'clé non trouvée' si la clé n'existe pas.'\n"

    l=[]#liste des socket client
    while(True):
        s_ready,_,_=select.select([s_serveur]+l,[],[])
        for sock in s_ready:
            if sock==s_serveur: #si sock est la socket serveur c'est que c'est une nouvelle connexion donc on cree une nouvelle socket client et on l'ajoute a la liste
                new_sock, adresse=s_serveur.accept()
                try:
                    new_sock_client=context.wrap_socket(new_sock, server_side=True) # connexion en mode SSL 
                    l.append(new_sock_client)
                    print("Nouveau client connecte", new_sock_client)
                except ssl.SSLError:
                    print("Erreur SSL")
                    new_sock.close()
            else:
                request_client=sock.recv(5000).decode("utf-8").strip()#on enleve les espaces de fin de chaine
                if(len(request_client)==0): #avec ca si client fait CTRL C ca crash pas le serveur
                    sock.close()
                    l.remove(sock)
                    break
                else:
                    args=request_client.split("]") # on traite le message reçu pour séparer les différentes parties
                    print(f"les arg sont {args}")
                    if(args[0].strip("[")=="help"):# cas particulier de la commande help
                        sock.sendall(aide.encode("utf-8"))
                    elif(args[0].strip("[")=="goodbye"):# si l'admin veut se deconnecter
                        sock.close()
                        l.remove(sock)
                        break
                    if(len(args)<2):# securiter si un client saisit seulement 1 une lettre car on après on va essayer d'accéder à args[1]
                        sock.sendall(f"invalid command\n{aide} \n".encode("utf-8"))
                        break
                    else:
                        save=args[0].strip("[")
                        dico=args[0].strip("[")
                        dico=dico.split(".")
                        print(f"apres le . {dico}")
                        dico_without_ext=dico[0] # comme nous avons 2 fichier le serveur admin interroge l'original 
                        command=args[1].strip(" [")
                        if(command=="GET" or command=="get"):
                            cle=args[2].strip(" [")
                            print(dico[0]+"_original.json")
                            cle=protocol_dico.get("data/"+dico_without_ext+"_original.json",cle)  #on ajoute _original.json pour interroger le bon dictionnaire.
                            sock.sendall(f"serveur admin: {cle}\n".encode("utf-8"))#peut pas obliger de preciser que c'est le serveur admin qui a répondu ?
                        elif(command=="pref" or command=="PREF"):
                            prefixe=args[2].strip(" [")
                            result=protocol_dico.pref ("data/"+dico_without_ext+"_original.json",prefixe)
                            sock.sendall(f"serveur admin: {result}\n".encode("utf-8"))
                        elif(command == 'set'or command=="SET"):
                            cle = args[2].strip(" [")
                            valeur = args[3].strip(" [")
                            result=protocol_dico.set("data/"+dico_without_ext+"_original.json",cle,valeur)
                            protocol_dico.copie_dico("data/"+dico_without_ext+"_original.json","data/"+save) # on est réalise la mis à jour du fichier copie que consulte le serveur esclave
                            sock.sendall(f"serveur admin: {result}\n".encode("utf-8"))
                        elif(command=='del' or command=='DEL'):
                            cle = args[2].strip(" [")
                            result=protocol_dico.delete("data/"+dico_without_ext+"_original.json",cle)
                            protocol_dico.copie_dico("data/"+dico_without_ext+"_original.json","data/"+save)
                            sock.sendall(f"serveur admin: {result}\n".encode("utf-8"))
                        else:
                            sock.sendall(f"invalid command\n{aide}\n".encode("utf-8"))