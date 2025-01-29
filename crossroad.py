#!/usr/bin/env python3

import multiprocessing
import time
import random

import random
import time
import multiprocessing

class Vehicle:
    def __init__(self, vehicle_id, source, destination, priority=False):
        self.vehicle_id = vehicle_id
        self.source = source
        self.destination = destination
        self.priority = priority

def normal_traffic_gen(queue):
    """
    Simulates the generation of normal traffic.
    """
    vehicle_id = 0
    while vehicle_id < 6:  # Limit to 6 vehicles for testing
        vehicle_id += 1
        print(f"Vehicle {vehicle_id} is waiting to cross the intersection")

        # Randomly choose the source
        source = random.choice(["North", "South", "East", "West"])

        # Determine destination based on source
        if source == "North":
            destination = "South"
        elif source == "South":
            destination = "North"
        elif source == "East":
            destination = "West"
        else:
            destination = "East"

        print(f"Vehicle {vehicle_id} is moving from {source} to {destination}")

        # Create the vehicle object and put it in the queue
        vehicle = Vehicle(vehicle_id, source, destination)
        queue.put(vehicle)

        # Simulate a random delay before generating the next vehicle
        time.sleep(random.uniform(0, 3))


def priority_traffic_gen(queue, priority_event):
    vehicle_id = 0
    while vehicle_id < 6:  # Limit to 6 vehicles for testing
        vehicle_id += 1
        print(f"Vehicle {vehicle_id} is waiting to cross the intersection")

        # Randomly choose the source
        source = random.choice(["North", "South", "East", "West"])

        # Determine destination based on source
        if source == "North":
            destination = "South"
        elif source == "South":
            destination = "North"
        elif source == "East":
            destination = "West"
        else:
            destination = "East"

        print(f"Vehicle {vehicle_id} is moving from {source} to {destination}")

        # Create the vehicle object and put it in the queue
        priority = random.random() < 0.1 # less than 30% chance of being a priority vehicle
        vehicle = Vehicle(vehicle_id, source, destination, priority=priority)
        
        # Notify the coordinator that a priority vehicle has arrived
        if vehicle.priority:
            print(f"Priority Vehicle {vehicle_id} detected from {vehicle.source}. Signaling the lights.")
            priority_event.set()

        queue.put(vehicle)

        # Simulate a random delay before generating the next vehicle
        time.sleep(random.uniform(0, 3))

        
    return

# def coordinator():
#     """
#     allows all vehicles (priority or not) to pass according to traffic regulations and
#     the state of traffic lights
#     """
#     while running():
#         if North_south == Green:
#             if car in message_queue["North_South"]:
#                 let_car_N_S_go()
#         else:
#             if car in message_queue["East_Weast"]:
#                 let_car_E_W_go()
#     return

def lights(priority_event):
    """"
    changes the color of the lights at regular intervals in normal mode, it is notified by
    priority_traffic_gen to set the lights to the appropriate color
    """
    green_light = "North-South"
    print(f"Initial signal state: Lights in {green_light} direction are green and in East-West direction are red")
    while True:
        if priority_event.is_set():
            print("Priority vehicle detected! Setting lights to green")
            priority_event.clear()

            priority_direction = random.choice(["North-South", "East-West"])
            
            if priority_direction == "North-South":
                green_light = "North-South"
                print(f"Priority light: {green_light} direction is green and East-West direction is red")
            elif priority_direction == "East-West":
                green_light = "East-West"
                print(f"Priority light: {green_light} direction is green and North-South direction is red")
        
            time.sleep(5)  # time for priority vehicle to pass

                
        else:
            if green_light == "North-South":
                green_light = "East-West"
                print(f"Normal light: {green_light} direction is green and North-South direction is red")
            else:
                green_light = "North-South"
                print(f"Normal light: {green_light} direction is green and East-West direction is red")
            
            time.sleep(10)

# def display():
#     """
#     allows the operator to observe the simulation in real-time
#     """
#     while running():
#         read_coordinator_data()
#         show_data()


#     return

# def stop_running():
#     """
#     Stop everything if the order is given
#     """

#     if key_pressed():
#         for procces in process_running:
#             send_signal_terminate(process)
    
#     return