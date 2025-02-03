import sysv_ipc
import sys
import time
import random

def normal_traffic_gen():
    """
    simulates the generation of normal traffic
    """
    key_N = 30304
    key_S = 20934
    key_E = 10102
    key_W = 20203
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
    while running.value:
        time.sleep(random.uniform(0,3))
        dir_chose = car_dir[random.randint(0,len(car_dir)-1)]
        m = ' '.join(format(ord(x), 'b') for x in dir_chose)
        print(m)
        match dir_chose[0]:
            case "N":
                mq_N.send(m, type=2)
            case "S":
                mq_S.send(m, type=2)
            case "E":
                mq_E.send(m, type=2)
            case "W":
                mq_W.send(m, type=2)

    return