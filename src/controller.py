# Fan SHIM Controller Script written in Python
# For the Raspberry Pi
# Written by BaconErie, released into the public domain
# https://baconerie.github.io

##########################
### CONSTANTS/SETTINGS ###
##########################

FAN_ON_TEMPERATURE = 52 # CPU Temperature (in celsius) at which the fan should turn on

FAN_OFF_TEMPERATURE = 47 # CPU Temperature (in celsius) at which the fan should cool to after it is 
# turned on. This must be lower than FAN_ON_TEMPERATURE

######################
### VARIABLE SETUP ###
######################
from fanshim import FanShim
from gpiozero import CPUTemperature
from time import sleep

cpu = CPUTemperature()
fan = FanShim()

########################
### HELPER FUNCTIONS ###
########################

def get_fan_status():
    '''Returns a string with a user friendly value of OFF or ON instead of 0 or 1'''
    if fan.get_fan() == 1:
        return 'ON'
    elif fan.get_fan() == 0:
        return 'OFF'
    else:
        return 'FAN STATUS BROKEN'

######################
### STARTUP CHECKS ###
######################

# Is FAN_OFF_TEMPERATURE less than FAN_ON_TEMPERATURE? If not, end script.
if not FAN_OFF_TEMPERATURE < FAN_ON_TEMPERATURE:
    print('FAN_OFF_TEMPERATURE is NOT less than FAN_ON_TEMPERATURE! Please check your settings and try again.')
    print(f'Stopping script, fan status is {get_fan_status()}')
    
    quit()

#################
### MAIN LOOP ###
#################

while True:
    # Get the CPU Temperature
    cpu_temp = cpu.temperature

    # Check if the fan is on
    if fan.get_fan() == 1:
        # If the fan is on, check the CPU temperature
        if cpu_temp <= FAN_OFF_TEMPERATURE:
            # If the CPU temperature is less than or equal to FAN_OFF_TEMPERATURE, turn off the fan and set light to green
            fan.set_fan(False)
            fan.set_light(0, 100, 0)
    
    elif fan.get_fan() == 0:
        # If the fan is off, check the CPU temperature
        if cpu_temp >= FAN_ON_TEMPERATURE:
            # If the CPU temperature is greater than or equal to FAN_ON_TEMPERATURE, turn ON the fan and set light to white    
            fan.set_fan(True)
            fan.set_light(100, 100, 100)

    # Wait 60 seconds, then loop again
    sleep(60)