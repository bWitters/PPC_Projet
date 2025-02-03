#!/usr/bin/env python3

from multiprocessing import Process, Lock, Value, current_process
import time
import random
import sysv_ipc
import sys
import keyboard
import signal

def stop_running():
    """
    Stop everything if the order is given
    """
    while True:
        if keyboard.is_pressed("j"):
            running.value = 0
            break
    
    # Tant que les autres process sont pas finis on attend
    


if __name__ == "__main__":
    print("Lancement du programme")
    N = 4
    roads = {"N": Lock(), "S": Lock(), "E" : Lock(), "W" : Lock()}
    light_swap_acces = Lock()
    light_N = Value('d', 0.0) #remote manager ou shared memory
    light_S = Value('d', 0.0)
    light_E = Value('d', 0.0)
    light_W = Value('d', 0.0)
    running = Value('d', 0.0)
    running.value = 1
    light_N.value, light_S.value = 1,1
    norm_traffic = Process(target=normal_traffic_gen, name="Normal_Traffic_gen")
    prio_traffic = Process(target=priority_traffic_gen, name= "Prio_Traffic_gen")
    light_swapper = Process(target=lights, name="Light_swapper")
    coord = Process(target=coordinator, name="Main_coordinator")
    run_proc = Process(target=stop_running, name="End_Process")
    
    norm_traffic.start()
    prio_traffic.start()
    light_swapper.start()
    coord.start()
    run_proc.start()

    run_proc.join()
