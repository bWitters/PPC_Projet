import signal
import time
import random
from multiprocessing import current_process, shared_memory
import numpy as np
import sys
import os
import threading

def prio_light(sig1, sig2):
    # Lights values variable
    lights_value = np.array([0, 0, 0, 0])
    l_shape = (len(lights_value),)
    l_type = np.int64
    val_l_shm = shared_memory.SharedMemory(name="lights_info")
    lights_val = np.ndarray(shape=l_shape, dtype=l_type, buffer=val_l_shm.buf)

    # Prio Light indicator
    prio_lights = np.array([0, 0, 0, 0])  # N,S,E,W
    pl_shape = (len(prio_lights),)
    pl_type = np.int64
    pl_shm = shared_memory.SharedMemory(name="prio_lights")
    pl_values = np.ndarray(shape=pl_shape, dtype=pl_type, buffer=pl_shm.buf)

    for i in range(len(pl_values)):
        if pl_values[i] == 1:
            for j in range(len(lights_val)):
                lights_val[j] = 0
            lights_val[i] = 1
            pl_values[i] = 0

    return

def update_lights(lights_val):
    """
    Update the lights value randomly every 2 seconds.
    """
    while True:
        # Generate random values (0 or 1) for the lights
        new_lights = np.random.randint(2, size=4)
        print(f"Updating lights to: {new_lights}")
        
        # Update the shared memory
        for i in range(4):
            lights_val[i] = new_lights[i]
        
        # Wait for 2 seconds
        time.sleep(4)

def lights():
    """
    Changes the color of the lights at regular intervals in normal mode, it is notified by
    priority_traffic_gen to set the lights to the appropriate color.
    """
    print("Lancement de lights")
    print("Starting Process:", current_process().name)
    signal.signal(signal.SIGUSR1, prio_light)

    # Other Process PID
    pid_list = np.array([0, 0, 0, 0, 0])  # Main, Lights, Coord, Prio, Normal
    pid_shape = (len(pid_list),)
    pid_type = np.int64
    pid_shm = shared_memory.SharedMemory(name="pid_info")
    pid_values = np.ndarray(shape=pid_shape, dtype=pid_type, buffer=pid_shm.buf)

    pid_values[1] = os.getpid()

    # Lights values variable
    lights_value = np.array([0, 0, 0, 0])
    l_shape = (len(lights_value),)
    l_type = np.int64
    val_l_shm = shared_memory.SharedMemory(name="lights_info")
    lights_val = np.ndarray(shape=l_shape, dtype=l_type, buffer=val_l_shm.buf)

    # Program still running variable
    running = np.array([1])
    d_shape = (len(running),)
    d_type = np.int64
    val_r_shm = shared_memory.SharedMemory(name="running_info")
    r = np.ndarray(shape=d_shape, dtype=d_type, buffer=val_r_shm.buf)

    # Start a thread to update the lights every 2 seconds
    lights_thread = threading.Thread(target=update_lights, args=(lights_val,))
    lights_thread.daemon = True  # Daemonize thread to exit when the main program exits
    lights_thread.start()

    while r[0]:
        print(f"Current lights: {lights_val[0]}, {lights_val[1]}, {lights_val[2]}, {lights_val[3]}")
        time.sleep(4)  # Sleep to avoid flooding the console with prints

    # Fermeture de l'utilisation des shared memories
    val_l_shm.close()
    val_r_shm.close()

    print("Fin du programme Lights")

if __name__ == "__main__":
    lights()