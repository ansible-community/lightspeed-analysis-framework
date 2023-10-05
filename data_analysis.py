import os
from analysis_code.combine_items import combine_items

print("starting analysis...")
user_data_folder = "data/user_files"

for file in os.listdir(user_data_folder):
    # print(file)
    if(file.endswith(".jsonl")):
        combine_items(user_data_folder, file)
    else:
        continue