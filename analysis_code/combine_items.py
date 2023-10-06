import os
import json
import yaml
from yaml import SafeLoader
from difflib import SequenceMatcher, Differ
from pprint import pprint
from analysis_code.analyze_edits import check_edits

def combine_items(user_data_folder, user_file):

    print(f"starting analyzing {user_file}...")

    global count_committed_tasks
    global less_than_fifty
    global full_hundred
    global changed_module
    global changed_key_part
    global changed_value_part
    global suggestion_errors
    global count_accepted_suggestions

    count_committed_tasks = 0
    count_accepted_suggestions = 0
    less_than_fifty = 0
    full_hundred = 0
    changed_module = 0
    changed_key_part = 0
    changed_value_part = 0
    suggestion_errors = 0

    def get_desired_ansible_task(model_suggestion, yaml_string, output_file):

        global count_committed_tasks
        global less_than_fifty
        global full_hundred
        global changed_module
        global changed_key_part
        global changed_value_part
        global suggestion_errors
        global count_accepted_suggestions

        task_name = model_suggestion["name"]

        try:
            python_dict = yaml.load(yaml_string, Loader=SafeLoader)
        except:
            python_dict = {}
        
        desired_task = {}

        if(python_dict is None):
            return

        for item in python_dict:

            if(len(model_suggestion.keys()) <= 1):
                suggestion_errors += 1
                count_accepted_suggestions -= 1
                continue

            if "tasks" not in item:
                if("name" in item and item["name"] == task_name):
                    desired_task = item

                    result = check_edits(model_suggestion, desired_task)
                    output_file.write(f"{json.dumps(result)}\n")
                    # print(json.dumps(result))
                    match_percentage = result["match_percentage"]
                    # print(match_percentage)

                    if(match_percentage == 100):
                        full_hundred += 1
                    elif(match_percentage < 50):
                        less_than_fifty += 1
                    

                    module_edit = not result["same_module"]
                    key_edit = result["key_edit"]
                    value_edit = result["value_edit"]
                    if(module_edit):
                        changed_module += 1
                    if (key_edit):
                        changed_key_part += 1
                    if (value_edit):
                        changed_value_part += 1

                    count_committed_tasks += 1
                continue

            
            tasks = item["tasks"]
            if not tasks:
                continue

            for task in tasks:
                if("name" in task and task["name"] == task_name):
                    desired_task = task

                    result = check_edits(model_suggestion, desired_task)
                    output_file.write(f"{json.dumps(result)}\n")
                    # print(json.dumps(result))
                    match_percentage = result["match_percentage"]
                    # print(match_percentage)

                    if(match_percentage == 100):
                        full_hundred += 1
                    elif(match_percentage < 50):
                        less_than_fifty += 1

                    module_edit = not result["same_module"]
                    key_edit = result["key_edit"]
                    value_edit = result["value_edit"]
                    if(module_edit):
                        changed_module += 1
                    if (key_edit):
                        changed_key_part += 1
                    if (value_edit):
                        changed_value_part += 1

                    count_committed_tasks += 1
                    continue
                continue


    input_file_name = os.path.join(user_data_folder, user_file)

    output_folder = f"{user_data_folder}/analysis"
    os.makedirs(output_folder, exist_ok=True)
    
    output_file_name = os.path.join(output_folder, f"new_useful_test_data_{user_file}.jsonl")

    extracted_lines = []

    # Open the input file for reading
    with open(input_file_name, "r") as input_file:
        lines = input_file.readlines()

    # Iterate through the lines in the input file
    for i, line in enumerate(lines):

        line = json.loads(line.strip())

        # Check if the current line is an inlineSuggestionFeedback and the action is 0, i.e., accepted
        if line["event"] == 'inlineSuggestionFeedback' and "action" in line["properties"] and line["properties"]["action"] == '0':
            if(i == 0):
                continue
            
            count_accepted_suggestions += 1

            # Extract the previous line, current line, and next line
            previous_line = json.loads(lines[i - 1].strip()) if i > 0 else json.loads("")
            current_line = line

            edit_line = {}
            next_line = json.loads(lines[i + 1].strip()) if i < len(lines) - 1 else json.loads("null")

            # previous line of accepted inlineSuggestion should be a completion event
            if(previous_line["event"] == "inlineSuggestionFeedback"
                or previous_line["event"] == "ansibleContentFeedback"):
                count_accepted_suggestions -= 1
                continue

            if(next_line and next_line["event"] == "completion"
                and next_line["properties"]["metadata"]["documentUri"] == previous_line["properties"]["metadata"]["documentUri"]):
                edit_line = next_line
            
            elif(next_line and next_line["event"] == "ansibleContentFeedback"
                and "documentUri" in next_line["properties"]):
                if (next_line["properties"]["documentUri"] == previous_line["properties"]["metadata"]["documentUri"]):
                    edit_line = next_line
            
            elif(next_line and next_line["event"] == "ansibleContentFeedback"
                and "documentUri" not in next_line["properties"]):
                if (next_line["properties"]["data"]["ansibleContent"]["documentUri"] == previous_line["properties"]["metadata"]["documentUri"]):
                    edit_line = next_line
                
            else:
                for j in range(i, len(lines) - 1):
                    new_line = json.loads(lines[j].strip())
                    # print(j, new_line["event"], new_line["originalTimestamp"])
                    if(new_line["event"] == "ansibleContentFeedback" 
                        and "documentUri" in new_line["properties"]
                        and new_line["properties"]["documentUri"] == previous_line["properties"]["metadata"]["documentUri"]):
                        edit_line = new_line
                        break
                    elif(new_line["event"] == "completion" 
                        and "documentUri" in new_line["properties"]["metadata"]
                        and new_line["properties"]["metadata"]["documentUri"] == previous_line["properties"]["metadata"]["documentUri"]):
                        edit_line = new_line
                        break
            
            # Create a dictionary to store the extracted lines
            extracted_data = {
                "Suggestion": previous_line,
                "Action": current_line,
                "Edits": edit_line
            }
            
            extracted_lines.append(extracted_data)


    with open(output_file_name, "w") as output_file:
        for data in extracted_lines:

            # get the task name for which the completion was triggered
            prompt = data["Suggestion"]["properties"]["request"]["prompt"]
            task_name = prompt.split("- name: ")[-1]
            # output_file.write("\nTask name:\n{}\n".format(task_name))
            
            # get the suggestion that was accepted
            prediction = "" 
            if ("predictions" in data["Suggestion"]["properties"]["response"]
                and  data["Suggestion"]["properties"]["response"]["predictions"] != None):
                    prediction = data["Suggestion"]["properties"]["response"]["predictions"][0]

            # output_file.write("Suggestion:\n{}\n".format(prediction))

            # create json object for the prompt (task name) and suggestion
            suggestion = yaml.load(prediction, SafeLoader)
            model_suggestion = {'name': task_name}
            if (suggestion != None):
                model_suggestion.update(suggestion)

            # get the file content during next event to compare edits made in the previous
            # acceptance of the suggestion
            if(data["Edits"] == {}):
                pass
            else:
                if(data["Edits"]["event"] == 'completion'):
                    # if 'completion' event, file content will be in the 'prompt' key
                    yaml_string = data["Edits"]["properties"]["request"]["prompt"]
                    get_desired_ansible_task(model_suggestion, yaml_string, output_file)
                    # output_file.write("Edits:\n{}\n".format(yaml_string))

                elif(data["Edits"]["event"] == 'ansibleContentFeedback'):
                    # if 'ansibleContentFeedback' event, file content will be in the 'content' key
                    if("content" not in data["Edits"]["properties"]):
                        suggestion_errors +=1
                        count_accepted_suggestions -=1
                        continue 

                    yaml_string = data["Edits"]["properties"]["content"]
                    get_desired_ansible_task(model_suggestion, yaml_string, output_file)
                    # output_file.write("Edits:\n{}\n".format(yaml_string))

                else:
                    pass

            # output_file.write("---------------------------------------------------------------\n")  # Add a separator between matched sections


    count_accepted_suggestions -= suggestion_errors

    print(f"Suggestion errors: {suggestion_errors}")
    print(f"Accepted suggestions): {count_accepted_suggestions}")
    print(f"Committed suggestions): {count_committed_tasks}")
    print(f"Uncommitted suggestions): {count_accepted_suggestions - count_committed_tasks}")
    print(f"Commit percent: {round((count_committed_tasks/count_accepted_suggestions) * 100, 2)}%")

    print(f"Fully accepted: {full_hundred}")
    print(f"Majorly edited (> 50%) keeping the same module: {abs(less_than_fifty - changed_module)}")

    print(f"Changed key part: {changed_key_part}")
    print(f"Changed value part: {changed_value_part}")
    print(f"Changed the module: {changed_module}")

    print(f"Extracted lines have been written to '{output_file_name}'.")
    print("completed!")
    print("\n")
