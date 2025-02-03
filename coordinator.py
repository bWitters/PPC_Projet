import sysv_ipc
import sys
import time

def coordinator():
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