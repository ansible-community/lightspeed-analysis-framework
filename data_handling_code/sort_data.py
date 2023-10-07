import re
import os
from datetime import datetime

def sort_file_data(file):

    timestamp_pattern = r'"originalTimestamp":"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}\+\d{2}:\d{2})"'

    # Create a list to store lines with timestamps
    lines_with_timestamps = []

    # for file in user_files:
    # Open the input file for reading
    input_file_name = file
    with open(input_file_name, "r") as input_file:
        # Loop through each line in the input file
        for line in input_file:
            
            # Extract the timestamp using the regex pattern
            timestamp_match = re.search(timestamp_pattern, line)
            
            # If a timestamp is found, add it to the list along with the line
            if timestamp_match:
                timestamp = timestamp_match.group(1)
                timestamp = timestamp.rsplit("+", 1)[0]
                lines_with_timestamps.append((timestamp, line))

    # Sort the lines based on the extracted timestamps
    lines_with_timestamps.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%S.%f'))

    file_name = os.path.basename(file)
    folder_name = os.path.dirname(file)

    output_file_name = os.path.join(folder_name, f"sorted_{file_name}")

    with open(output_file_name, "w") as output_file:
        # Write the sorted lines to the output file
        for _, line in lines_with_timestamps:
            output_file.write(line)

    # Close both files
    input_file.close()
    output_file.close()

    print(f"file sorted and written in: {output_file_name}")




