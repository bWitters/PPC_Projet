import signal
import time
import random
from multiprocessing import current_process, shared_memory
import numpy as np
import sys

def prio_light():
    return

def lights():
    """
    changes the color of the lights at regular intervals in normal mode, it is notified by
    priority_traffic_gen to set the lights to the appropriate color
    """
    
    print("Lancement de lights")
    print("Starting Process:", current_process().name)
    signal.signal(signal.SIGUSR1, prio_light)
    lights_value = np.array([0,0,0,0])
    l_shape = (len(lights_value),)
    l_type = np.int64
    val_l_shm = shared_memory.SharedMemory(name="lights_info")
    lights_val = np.ndarray(shape=l_shape, dtype=l_type, buffer=val_l_shm.buf)
    running = np.array([1])
    d_shape = (len(running),)
    d_type = np.int64
    val_r_shm = shared_memory.SharedMemory(name="running_info")
    r = np.ndarray(shape=d_shape, dtype=d_type, buffer=val_r_shm.buf)
    while r[0]:
        print(lights_val[0], lights_val[1], lights_val[2], lights_val[3])
        time.sleep(random.uniform(5,10)) # Module signal.alarm(n) ou threading.Timer()
        if lights_val[2] == 1:
            lights_val[2], lights_val[3] = 0,0
            lights_val[0], lights_val[1] = 1,1
        else :
            lights_val[2], lights_val[3] = 1,1
            lights_val[0], lights_val[1] = 0,0

if __name__ == "__main__":
    lights()