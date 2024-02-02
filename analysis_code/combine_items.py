import os
import json
import yaml
from yaml import SafeLoader
from analysis_code.analyze_edits import check_edits

def combine_items(user_data_folder, user_file):

    print(f"starting analyzing {user_file}...")

    global count_committed_tasks
    global less_than_fifty
    global more_than_fifty
    global full_hundred
    global changed_module
    global changed_key_part
    global changed_value_part
    global suggestion_errors
    global count_accepted_suggestions
    global count_valid_suggestions_analyzed
    global zero_match
    global deleted_after_accepting
    global minor_edit_key_change
    global minor_edit_value_change
    global minor_edit_module_change

    count_committed_tasks = 0
    count_accepted_suggestions = 0
    count_valid_suggestions_analyzed = 0
    less_than_fifty = 0
    more_than_fifty = 0
    full_hundred = 0
    changed_module = 0
    changed_key_part = 0
    changed_value_part = 0
    suggestion_errors = 0
    zero_match = 0
    deleted_after_accepting = 0
    minor_edit_key_change = 0
    minor_edit_value_change = 0
    minor_edit_module_change = 0

    def get_desired_ansible_task(model_suggestion, yaml_string, playbook_context, output_file):

        global count_committed_tasks
        global less_than_fifty
        global more_than_fifty
        global full_hundred
        global changed_module
        global changed_key_part
        global changed_value_part
        global suggestion_errors
        global count_accepted_suggestions
        global count_valid_suggestions_analyzed
        global zero_match
        global deleted_after_accepting
        global minor_edit_key_change
        global minor_edit_value_change
        global minor_edit_module_change


        task_name = model_suggestion["name"]

        try:
            ansible_dict = yaml.load(yaml_string, Loader=SafeLoader)
        except:
            ansible_dict = {}
        
        final_user_edited_task = {}

        if(ansible_dict is None):
            return

        for item in ansible_dict:

            # a task has to be a dict
            if(not isinstance(item, dict)):
                continue

            if(len(model_suggestion.keys()) <= 1):
                suggestion_errors += 1
                count_accepted_suggestions -= 1
                count_valid_suggestions_analyzed -= 1
                continue

            if "tasks" not in item:
                if(isinstance(item, dict) and "name" in item and item["name"] == task_name):
                    final_user_edited_task = item

                    result = check_edits(model_suggestion, final_user_edited_task, playbook_context)
                    print("done top")
                    output_file.write(f"{json.dumps(result, default=str)}\n")
                    match_percentage = result["match_percentage"]

                    if(match_percentage == 100):
                        full_hundred += 1
                    elif(match_percentage >= 50 and match_percentage < 100):
                        more_than_fifty += 1
                    elif(match_percentage > 0 and match_percentage < 50):
                        less_than_fifty += 1
                    elif(match_percentage == 0):
                        zero_match += 1

                    module_edit = not result["same_module"]
                    key_edit = result["key_edit"]
                    value_edit = result["value_edit"]
                    deleted_suggestion = result["deleted_after_accepting"]
                    if(module_edit):
                        changed_module += 1
                        if(match_percentage >= 50):
                            minor_edit_module_change += 1
                    if(key_edit):
                        changed_key_part += 1
                        if(match_percentage >= 50 and not module_edit):
                            minor_edit_key_change += 1
                    if(value_edit):
                        changed_value_part += 1
                        if(match_percentage >= 50 and not module_edit):
                            minor_edit_value_change += 1
                    if(deleted_suggestion):
                        deleted_after_accepting += 1

                    count_committed_tasks += 1
                continue

            tasks = item["tasks"]
            if not tasks:
                continue

            for task in tasks:
                if(isinstance(task, dict) and "name" in task and task["name"] == task_name):
                    final_user_edited_task = task

                    result = check_edits(model_suggestion, final_user_edited_task, playbook_context)
                    print("done bottom")
                    output_file.write(f"{json.dumps(result, default=str)}\n")
                    match_percentage = result["match_percentage"]

                    if(match_percentage == 100):
                        full_hundred += 1
                    elif(match_percentage >= 50 and match_percentage < 100):
                        more_than_fifty += 1
                    elif(match_percentage > 0 and match_percentage < 50):
                        less_than_fifty += 1
                    elif(match_percentage == 0):
                        zero_match += 1

                    module_edit = not result["same_module"]
                    key_edit = result["key_edit"]
                    value_edit = result["value_edit"]
                    deleted_suggestion = result["deleted_after_accepting"]
                    if(module_edit):
                        changed_module += 1
                        if(match_percentage >= 50):
                            minor_edit_module_change += 1
                    if(key_edit):
                        changed_key_part += 1
                        if(match_percentage >= 50 and not module_edit):
                            minor_edit_key_change += 1
                    if(value_edit):
                        changed_value_part += 1
                        if(match_percentage >= 50 and not module_edit):
                            minor_edit_value_change += 1
                    if(deleted_suggestion):
                        deleted_after_accepting += 1

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
        if line["event"] == 'inlineSuggestionFeedback' and "action" in line["properties"] and line["properties"]["action"]:
            if(i == 0):
                continue
            
            count_valid_suggestions_analyzed += 1

            if line["properties"]["action"] == '0':
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
                    count_valid_suggestions_analyzed -= 1
                    continue

                if(next_line and next_line["event"] == "completion"
                    and next_line["properties"]["metadata"]
                    and next_line["properties"]["metadata"]["documentUri"]
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

            # get the 'task name' and 'playbook context' for which the completion was triggered
            prompt = data["Suggestion"]["properties"]["request"]["prompt"]
            content = prompt.split("- name: ")
            task_name = content.pop()
            playbook_context = "- name: ".join(content).strip()
            
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
                    get_desired_ansible_task(model_suggestion, yaml_string, playbook_context, output_file)
                    # output_file.write("Edits:\n{}\n".format(yaml_string))

                elif(data["Edits"]["event"] == 'ansibleContentFeedback'):
                    # if 'ansibleContentFeedback' event, file content will be in the 'content' key
                    if("content" not in data["Edits"]["properties"]):
                        suggestion_errors +=1
                        count_accepted_suggestions -=1
                        count_valid_suggestions_analyzed -= 1
                        continue 

                    yaml_string = data["Edits"]["properties"]["content"]
                    get_desired_ansible_task(model_suggestion, yaml_string, playbook_context, output_file)
                    # output_file.write("Edits:\n{}\n".format(yaml_string))

                else:
                    pass

    user_data = {}

    count_accepted_suggestions -= suggestion_errors
    count_valid_suggestions_analyzed -= suggestion_errors
    
    user_data["suggestions_analyzed"] = count_valid_suggestions_analyzed
    user_data["accepted_suggestion"] = count_accepted_suggestions
    user_data["committed_suggestions"] = count_committed_tasks
    user_data["fully_accepted"] = full_hundred
    user_data["major_edits"] = less_than_fifty
    user_data["minor_edits"] = more_than_fifty
    user_data["changed_key"] = changed_key_part
    user_data["changed_value"] = changed_value_part
    user_data["changed_module"] = changed_module
    user_data["no_match"] = zero_match
    user_data["deleted_after_accepting"] = deleted_after_accepting
    user_data["minor_edit_key_change"] = minor_edit_key_change
    user_data["minor_edit_value_change"] = minor_edit_value_change
    user_data["minor_edit_module_change"] = minor_edit_module_change

    print(f"Extracted lines have been written to '{output_file_name}'.")

    return user_data
