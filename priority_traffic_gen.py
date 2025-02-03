import signal
import sysv_ipc
import sys
import time
import random

def priority_traffic_gen():
    """
    simulates the generation of high-priority traffic
    """
    key_N = 30304
    key_S = 20934
    key_E = 10102
    key_W = 20203
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
    while running.value:
        time.sleep(random.uniform(0,3))
        dir_chose = car_dir[random.randint(0,len(car_dir)-1)]
        m = ' '.join(format(ord(x), 'b') for x in dir_chose)
        print(m)
        signal.raise_signal(signal.SIGUSR1) # os.kill()
        match dir_chose[0]:
            case "N":
                mq_N.send(m, type=3)
            case "S":
                mq_S.send(m, type=3)
            case "E":
                mq_E.send(m, type=3)
            case "W":
                mq_W.send(m, type=3)
    return