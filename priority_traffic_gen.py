import signal
import sysv_ipc
import sys
import time
import random
import os
import numpy as np
from multiprocessing import shared_memory

def priority_traffic_gen():
    """
    simulates the generation of high-priority traffic
    """
    key_N = 30304
    key_S = 20934
    key_E = 10102
    key_W = 20203

    # Other Process PID
    pid_list = np.array([0,0,0,0,0]) # Main, Lights, Coord, Prio, Normal
    pid_shape = (len(pid_list),)
    pid_type = np.int64
    pid_shm = shared_memory.SharedMemory(name="pid_info")
    pid_values = np.ndarray(shape=pid_shape, dtype=pid_type, buffer=pid_shm.buf)

    # Prio lights indicator
    prio_lights = np.array([0,0,0,0]) # N, S, E, W
    pl_shape = (len(prio_lights),)
    pl_type = np.int64
    pl_shm = shared_memory.SharedMemory(name="prio_lights")
    pl_values = np.ndarray(shape=pl_shape, dtype=pl_type, buffer=pl_shm.buf)

    pid_values[3] = os.getpid()

    running = np.array([1])
    d_shape = (len(running),)
    d_type = np.int64
    val_r_shm = shared_memory.SharedMemory(name="running_info")
    r = np.ndarray(shape=d_shape, dtype=d_type, buffer=val_r_shm.buf)
    try:
        mq_N = sysv_ipc.MessageQueue(key_N)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_N, ", terminating.")
        sys.exit(1)
    try:
        mq_S = sysv_ipc.MessageQueue(key_S)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_S, ", terminating.")
        sys.exit(1)
    try:
        mq_E = sysv_ipc.MessageQueue(key_E)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_E, ", terminating.")
        sys.exit(1)
    try:
        mq_W = sysv_ipc.MessageQueue(key_W)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_W, ", terminating.")
        sys.exit(1)
    car_dir = ["NS", "NE", "NW", "SN", "SE", "SW", "EW", "EN", "ES", "WN", "WS", "WE"]
    test_traffic = ["SW","SW"]
    i = 0
    while r[0] and i<len(test_traffic):
        # time.sleep(random.uniform(0,3))
        # dir_chose = car_dir[random.randint(0,len(car_dir)-1)]
        dir_chose = test_traffic[i]
        m = dir_chose.encode()
        print(dir_chose)
        os.kill(pid_values[1], signal.SIGUSR1)
        match dir_chose[0]:
            case "N":
                mq_N.send(m, type=3)
                pl_values[0] = 1
            case "S":
                mq_S.send(m, type=3)
                pl_values[1] = 1
            case "E":
                mq_E.send(m, type=3)
                pl_values[2] = 1
            case "W":
                mq_W.send(m, type=3)
                pl_values[3] = 1
        i+=1
    while r[0]:
        continue
    return

if __name__ == "__main__":
    priority_traffic_gen()