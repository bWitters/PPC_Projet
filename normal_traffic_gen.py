import sysv_ipc
import sys
import time
import random
import numpy as np
from multiprocessing import shared_memory
import os

def normal_traffic_gen():
    """
    simulates the generation of normal traffic
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

    pid_values[4] = os.getpid()

    running = np.array([1])
    d_shape = (len(running),)
    d_type = np.int64
    val_r_shm = shared_memory.SharedMemory(name="running_info")
    r = np.ndarray(shape=d_shape, dtype=d_type, buffer=val_r_shm.buf)
    try:
        mq_N = sysv_ipc.MessageQueue(key_N, sysv_ipc.IPC_CREX)
    except sysv_ipc.ExistentialError:
        print("Message queue", key_N, "already exsits, terminating.")
        sys.exit(1)
    try:
        mq_S = sysv_ipc.MessageQueue(key_S, sysv_ipc.IPC_CREX)
    except sysv_ipc.ExistentialError:
        print("Message queue", key_S, "already exsits, terminating.")
        sys.exit(1)
    try:
        mq_E = sysv_ipc.MessageQueue(key_E, sysv_ipc.IPC_CREX)
    except sysv_ipc.ExistentialError:
        print("Message queue", key_E, "already exsits, terminating.")
        sys.exit(1)
    try:
        mq_W = sysv_ipc.MessageQueue(key_W, sysv_ipc.IPC_CREX)
    except sysv_ipc.ExistentialError:
        print("Message queue", key_W, "already exsits, terminating.")
        sys.exit(1) 
    car_dir = ["NS", "NE", "NW", "SN", "SE", "SW", "EW", "EN", "ES", "WN", "WS", "WE"]
    test_traffic = ["NS", "NS","NS","NS","NS","SW","SW", "SW", "SW", "SW","SW", "SW" ,"NS","NS","NS","NS","NS"]
    i = 0
    while r[0] and i< len(test_traffic):
        # time.sleep(random.uniform(0,3))
        # dir_chose = car_dir[random.randint(0,len(car_dir)-1)]
        dir_chose = test_traffic[i]
        m = dir_chose.encode()
        print(dir_chose)
        match dir_chose[0]:
            case "N":
                mq_N.send(m, type=2)
            case "S":
                mq_S.send(m, type=2)
            case "E":
                mq_E.send(m, type=2)
            case "W":
                mq_W.send(m, type=2)
        i += 1
    while r[0]:
        continue
    mq_N.remove()
    mq_S.remove()
    mq_E.remove()
    mq_W.remove()

if __name__ == "__main__":
    normal_traffic_gen()