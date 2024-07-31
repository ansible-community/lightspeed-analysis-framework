import os
import json
# from analysis_code.analyze_edits import check_edits

def get_rejected_suggestions(user_data_folder, user_file):

    print(f"starting analyzing {user_file}...")

    input_file_name = os.path.join(user_data_folder, user_file)

    output_folder = f"{user_data_folder}/rejection_analysis"
    os.makedirs(output_folder, exist_ok=True)
    
    output_file_name = os.path.join(output_folder, f"new_useful_test_data_{user_file}.jsonl")

    extracted_lines = []

    count_rejected = 0
    count_considered = 0

    # Open the input file for reading
    with open(input_file_name, "r") as input_file:
        lines = input_file.readlines()

    # Iterate through the lines in the input file
    for i, line in enumerate(lines):

        line = json.loads(line.strip())

        # Check if the current line is an inlineSuggestionFeedback and the action is 1, i.e., rejected
        if line["event"] == 'inlineSuggestionFeedback' and "action" in line["properties"] and line["properties"]["action"]:
            if(i == 0):
                continue
            
            if line["properties"]["action"] == '1':
                count_rejected += 1

                # Extract the previous line
                previous_line = json.loads(lines[i - 1].strip()) if i > 0 else json.loads("")
                current_line = line

                # previous line of accepted inlineSuggestion should be a completion event
                if(previous_line["event"] == "inlineSuggestionFeedback"
                    or previous_line["event"] == "ansibleContentFeedback"):
                    continue
                    
                else:
                    # Create a dictionary to store the extracted lines
                    extracted_data = {
                        "Suggestion": previous_line,
                        "Action": current_line,
                    }
                    count_considered += 1
                
                extracted_lines.append(extracted_data)


    with open(output_file_name, "w") as output_file:
        for data in extracted_lines:

            rejected_item = {}

            if("request" not in data["Suggestion"]["properties"]):
                continue

            # get the 'task name' and 'playbook context' for which the completion was triggered
            prompt = data["Suggestion"]["properties"]["request"]["prompt"]
            # print("*****", prompt)

            if(not prompt):
                continue

            content = prompt.split("- name: ")
            task_name = content.pop()
            playbook_context = "- name: ".join(content).strip()
            
            # get the suggestion that was accepted
            prediction = "" 
            if ("predictions" in data["Suggestion"]["properties"]["response"]
                and  data["Suggestion"]["properties"]["response"]["predictions"] != None):
                    prediction = data["Suggestion"]["properties"]["response"]["predictions"][0]

            rejected_item["playbook context"] = playbook_context
            rejected_item["task name"] = task_name
            rejected_item["suggestion"] = prediction

            # output_file.write("playbook context:\n{}".format(playbook_context))
            # output_file.write("task name:\n{}".format(task_name))
            output_file.write(f"{json.dumps(rejected_item)}\n")

    input_file.close()
    output_file.close()

    return {"count_rejected": count_rejected, "count_considered": count_considered}


print("starting analysis...")
user_data_folder = "data/"

count_users = 0
count_rejected = 0
count_considered = 0
for file in os.listdir(user_data_folder):
    if(file.endswith(".jsonl")):
        count_users += 1
        user_data = get_rejected_suggestions(user_data_folder, file)
        count_rejected += user_data["count_rejected"]
        count_considered += user_data["count_considered"]

    else:
        continue

print(f"Users: {count_users}")
print(f"Rejected: {count_rejected}")
print(f"Rejections considered: {count_considered}")


