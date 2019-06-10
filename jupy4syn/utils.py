import ipywidgets as widgets
from IPython.display import display
import time
from pathlib import Path
from py4syn.epics.MotorClass import Motor
import py4syn
from .Configuration import Configuration


# Logging function that write log information in a file and also in the notebook output cells (if this config is set True)
def logprint(string, mode="[INFO]", config=Configuration()):
    # Log information has a time stamp using GMT-0 time to avoid local computer time problems
    ts = time.gmtime()
    
    # Logs will be stored in a .log directory that will be created if it doesn't exist
    year_month_day = time.strftime("%Y-%m-%d", ts)
    file_name = Path('.logs/' + year_month_day + '-log.txt')

    if not file_name.parent.is_dir():
        file_name.parent.mkdir()
    
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    
    # Write log in the file
    with open(str(file_name), "a") as f:
        f.write(time_stamp + ' | ' + mode + ' ' + string + '\n')
    
    # Write log in stdout
    if config.config['log_cell'].value:
        print(time_stamp + ' | ' + mode + ' ' + string)


# Util function to create a motor with logging informations
def configurate_motor(motor_pv_name='', motor_name='', config=Configuration()):
    motor = None
    
    try:
        motor = Motor(motor_pv_name, motor_name)
        logprint("Motor: \'" + motor_pv_name + "\' succesfully created as \'" + motor_name + "\'", config=config)
    except Exception as e:
        logprint("Error trying to create Motor: \'" + motor_pv_name + "\' as \'" + motor_name + "\'", "[ERROR]", config=config)
        logprint(str(e), "[ERROR]", config=config)
        
    return motor
