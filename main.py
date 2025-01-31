#!/usr/bin/env python3

from multiprocessing import Process, Lock, Value, current_process
import time
import random
import sysv_ipc
import sys
import keyboard
import signal

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

def going_left():
    #
    return

# def coordinator_N():
#     key_N = 30304
#     try:
#         mq_N = sysv_ipc.MessageQueue(key_N)
#     except sysv_ipc.ExistentialError:
#         print("Cannot connect to message queue", key_N, ", terminating.")
#         sys.exit(1)
#     while running.value:
#         while light_N.value:
#             if mq_N.current_messages > 0:
#                 m, t = mq_N.receive(type = 2)
#                 dir = m.decode()
#                 roads["N"].acquire()
#                 time.sleep(1)
#                 while dir in ["NS", "NW"]:
#                     m, t = mq_N.receive(type = 2)
#                     dir = m.decode()
#                     time.sleep(0.5)
#                 roads["N"].release()
#                 roads["W"].acquire()
#                 time.sleep(1)
#                 roads["W"].release()

# def coordinator_S():
#     key_S = 20934
#     try:
#         mq_S = sysv_ipc.MessageQueue(key_S)
#     except sysv_ipc.ExistentialError:
#         print("Cannot connect to message queue", key_S, ", terminating.")
#         sys.exit(1)
#     while running.value:
#         while light_S.value:
#             if mq_S.current_messages > 0:
#                 m, t = mq_S.receive(type = 2)
#                 dir = m.decode()
#                 roads["S"].acquire()
#                 time.sleep(1)
#                 while dir in ["SN", "SE"]:
#                     m, t = mq_S.receive(type = 2)
#                     dir = m.decode()
#                     time.sleep(0.5)
#                 roads["S"].release()
#                 roads["E"].acquire()
#                 time.sleep(1)
#                 roads["E"].release()

# def coordinator_E():
#     key_E = 10102
#     try:
#         mq_E = sysv_ipc.MessageQueue(key_E)
#     except sysv_ipc.ExistentialError:
#         print("Cannot connect to message queue", key_E, ", terminating.")
#         sys.exit(1)
#     while running.value:
#         while light_E.value:
#             if mq_E.current_messages > 0:
#                 m, t = mq_E.receive(type = 2)
#                 dir = m.decode()
#                 roads["E"].acquire()
#                 time.sleep(1)
#                 while dir in ["EW", "EN"]:
#                     m, t = mq_E.receive(type = 2)
#                     dir = m.decode()
#                     time.sleep(0.5)
#                 roads["E"].release()
#                 roads["S"].acquire()
#                 time.sleep(1)
#                 roads["S"].release()

# def coordinator_W():
#     key_W = 20203
#     try:
#         mq_W = sysv_ipc.MessageQueue(key_W)
#     except sysv_ipc.ExistentialError:
#         print("Cannot connect to message queue", key_W, ", terminating.")
#         sys.exit(1)
#     while running.value:
#         while light_W.value:
#             if mq_W.current_messages > 0:
#                 m, t = mq_W.receive(type = 2)
#                 dir = m.decode()
#                 roads["W"].acquire()
#                 time.sleep(1)
#                 while dir in ["WE", "WS"]:
#                     m, t = mq_W.receive(type = 2)
#                     dir = m.decode()
#                     time.sleep(0.5)
#                 roads["W"].release()
#                 roads["N"].acquire()
#                 time.sleep(1)
#                 roads["N"].release()

