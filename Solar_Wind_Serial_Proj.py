# Matthew Buzalsky, Colby Connolly
# Anemometer and Solar project
# Introduction to Renewable Energy
# 7/15/2024

import serial.tools.list_ports
import keyboard
from datetime import datetime
import numpy as np
import csv

# Timestamp list

time_list = []

# Power (solar) list

pow_solar_list = []

# Voltage (wind) list

vol_wind_list = []

# Wind speed list

wind_speed = []

# List available COM ports

ports = serial.tools.list_ports.comports()

def write_to_file(final_data):

    # Define time stamp for file

    time_stamp = datetime.now()

    time_stamp_file = time_stamp.strftime("%H;%M;%S")

    # New file name
    
    file_name = "Final_Proj_" + time_stamp_file + ".csv"

    # Open write file

    try:
        with open(file_name, "w", newline = "") as final_data_file:
            final_data_write = csv.writer(final_data_file, delimiter = ",")

            # Write headers

            final_data_write.writerow(["","Solar Data", "Wind Data"])
            final_data_write.writerow(["Time", "Power (W)", "Voltage (V)", "Speed (m/s)"])

            # Write to file

            for data in final_data:
                final_data_write.writerow([data[0], data[1], data[2], data[3]])

    except:
        print("There were errors writing to the CSV file!")


if __name__ == "__main__":

    # Print available COM Ports

    for element in ports:
        print(str(element))

    
    # Choose COM port through user input
        
    user_input = input("Please enter in the COM port number for Arduino: ")
    baud_rate = int(input("Please enter in the baud rate: "))

    port_number = "COM" + user_input

    # Initialize Serial Monitor

    serial_monitor = serial.Serial(port_number, baud_rate)

    # Print from Serial Monitor

    while True:
        if serial_monitor.in_waiting:
            # Exit if ctrl + a is pressed

            if keyboard.is_pressed('ctrl+a'):
                break
            
            # Print serial
            else:
                serial_string = serial_monitor.readline()

                # Decode into utf-8

                new_string = str(serial_string.decode('utf-8').rstrip('\n'))

                # Capture time stamp
                current_time = datetime.now()
                time_string = current_time.strftime("%H:%M:%S")

                # Print final string

                final_string = time_string + ", " + new_string

                print(final_string)

                # Record data

                split_string = final_string.split(", ")

                # Condition to check if data is correct size

                if len(split_string) == 4:

                    # Data is not the correct size

                    if len(split_string[1]) < 14 or len(split_string[2].rstrip('V')) < 10 or len(split_string[3].rstrip(' m/s\r')) < 4:
                        pass
                    else:
                        # Append time string

                        time_val = split_string[0]

                        time_list.append(time_val)

                        # Append to each list

                        pow_solar_list.append(float(split_string[1][10:]))

                        vol_wind_list.append(float(split_string[2][6:-1]))

                        wind_speed.append(float(split_string[3][:-5]))

    
    # Create a list of values
                        
    list_values = [time_list, pow_solar_list, vol_wind_list, wind_speed]

    # Import into numpy

    new_list = np.array(list_values)

    # Transpose array

    final_data = new_list.T

    # Write to CSV 

    write_to_file(final_data)
    
