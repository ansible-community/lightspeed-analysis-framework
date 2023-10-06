from difflib import SequenceMatcher, Differ
import json
import yaml

def recursive_items(dictionary, i):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value, i+1)
        else:
            yield (i, key, value)

def check_edits(suggestion_task, user_task):

    edit_analysis = {}

    edit_analysis["suggestion_task"] = dict(**suggestion_task)
    edit_analysis["user_task"] = dict(**user_task)

    same_module = True
    key_edit = False
    value_edit = False
    difference = []

    matcher = SequenceMatcher(None, json.dumps(suggestion_task), json.dumps(user_task))
    match_percentage = matcher.ratio() * 100

    if(match_percentage == 100):
        edit_analysis["match_percentage"] = match_percentage
        edit_analysis["same_module"] = same_module
        edit_analysis["key_edit"] = key_edit
        edit_analysis["value_edit"] = value_edit
        edit_analysis["difference"] = difference
        return edit_analysis
    
    # get actual text difference
    differ = Differ()
    difference = list(differ.compare(yaml.dump(suggestion_task, sort_keys=False).splitlines(), yaml.dump(user_task, sort_keys=False).splitlines()))

    # check the module

    if(len(list(user_task.keys())) < 2):
        same_module = False
        
        edit_analysis["match_percentage"] = match_percentage
        edit_analysis["same_module"] = same_module
        edit_analysis["key_edit"] = key_edit
        edit_analysis["value_edit"] = value_edit
        edit_analysis["difference"] = difference
        return edit_analysis

    # print(suggestion_task)
    suggestion_module = list(suggestion_task.keys())[1]
    user_module = list(user_task.keys())[1]

    if(suggestion_module != user_module):
        same_module = False
        
        edit_analysis["match_percentage"] = match_percentage
        edit_analysis["same_module"] = same_module
        edit_analysis["key_edit"] = key_edit
        edit_analysis["value_edit"] = value_edit
        edit_analysis["difference"] = difference
        return edit_analysis

    suggestion_task_flatten = {}
    user_task_flatten = {}

    for i, key, value in recursive_items(suggestion_task, 1):
        # print(f"{i}_{key} -> {value}")
        suggestion_task_flatten[f"{i}_{key}"] = value

    for i, key, value in recursive_items(user_task, 1):
        # print(f"{i}_{key} -> {value}")
        user_task_flatten[f"{i}_{key}"] = value

    suggestion_task_keys = list(suggestion_task_flatten.keys())
    user_task_keys = list(user_task_flatten.keys())

    # check for key and value edits
    if(len(suggestion_task_keys) != len(user_task_keys)):
        key_edit = True
    
    if(len(suggestion_task_keys) == len(user_task_keys)):
        for i in range (len(suggestion_task_keys)):
            s_key = suggestion_task_keys[i]
            u_key = user_task_keys[i]
            if(s_key == u_key):
                if(suggestion_task_flatten[s_key] != user_task_flatten[u_key]):
                    value_edit = True
            else:
                key_edit = True

    edit_analysis["match_percentage"] = match_percentage
    edit_analysis["same_module"] = same_module
    edit_analysis["key_edit"] = key_edit
    edit_analysis["value_edit"] = value_edit
    edit_analysis["difference"] = difference
    return edit_analysis