def coordinator(): # Faut faire des subprocess pour chaque route, car Nord et Sud peuvent aller tout droite en meme temps
    """
    allows all vehicles (priority or not) to pass according to traffic regulations and
    the state of traffic lights
    """
    key_N = 30304
    key_S = 20934
    key_E = 10102
    key_W = 20203
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
    car_waiting = {"E" : "", "W" : "", "N" : "", "S" : ""}
    while running.value:
        time.sleep(1)
        m_received = {"E" : 0, "W" : 0, "N" : 0, "S" : 0}
        if light_E.value and light_W.value:
            try:
                m_E_prio, t_E_prio = mq_E.receive(type = 3, block = False)
            except:
                print("No priority vehicle  in E")
            else:
                direction = m_E_prio.decode()[1]
                print("Prio from E is going to :" + direction)
                continue
            try:
                m_W_prio, t_W_prio = mq_W.receive(type = 3, block = False)
            except:
                print("No priority vehicle in W")    
            else:
                direction = m_W_prio.decode()[1]
                print("Prio from E is going to :" + direction)
                continue
            if len(car_waiting["E"]) == 0:
                try:
                    m_E, t_E = mq_E.receive(type = 2, block = False)
                    m_received["E"] = 1
                except:
                    print("No car in the E queue")
            if len(car_waiting["W"]) == 0:
                try:
                    m_W, t_W = mq_W.receive(type = 2, block = False)
                    m_received["W"] = 1
                except:
                    print("No car in the W queue")
            
            if car_waiting["E"] != "" and m_received["E"]:
                dir_E = m_E.decode()
            elif car_waiting["E"] != "":
                dir_E = car_waiting["E"][0]
            else:
                dir_E = "00"
            if car_waiting["W"] != "" and m_received["W"]:
                dir_W = m_W.decode()
            elif car_waiting["W"] != "":
                dir_W = car_waiting["W"][0]
            else:
                dir_W = "00"
            match dir_E[1]:
                case "N" | "W":
                    print("vehicle from E goes to" + dir_E[1])
                case "S":
                    match dir_W[1]:
                        case "S" | "E":
                            print("vehicle from E is waiting to go through")
                            car_waiting["E"] = dir_E
                        case "N" | "0":
                            print("vehicle from E goes to" + dir_E[1])
                case "0":
                    print("No vehicle in E queue")
            match dir_W[1]:
                case "S" | "E":
                    print("vehicle from W goes to" + dir_W[1])
                case "N":
                    match dir_E[1]:
                        case "N" | "W":
                            print("vehicle from W is waiting to go through")
                            car_waiting["W"] = dir_W
                        case "S" | "0":
                            print("vehicle from W goes to" + dir_W[1])
                case "0":
                    print("No vehicle in W queue")
        if light_N.value and light_S.value:
            try:
                m_N_prio, t_N_prio = mq_N.receive(type = 3, block = False)
            except:
                print("No priority vehicle  in N")
            else:
                direction = m_N_prio.decode()[1]
                print("Prio from N is going to :" + direction)
                continue
            try:
                m_S_prio, t_S_prio = mq_S.receive(type = 3, block = False)
            except:
                print("No priority vehicle in S")   
            else:
                direction = m_S_prio.decode()[1]
                print("Prio from S is going to :" + direction)
                continue
            if len(car_waiting["N"]) == 0:
                try:
                    m_N, t_N = mq_N.receive(type = 2, block = False)
                    m_received["N"] = 1
                except:
                    print("No car in the N queue")
            if len(car_waiting["S"]) == 0:
                try:
                    m_S, t_S = mq_S.receive(type = 2, block = False)
                    m_received["S"] = 1
                except:
                    print("No car in the S queue")
            
            if car_waiting["N"] !=  "" and m_received["N"]:
                dir_N = m_N.decode()
            elif car_waiting["N"] != "":
                dir_N = car_waiting["N"][0]
            else:
                dir_N = "00"
            if car_waiting["S"] !=  "" and m_received["S"]:
                dir_S = m_S.decode()
            elif car_waiting["S"] != "":
                dir_S = car_waiting["S"][0]
            else:
                dir_S = "00"
            match dir_N[1]:
                case "S" | "W":
                    print("vehicle from N goes to" + dir_N[1])
                case "E":
                    match dir_S[1]:
                        case "N" | "E":
                            print("vehicle from N is waiting to go through")
                            car_waiting["N"] = dir_N
                        case "W" | "0":
                            print("vehicle from N goes to" + dir_N[1])
                case "0":
                    print("No vehicle in N queue")
            match dir_S[1]:
                case "N" | "E":
                    print("vehicle from S goes to" + dir_S[1])
                case "W":
                    match dir_N[1]:
                        case "S" | "W":
                            print("vehicle from S is waiting to go through")
                            car_waiting["S"] = dir_S
                        case "E" | "0":
                            print("vehicle from S goes to" + dir_S[1])
                case "0":
                    print("No vehicle in S queue")
    # coord_n = Process(target=coordinator_N, name="North_coord")
    # coord_s = Process(target=coordinator_S, name="South_coord")
    # coord_e = Process(target=coordinator_E, name="East_coord")
    # coord_w = Process(target=coordinator_W, name="Weast_coord")
    # coord_n.start()
    # coord_s.start()
    # coord_e.start()
    # coord_w.start()

    # while running.value:
    #     pass

    # coord_n.join()
    # coord_s.join()
    # coord_e.join()
    # coord_w.join()
    
    return

def lights():
    """
    changes the color of the lights at regular intervals in normal mode, it is notified by
    priority_traffic_gen to set the lights to the appropriate color
    """
    print("Lancement de lights")
    print("Starting Process:", current_process().name)
    signal.signal(signal.SIGUSR1, prio_light)
    while running.value:
        print(light_E.value, light_W.value, light_N.value, light_S.value)
        time.sleep(random.uniform(5,10)) # Module signal.alarm(n) ou threading.Timer()
        light_swap_acces.acquire()
        if light_E.value == 1:
            light_E.value, light_W.value = 0,0
            light_N.value, light_S.value = 1,1
        else :
            light_E.value, light_W.value = 1,1
            light_N.value, light_S.value = 0,0
        light_swap_acces.release()

    return

def prio_light():
    light_swap_acces.acquire()
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