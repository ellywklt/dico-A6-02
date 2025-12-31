#!/usr/bin/env python3
from typing import Dict

import os
import json
import socket
import ssl

def load_dico(dico_file: str) -> Dict[str, str]:
    """Load JSON dictionary from file, return empty dict on missing/invalid file."""
    if not os.path.exists(dico_file):
        return {}
    with open(dico_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Ensure the loaded object is a dict; otherwise return empty dict
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            return {}


def save_dico(dico_file: str, dico: Dict[str, str]) -> None:
    with open(dico_file, 'w', encoding='utf-8') as f:
        json.dump(dico, f, ensure_ascii=False, indent=2)


def copie_dico(dico_source,dico_dest):
    dico = load_dico(dico_source)     # lit le dictionnaire depuis le fichier source
    save_dico(dico_dest, dico)

def intero_maitre(request): # cette fonction sert de client pour interroger le serveur maitre
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("certif/ca.pem")
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creation socket
    s_client=context.wrap_socket(s, server_hostname="127.0.0.1")
    s_client.connect(("127.0.0.1",8888)) #cast de la variable port car argv est une chaine
    s_client.sendall(request.encode("utf-8")) #on adresse la requete qui avait été formulé par le client 
    msg_recu=s_client.recv(5000)
    msg_recu=msg_recu.decode("utf-8").strip()
    s_client.close()
    return msg_recu


def get(dico_file,key):
    dico: Dict[str, str] = load_dico(dico_file)
    if key in dico:
        return dico[key]
    else:
        return("clé non trouvée")

def pref (dico_file,prefixe):
    dico: Dict[str, str] = load_dico(dico_file)
    found= False
    l_pref=""
    for key in dico:
        if key.startswith(prefixe):
            l_pref=l_pref+key+" "+dico[key]+" "
            found = True
    if not found:
        l_pref="aucune clé de trouvée avec ce préfixe"

    return l_pref

def set(dico_file,cle,valeur):
    dico: Dict[str, str] = load_dico(dico_file)
    dico[cle] = valeur
    save_dico(dico_file, dico)
    return (f"Set {cle} = {valeur}")

def delete(dico_file,cle):
    dico: Dict[str, str] = load_dico(dico_file)
    if cle in dico:
        del dico[cle]
        save_dico(dico_file, dico)
        return (f"{cle} supprimée")
    else:
        return ("clé non trouvée")
