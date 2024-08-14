# Matthew Buzalsky, Colby Connolly
# Read csv data and write to new file

import csv

data_list = []

# Input file name

file_name = input("Please input the name of the csv file (without .csv): ")

# New file name

new_name = file_name + ".csv"


if __name__ == "__main__":

    # Read raw data file

    with open(new_name, "r") as data_file:

        # Print each line of data

        wind_file = csv.reader(data_file)

        # Skip two rows of headers

        next(wind_file, None)
        next(wind_file, None)

        for row in wind_file:
            
            # Check for the first timestamp

            new_list = row[0].split(":")

            if new_list[2] == "00":

                # Add to list

                data_list.append(row)
            
            else:
                pass

    # Write to new csv file

    with open("Final_Proj_Data_Minute_Morning.csv", "w", newline = "") as new_file:
        new_wind_file = csv.writer(new_file, delimiter = ",")

        # Write headers

        new_wind_file.writerow(["","Solar Data", "Wind Data"])
        new_wind_file.writerow(["Time", "Power (W)", "Voltage (V)", "Speed (m/s)"])

        # Write each line to the csv file

        for element in data_list:
            new_wind_file.writerow(element)
