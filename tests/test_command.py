import socket
import time


#on lance le serveur dans un autre terminal
host = "127.0.0.1"
port = 7777

def test_command(command):
    print(f"Test envoi : '{command}' ... ", end="")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        sock.sendall((command + "\n").encode('utf-8'))

        reponse = sock.recv(1024).decode('utf-8').strip()
        print(f"Succes : {reponse}")
        
        sock.close()
    except Exception:
        print("Echec: Le serveur n'est pas lancé ! Lancez-le dans un autre terminal.")


test_command("[mois_duree.json] [get] [janvier]")
test_command("[mois_duree.json] [get] [février]")
test_command("[mois_duree.json] [GET] [inconnu]")
