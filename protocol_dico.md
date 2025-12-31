# definition du protocole applicatif

L'objectif de ce protocole est qu'un client puisse communiquer avec le serveur1 pour consulter à distance un dictionnaire sauvegardé dans un fichier json qui est la copie d'un fichier géré par le serveur maître.
Le serveur recupère le dictionnaire depuis le fichier .json à chauque requête du client. Le fichier .json est mis à jour à chaque nouvelle requête qui le nécessite.
Si un client se connecte en administrateur, il communique avec le serveur maître et peut modifier le dictionnaire.
Ces accès s'effectuent par le terminal en saisissant des commandes textuelles qui seront interprétées par les serveurs.


# Type de communication possible 

-Les clients communiquent avec le serveur1 qui lit une copie du fichier json contenant le dictionnaire.
-Si le client est un administrateur,celui-ci communique avec le serveur maître, car celui-ci accepte les requêtes de modifications du fichier json contenant le dictionnaire.
-Le serveur1 consulte une copie [mois_duree.json] du dictionnaire en lecture seule, alors que le serveur maître accède au fichier original [mois_duree_original.json]
-si le serveur1 ne trouve pas une clé du dictionnaire il doit interroger le serveur maitre et retourner la réponse de celui-ci


# Initialisation d'une connexion

Le serveur1 écoute une adresse [127.0.0.1], port [7777] TCP, par lequel il accepte les connexions entrantes.
Le serveurmaitre écoute une adresse [127.0.0.1], port [8888] TCP, par lequel il accepte les connexions entrantes.
Chaque nouvelle connexion entraîne la création d'un socket_client pour communiquer avec le client et traiter les différentes requêtes d'action sur le dictionnaire.
Ces socket_client sont conservés dans un dictionnaire et mis à jour en fonction des ouvertures et fermetures des connexions. 


# Commande pour se connecter en mode client et réaliser une action
Le client doit saisir la commande suivante:
[dico_client.py] [127.0.0.1] [7777] [command]

# Commande pour se connecter en mode administrateur
Le client  doit saisir la commande suivante pour se connecter:
[dico_admin.py] [127.0.0.1] [8888]

# Commande pour initialiser les serveurs avec le port à écouter ainsi que le fichier JSON d'où il faut récupérer le dictionnaire
Pour lancer le serveur1, il faut entrer la commande suivante:
[dico_server.py] [7777]

Si serveur maître:
[dico_server.py] [7777] [master] [127.0.0.1] [8888]


# Commande client utilisable une fois connecté
Le client standard ne peut réaliser que 3 actions:

Consulter une valeur associé à une clé:
[dico_file.json] [get] [key] 

Consulter les couples clé-valeur dont la clé commence par le préfixe donné.
[dico_file.json] [pref] [préfixe] 

Afficher les commandes que le client peut saisir.
[help] 

# Commande administrateur
En mode administrateur, on ajoute à la liste des commandes client les 3 commandes suivantes :

[dico_file.json] [set] [key] [value] modifie la valeur d'une clé existante 
[set] [février] [32]   assigne la valeur 32 au mois de février

[dico_file.json] [del] [key] supprime un couple clé/valeur
[del] [février] supprime le mois de février du dictionnaire

[dico_file.json] [add] [key] [value] ajoute une nouveau couple clé/valeur
[add] [champetre] [14] ajoute le mois champetre avec comme valeur 14

[goodbye] pour se deconnecter du serveur

# exemples requête du client:
1.[dico_file.json] [get] [avril] "demande la valeur (le nombre de jour) associée à une clé (ici le mois d'avril)"
2.[dico_file.json] [get] [juillet] "demande la valeur (le nombre de jour) associée à une clé (ici le mois de juillet)"
3.[dico_file.json] [pref] [jui] "demande les clés donc qui commence par le préfixe "jui" "

    réponse du serveur: 
        Succès : 30 
        Succès : 31 
        Succès : juin  juillet

# exemples de requête érronée:
1.[dico_file.json] [set] [avril] action set non autorisée
2.[dico_file.json] [set] [avril] [31] action set non autorisée
3.[dico_file.json] [get] [avrille] erreur d'orthographe
4.[olae] [poina] commande inexistante

    réponse du serveur:
        1.Echec: commande invalide (client non administrateur)
        2.Echec: permission refusée (client non administrateur)
        3.Echec: clé non trouvée
        4.Echec: commande invalide (client non administrateur)

# Afichage de l'aide dans le terminal
Commandes: [help] 
- '[get] [key]' pour récupéer la valeur associée à la clé. Affiche 'Echec: clé non trouvée' si la clé n'existe pas.
- '[pref] [prefix]' pour afficher tous les couples clé-valeur dont la clé commence par le préfixe donné.
- '[help]' pour afficher l'aide.
- '[goodbye]' pour que le client se déconnecte du serveur.
Admin:
- 'set [key] [value]' pour modifier une paire (clé, valeur).
- 'del [key]' pour supprimer la clé du dictionnaire. Affiche 'Key not found' si la clé n'existe pas.

