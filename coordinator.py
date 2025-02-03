import sysv_ipc
import sys
import time
import numpy as np
from multiprocessing import shared_memory
import os

def coordinator():
    """
    allows all vehicles (priority or not) to pass according to traffic regulations and
    the state of traffic lights
    """
    # Message queues keys
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

    pid_values[2] = os.getpid()

    # Lights values shm
    lights_value = np.array([0,0,0,0])
    l_shape = (len(lights_value),)
    l_type = np.int64
    val_l_shm = shared_memory.SharedMemory(name="lights_info")
    lights_val = np.ndarray(shape=l_shape, dtype=l_type, buffer=val_l_shm.buf)

    # Running value shm 
    running = np.array([1])
    d_shape = (len(running),)
    d_type = np.int64
    val_r_shm = shared_memory.SharedMemory(name="running_info")
    r = np.ndarray(shape=d_shape, dtype=d_type, buffer=val_r_shm.buf)

    # Try Message queue connection
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

    # Main usage
    car_waiting = {"E" : "", "W" : "", "N" : "", "S" : ""}
    while r[0]:
        time.sleep(1)
        m_received = {"E" : 0, "W" : 0, "N" : 0, "S" : 0}

        # Feu E/W
        if lights_val[2] and lights_val[3]:
            # Véhicule prioritaire.
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
            if car_waiting["E"] == "":
                try:
                    m_E, _ = mq_E.receive(type = 2, block = False)
                    m_received["E"] = 1
                    print("Car in queue E")
                except:
                    print("No car in the E queue")
            if car_waiting["W"] == "":
                try:
                    m_W, _ = mq_W.receive(type = 2, block = False)
                    m_received["W"] = 1
                    print("Car in queue W")
                except:
                    print("No car in the W queue")
            
            if car_waiting["E"] == "" and m_received["E"]:
                dir_E = m_E.decode()
                print("message décodé E")
            elif car_waiting["E"] != "":
                dir_E = car_waiting["E"]
            else:
                dir_E = "00"
            if car_waiting["W"] == "" and m_received["W"]:
                dir_W = m_W.decode()
                print("message décodé W")
            elif car_waiting["W"] != "":
                dir_W = car_waiting["W"]
            else:
                dir_W = "00"
            print(dir_E)
            match dir_E[1]:
                case "N" | "W":
                    print("vehicle from E goes to " + dir_E[1])
                case "S":
                    match dir_W[1]:
                        case "S" | "E":
                            print("vehicle from E is waiting to go through")
                            car_waiting["E"] = dir_E
                        case "N" | "0":
                            print("vehicle from E goes to " + dir_E[1])
                            car_waiting["E"] = ""
                case "0":
                    print("No vehicle in E queue")
            match dir_W[1]:
                case "S" | "E":
                    print("vehicle from W goes to " + dir_W[1])
                case "N":
                    match dir_E[1]:
                        case "N" | "W":
                            print("vehicle from W is waiting to go through")
                            car_waiting["W"] = dir_W
                        case "S" | "0":
                            print("vehicle from W goes to " + dir_W[1])
                            car_waiting["W"] = ""
                case "0":
                    print("No vehicle in W queue")

        # Feu N/S
        if lights_val[0] and lights_val[1]:
            # Véhicule prioritaire
            try:
                m_N_prio, _ = mq_N.receive(type = 3, block = False)
            except:
                print("No priority vehicle  in N")
            else:
                direction = m_N_prio.decode()[1]
                print("Prio from N is going to :" + direction)
                continue
            try:
                m_S_prio, _ = mq_S.receive(type = 3, block = False)
            except:
                print("No priority vehicle in S")   
            else:
                direction = m_S_prio.decode()[1]
                print("Prio from S is going to :" + direction)
                continue
            if car_waiting["N"] == "":
                try:
                    m_N, _ = mq_N.receive(type = 2, block = False)
                    m_received["N"] = 1
                except:
                    print("No car in the N queue")
            if car_waiting["S"] == "":
                try:
                    m_S, _ = mq_S.receive(type = 2, block = False)
                    m_received["S"] = 1
                except:
                    print("No car in the S queue")
            
            if car_waiting["N"] ==  "" and m_received["N"]:
                dir_N = m_N.decode()
            elif car_waiting["N"] != "":
                dir_N = car_waiting["N"]
            else:
                dir_N = "00"
            if car_waiting["S"] ==  "" and m_received["S"]:
                dir_S = m_S.decode()
            elif car_waiting["S"] != "":
                dir_S = car_waiting["S"]
            else:
                dir_S = "00"
            print(dir_N)
            print(dir_S)
            match dir_N[1]:
                case "S" | "W":
                    print("vehicle from N goes to " + dir_N[1])
                case "E":
                    match dir_S[1]:
                        case "N" | "E":
                            print("vehicle from N is waiting to go through")
                            car_waiting["N"] = dir_N
                        case "W" | "0":
                            print("vehicle from N goes to " + dir_N[1])
                            car_waiting["N"] = ""
                case "0":
                    print("No vehicle in N queue")
            match dir_S[1]:
                case "N" | "E":
                    print("vehicle from S goes to " + dir_S[1])
                case "W":
                    match dir_N[1]:
                        case "S" | "W":
                            print("vehicle from S is waiting to go through")
                            car_waiting["S"] = dir_S
                        case "E" | "0":
                            print("vehicle from S goes to " + dir_S[1])
                            car_waiting["S"] = ""
                case "0":
                    print("No vehicle in S queue")

    # Fermeture de l'utilisation des shared memories
    val_l_shm.close()
    val_r_shm.close()
    

if __name__ == "__main__":
    coordinator()