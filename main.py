#!/usr/bin/env python3

def normal_traffic_gen():
    """
    simulates the generation of normal traffic
    """
    while running():
        wait()
        send_message_add_car()

    return
    

def priority_traffic_gen():
    """
    simulates the generation of high-priority traffic
    """
    while running():
        wait()
        send_message_add_priority_car()
    return

def coordinator():
    """
    allows all vehicles (priority or not) to pass according to traffic regulations and
    the state of traffic lights
    """
    while running():
        if North_south == Green:
            if car in message_queue["North_South"]:
                let_car_N_S_go()
        else:
            if car in message_queue["East_Weast"]:
                let_car_E_W_go()
    return

def lights():
    """
    changes the color of the lights at regular intervals in normal mode, it is notified by
    priority_traffic_gen to set the lights to the appropriate color
    """
    while running():
        wait()
        change_lights()

    return


def display():
    """
    allows the operator to observe the simulation in real-time
    """
    while running():
        read_coordinator_data()
        show_data()


    return

def stop_running():
    """
    Stop everything if the order is given
    """

    if key_pressed():
        for procces in process_running:
            send_signal_terminate(process)
    
    return

if __name__ == "main":
    print("Lancement du programme")