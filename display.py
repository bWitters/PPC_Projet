import sysv_ipc
import sys
import time
import random
import numpy as np
from multiprocessing import shared_memory
import os
import socket


# Type de message : "L,E,W" Lights, direction 1 et direction 2 Verte
# "V,P,E,W" Véhicule, Prioritaire East West
# "V,N,E,W" Normal
# "V,W,E,W" Waiting

def display():
    HOST = "localhost"
    PORT = 6666
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        m = input("message> ")
        while len(m):
            client_socket.sendall(m.encode())
            data = client_socket.recv(1024)
            print("echo> ", data.decode())
            m = input("message> ")

if __name__ == "__main__":
    display()