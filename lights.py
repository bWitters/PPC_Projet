import signal
import time
import random
from multiprocessing import current_process

def prio_light():
    light_swap_acces.acquire()
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