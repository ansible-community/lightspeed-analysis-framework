import os
import csv
from analysis_code.combine_items import combine_items

print("starting analysis...")
user_data_folder = "test/user_files"

header = ["id", "suggestions_analyzed", "accepted_suggestion", "committed_suggestions", "fully_accepted", "major_edits", "minor_edits", "changed_key", "changed_value", "changed_module", "no_match", "deleted_after_accepting", "minor_edit_key_change", "minor_edit_value_change", "minor_edit_module_change"]

with open('user_analysis.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()

    for file in os.listdir(user_data_folder):
        if(file.endswith(".jsonl")):
            user_data = combine_items(user_data_folder, file)
            user_data["id"] = file
            
            if(user_data["committed_suggestions"] != 0):
                writer.writerow(user_data)

        else:
            continue