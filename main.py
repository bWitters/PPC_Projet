#!/usr/bin/env python3

from multiprocessing import Process, shared_memory
import keyboard
from lights import *
from coordinator import *
from priority_traffic_gen import *
from normal_traffic_gen import *
import sys
import numpy as np

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
    lights_value = np.array([0,0,0,0]) # N,S,E,W
    l_shape = (len(lights_value),)
    l_type = np.int64
    l_size = np.dtype(l_type).itemsize * np.prod(l_shape)
    running = np.array([1]) 
    d_shape = (len(running),)
    d_type = np.int64
    d_size = np.dtype(d_type).itemsize * np.prod(d_shape)
    shm = shared_memory.SharedMemory(create=True, size=d_size, name="running_info")
    shm_2 = shared_memory.SharedMemory(create=True, size=l_size, name="lights_info")
    l = np.ndarray(shape=d_shape, dtype=d_type, buffer=shm_2.buf)
    r = np.ndarray(shape=d_shape, dtype=d_type, buffer=shm.buf)
    r[0] = 1
    light_N, light_S = 1,1
    # norm_traffic = Process(target=normal_traffic_gen, name="Normal_Traffic_gen")
    # prio_traffic = Process(target=priority_traffic_gen, name= "Prio_Traffic_gen")
    # light_swapper = Process(target=lights, name="Light_swapper")
    # coord = Process(target=coordinator, name="Main_coordinator")
    # run_proc = Process(target=stop_running, name="End_Process")
    
    # norm_traffic.start()
    # prio_traffic.start()
    # light_swapper.start()
    # coord.start()
    # run_proc.start()

    # run_proc.join()
    while True:
        continue
