#############
# Test DATA #
#############

# North_South car gen test
# -> No buffer full
# -> Car created correctly as {"Car_type" : "Classic", "Road" : "N_S"}

# East_Weast car gen test
# -> No buffer full
# -> Car created correctly as {"Car_type" : "Classic", "Road" : "E_W"}

# Coordinator test

Message_queue_N_S = [{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"}]
Message_queue_E_W = [{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"}]
Message_queue_only_prio = [{"Car_type" : "Priority", "Road" : "N_S"},{"Car_type" : "Priority", "Road" : "E_W"},{"Car_type" : "Priority", "Road" : "N_S"},{"Car_type" : "Priority", "Road" : "N_S"},{"Car_type" : "Priority", "Road" : "N_S"},{"Car_type" : "Priority", "Road" : "E_W"},{"Car_type" : "Priority", "Road" : "E_W"},{"Car_type" : "Priority", "Road" : "E_W"},{"Car_type" : "Priority", "Road" : "E_W"}]
Message_queue_mixed = [{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Classic", "Road" :"N_S"},{"Car_type" : "Priority", "Road" : "E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"},{"Car_type" : "Classic", "Road" :"E_W"}]

# Lights test
# Not too much light swap
# We will probably need something with 4 reds to allow car in the middle to go through

# Stop running test
# Clean process exit

# Display test
# Cool display
