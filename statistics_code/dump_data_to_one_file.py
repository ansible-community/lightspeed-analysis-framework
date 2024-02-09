import os

print("starting analysis...")
user_data_folder = "data/user_files/analysis"

output_file = "data_dump.jsonl"

with open(output_file, "w") as output_file:
    for file in os.listdir(user_data_folder):
        print(file)
        with open(f"{user_data_folder}/{file}", 'r') as input_file:
            for line in input_file:
                output_file.write(line)

input_file.close()
output_file.close()