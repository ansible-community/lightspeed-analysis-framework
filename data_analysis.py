import os
import re
import csv
from analysis_code.combine_items import combine_items

print("starting analysis...")
user_data_folder = "data/user_files"

output_csv_file = 'user_analysis.csv'

header = ["id", "suggestions_analyzed", "accepted_suggestion", 
        "committed_suggestions", "fully_accepted", "major_edits", 
        "minor_edits", "changed_key", "changed_value", "changed_module", 
        "no_match", "deleted_after_accepting", "minor_edit_key_change", 
        "minor_edit_value_change", "minor_edit_module_change"]

user_id_pattern = r'sorted_(.*?)_filtered_file\.jsonl'

with open(output_csv_file, 'w') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()

    for file in os.listdir(user_data_folder):
        if(file.endswith(".jsonl")):
            user_data = combine_items(user_data_folder, file)
            match = re.search(user_id_pattern, file)
            if match:
                user_data["id"] = match.group(1)
            
            if(user_data["committed_suggestions"] != 0):
                writer.writerow(user_data)

        else:
            continue