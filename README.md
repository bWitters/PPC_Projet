# PPC_Projet

## Execution :

Le programme a un ordre particulier de lancement à cause de la création des messages queues, shared memory, sockets, dans l’ordre :
- Main.py, qui écrit dans la shared memory que les programmes doivent boucler
- Lights.py qui écrit l’état des feux.
- Normal_traƯic_gen.py qui crée les messages queues et commence à les remplir
- Coordinator.py qui lit les messages queues et crée le socket
- Display.py qui va se connecter au socket et va faire que coordinator comme à écrire
dans le socket (cependant coordinator fait quand même le traitement des véhicules
même si le display n’est pas actif)
- Prio_traƯic_gen.py si l’on veut ajouter des véhicules prioritaires dans nos queues.