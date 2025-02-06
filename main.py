#!/usr/bin/env python3

from multiprocessing import  shared_memory
from lights import *
from coordinator import *
from priority_traffic_gen import *
from normal_traffic_gen import *
import numpy as np

def stop_running():
    """
    Stop everything if the order is given
    """
    while True:
        key = str(input("Arreter le programme avec j"))
        if key == "j":
            r[0] = 0
            break
    
    # Tant que les autres process sont pas finis on attend
    


if __name__ == "__main__":
    print("Lancement du programme")
    N = 4

    # Lights Values Varaible
    lights_value = np.array([0,0,0,0]) # N,S,E,W
    l_shape = (len(lights_value),)
    l_type = np.int64
    l_size = np.dtype(l_type).itemsize * np.prod(l_shape)
    shm_2 = shared_memory.SharedMemory(create=True, size=l_size, name="lights_info")

    # Running Variable
    running = np.array([1]) 
    d_shape = (len(running),)
    d_type = np.int64
    d_size = np.dtype(d_type).itemsize * np.prod(d_shape)
    shm = shared_memory.SharedMemory(create=True, size=d_size, name="running_info")


    l = np.ndarray(shape=d_shape, dtype=d_type, buffer=shm_2.buf)
    r = np.ndarray(shape=d_shape, dtype=d_type, buffer=shm.buf)
    r[0] = 1

    # Other process PID
    pid_list = np.array([0,0,0,0,0]) # Main, Lights, Coord, Prio, Normal
    pid_shape = (len(pid_list),)
    pid_type = np.int64
    pid_size = np.dtype(pid_type).itemsize * np.prod(pid_shape)
    pid_shm = shared_memory.SharedMemory(create=True, size=pid_size, name="pid_info")
    pid_values = np.ndarray(shape=pid_shape, dtype=pid_type, buffer=pid_shm.buf)
    
    pid_values[0] = os.getpid()

    # Prio light indicator
    prio_lights = np.array([0,0,0,0]) # Main, Lights, Coord, Prio, Normal
    pl_shape = (len(prio_lights),)
    pl_type = np.int64
    pl_size = np.dtype(pl_type).itemsize * np.prod(pl_shape)
    pl_shm = shared_memory.SharedMemory(create=True, size=pl_size, name="prio_lights")
    pl_values = np.ndarray(shape=pl_shape, dtype=pl_type, buffer=pl_shm.buf)

    stop_running()

    # MÃ©chanisme d'attente des autres process avant de fermer la shared memory
    shm.close()
    shm_2.close()
    shm.unlink()  
    shm_2.unlink() 
    pid_shm.close()
    pid_shm.unlink()
    pl_shm.close()
    pl_shm.unlink()

    print("Fin du programme main")