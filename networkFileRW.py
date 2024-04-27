#!/usr/bin/env python3
# networkFileRW.py
# Amber Chatman
# Friday, April 5, 2024


# Importing JSON module with try/except clause
import json  

## Constants for file names
EQUIP_R_FILE = "equip_r.txt"
EQUIP_S_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
INVALID_FILE = "invalid.txt"

# Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

# Function to load data from JSON file
def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}

# Function to write data to JSON file
def write_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        # Prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

# Function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount

def main():
    # Load data from JSON files
    routers = load_json_file(EQUIP_R_FILE)
    switches = load_json_file(EQUIP_S_FILE)

    # The updated dictionary holds the device name and new IP address
    updated = {}

    # List of bad addresses entered by the user
    invalidIPAddresses = []

    # Accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    # Flags and sentinels
    quitNow = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        # Function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        # Function call to get valid IP address
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        # Update device
        if 'r' in device:
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        # Add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    # User finished updating devices
    print("\nSummary:")
    print("\nNumber of devices updated:", devicesUpdatedCount)

    # Write the updated equipment dictionary to a file
    write_json_file(UPDATED_FILE, updated)
    print("Updated equipment written to file 'updated.txt'")

    # Write the list of invalid addresses to a file
    write_json_file(INVALID_FILE, invalidIPAddresses)
    print("Number of invalid addresses attempted:", invalidIPCount)
    print("List of invalid addresses written to file 'invalid.txt'")

# Top-level scope check
if __name__ == "__main__":
    main()
