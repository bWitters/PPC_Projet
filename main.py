from crossroad import *

# Run the test
if __name__ == "__main__":
    # queue = multiprocessing.Queue()

    # # Run the normal_traffic_gen function in a separate process
    # generator_process = multiprocessing.Process(target=normal_traffic_gen, args=(queue,))
    # generator_process.start()

    # # Wait a bit for vehicles to be added to the queue
    # time.sleep(6)  # Wait for all 6 vehicles to be generated

    # # Now check the contents of the queue
    # while not queue.empty():
    #     vehicle = queue.get()
    #     print(f"Vehicle ID: {vehicle.vehicle_id}, Source: {vehicle.source}, Destination: {vehicle.destination}")

    # # Terminate the generator process
    # generator_process.terminate()

     # Create a queue to simulate the communication between processes
    queue = multiprocessing.Queue()
    
    # Create an event for signaling priority vehicle arrival
    event = multiprocessing.Event()

    # Run the lights process in another separate process
    lights_process = multiprocessing.Process(target=lights, args=(event,))
    lights_process.start()

    # Run the priority_traffic_gen function in a separate process
    generator_process = multiprocessing.Process(target=priority_traffic_gen, args=(queue, event))
    generator_process.start()

    

    # Wait for processes to finish 
    generator_process.join()  # Wait for the priority traffic generator to finish
    lights_process.terminate()  # Terminate the lights process after the simulation ends

    # check the contents of the queue
    while not queue.empty():
        vehicle = queue.get()
        print(f"Vehicle ID: {vehicle.vehicle_id}, Source: {vehicle.source}, Destination: {vehicle.destination}, Priority: {vehicle.priority}")
    

    # Terminate the generator process
    