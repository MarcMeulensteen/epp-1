#!/usr/bin/env python
#
# Description:
#   This script is written to controll the A.R.T. EPP-1 E(E)PROM programmer.
#   The used device was running firmware version RTepp, ver 870808.
#
# Before using this script allow non-root access to /ttyUSB0:
#   sudo usermod -a -G dialout $USER
#   Reboot the system
# Check connection:
#   cu -l /dev/ttyUSB0 -s 1200
#
# Install pySerial library:
#   sudo apt-get install python-pip
#   sudo pip install pyserial

import serial

ser = serial.Serial("/dev/ttyUSB0", baudrate=1200, timeout=1)
ser.timeout=1
ser.bytesize=8
ser.parity='N'
ser.stopbits=1
#print("connected to: " + ser.portstr)

class EppException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def command(command):
    #print("Command: " + command)
    ser.write(command + "\r")
    first=True
    appender=""
    while True:
        line = ser.readline()
        #print '> ' + line,
        # Skip first line containing command itself
        if first:
            first=False
            continue
        # Raise error when line contains error
        if "Error\r\n" == line:
            raise EppException('Command \'' + command + '\' failed.')
        # Return results when prompt is shown
        if '*' in line:
            return appender.rstrip()
        appender+=line
      #print("Result: " + line),

def get_start_address():
    """Returns the curently selected start address in hex format."""
    try:
        return command("P")
    except EppException as e:
        print 'No EPROM type is selected.', e.value

def set_start_address(address):
    """Sets the EPROM start address in hex format."""
    try:
        command(address + "P")
    except EppException as e:
        print 'No EPROM type is selected, or value is higher than end address.', e.value

def get_end_address():
    """Returns the currently selected last address in Hex format"""
    try:
        return command("L")
    except EppException as e:
        print 'No EPROM type is selected.', e.value

def set_end_address(address):
    """Sets the EPROM end address in hex format."""
    try:
        command(address + "L")
    except EppException as e:
        print 'No EPROM type is selected, or value is lower than start address.', e.value
            
def get_offset_address():
    """Returns the currently selected offset address in Hex format"""
    return command("O")

def set_offset_address(address):
    """Sets the EPROM end address in hex format."""
    command(address + "O")
        
def read():
    """Returns String of contents of the selected EPROM in Intel format."""
    print(command("R"))
    
def is_empty():
    """Returns True if EPROM is empty between defined start and end address values."""
    try:
        command("T")
    except EppException:
        return False
    else:
        return True

def get_eprom_type():
    """Returns EPROM type in hex format."""
    return command("S")
        
def set_eprom_type(eprom_type):
    """Sets the EPROM type in hex format."""
    command(eprom_type + "S")
    
"""    

set_start_address("0000")
print "Start address: " + get_start_address()
set_end_address("00A0")
print "End address: " + get_end_address()
read()
print("Is empty?: " + str(is_empty()))

ser.close()
"""
