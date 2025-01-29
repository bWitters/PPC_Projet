#!/usr/bin/env python3

from multiprocessing import Process, Lock, Value
import time
import random
import sysv_ipc
import sys
import keyboard

def normal_traffic_gen():
    """
    simulates the generation of normal traffic
    """
    key_N = 30304
    key_S = 50405
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
        dir_chose = car_dir[random.randint(0,len(car_dir))]
        m = ' '.join(format(ord(x), 'b') for x in dir_chose)
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
    

def priority_traffic_gen():
    """
    simulates the generation of high-priority traffic
    """
    key_N = 30304
    key_S = 50405
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
        dir_chose = car_dir[random.randint(0,len(car_dir))]
        m = ' '.join(format(ord(x), 'b') for x in dir_chose)
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

def coordinator_N():
    key_N = 30304
    try:
        mq_N = sysv_ipc.MessageQueue(key_N)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_N, ", terminating.")
        sys.exit(1)
    while running.value:
        while light_N.value:
            if mq_N.current_messages() > 0:
                m = mq_N.receive(type = 2)
                dir = m.decode()
                roads["N"].acquire()
                time.sleep(1)
                while dir in ["NS", "NW"]:
                    m = mq_N.receive(type = 2)
                    dir = m.decode()
                    time.sleep(0.5)
                roads["N"].release()
                roads["W"].acquire()
                time.sleep(1)
                roads["W"].release()

def coordinator_S():
    key_S = 50405
    try:
        mq_S = sysv_ipc.MessageQueue(key_S)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_S, ", terminating.")
        sys.exit(1)
    while running.value:
        while light_S.value:
            if mq_S.current_messages() > 0:
                m = mq_S.receive(type = 2)
                dir = m.decode()
                roads["S"].acquire()
                time.sleep(1)
                while dir in ["SN", "SE"]:
                    m = mq_S.receive(type = 2)
                    dir = m.decode()
                    time.sleep(0.5)
                roads["S"].release()
                roads["E"].acquire()
                time.sleep(1)
                roads["E"].release()

def coordinator_E():
    key_E = 10102
    try:
        mq_E = sysv_ipc.MessageQueue(key_E)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_E, ", terminating.")
        sys.exit(1)
    while running.value:
        while light_E.value:
            if mq_E.current_messages() > 0:
                m = mq_E.receive(type = 2)
                dir = m.decode()
                roads["E"].acquire()
                time.sleep(1)
                while dir in ["EW", "EN"]:
                    m = mq_E.receive(type = 2)
                    dir = m.decode()
                    time.sleep(0.5)
                roads["E"].release()
                roads["S"].acquire()
                time.sleep(1)
                roads["S"].release()

def coordinator_W():
    key_W = 20203
    try:
        mq_W = sysv_ipc.MessageQueue(key_W)
    except sysv_ipc.ExistentialError:
        print("Cannot connect to message queue", key_W, ", terminating.")
        sys.exit(1)
    while running.value:
        while light_W.value:
            if mq_W.current_messages() > 0:
                m = mq_W.receive(type = 2)
                dir = m.decode()
                roads["W"].acquire()
                time.sleep(1)
                while dir in ["WE", "WS"]:
                    m = mq_W.receive(type = 2)
                    dir = m.decode()
                    time.sleep(0.5)
                roads["W"].release()
                roads["N"].acquire()
                time.sleep(1)
                roads["N"].release()

def coordinator(): # Faut faire des subprocess pour chaque route, car Nord et Sud peuvent aller tout droite en meme temps
    """
    allows all vehicles (priority or not) to pass according to traffic regulations and
    the state of traffic lights
    """
    coord_n = Process(target=coordinator_N)
    coord_s = Process(target=coordinator_S)
    coord_e = Process(target=coordinator_E)
    coord_w = Process(target=coordinator_W)
    coord_n.start()
    coord_s.start()
    coord_e.start()
    coord_w.start()

    while running.value:
        pass

    coord_n.join()
    coord_s.join()
    coord_e.join()
    coord_w.join()
    
    return

def lights():
    """
    changes the color of the lights at regular intervals in normal mode, it is notified by
    priority_traffic_gen to set the lights to the appropriate color
    """
    while running.value:
        time.sleep(random.uniform(5,10))
        if light_E.value == 1:
            light_E.value, light_W.value = 0,0
            light_N.value, light_S.value = 1,1
        else :
            light_E.value, light_W.value = 1,1
            light_N.value, light_S.value = 0,0

    return


# def display():
#     """
#     allows the operator to observe the simulation in real-time
#     """
#     while running.value:
#         read_coordinator_data()
#         show_data()


#     return

def stop_running():
    """
    Stop everything if the order is given
    """
    while True:
        if keyboard.is_pressed("j"):
            running.value = 0
            break
    
    # Tant que les autres process sont pas finis on attend
    
    return



if __name__ == "__main__":
    print("Lancement du programme")
    N = 4
    roads = {"N": Lock(), "S": Lock(), "E" : Lock(), "W" : Lock()}
    light_N = Value('d', 0.0)
    light_S = Value('d', 0.0)
    light_E = Value('d', 0.0)
    light_W = Value('d', 0.0)
    running = Value('d', 0.0)
    running.value = 1
    light_N.value, light_S.value = 1,1
    norm_traffic = Process(target=normal_traffic_gen)
    prio_traffic = Process(target=priority_traffic_gen)
    coord = Process(target=coordinator)
    run_proc = Process(target=stop_running)
    
    norm_traffic.start()
    prio_traffic.start()
    coord.start()
    run_proc.start()

    run_proc.join()