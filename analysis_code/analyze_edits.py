from difflib import SequenceMatcher, Differ
import yaml
from analysis_code.utils import recursive_items, sort_nested_dict, type_cast_key_to_str

def check_edits(suggestion_task, user_task, playbook_context):

    edit_analysis = {}

    edit_analysis["playbook_context"] = playbook_context

    # remove name from task before comparison and diff calculation
    if list(suggestion_task.keys())[0] == "name":
        edit_analysis["task_name"] = suggestion_task["name"]
        del suggestion_task["name"]
    if list(user_task.keys())[0] == "name":
        del user_task["name"]

    # type cats and sort task keys
    suggestion_task = type_cast_key_to_str(suggestion_task)
    user_task = type_cast_key_to_str(user_task)
    suggestion_task = sort_nested_dict(suggestion_task)
    user_task = sort_nested_dict(user_task)

    edit_analysis["suggestion_task"] = dict(**suggestion_task)
    edit_analysis["user_task"] = dict(**user_task)

    same_module = True
    deleted_after_accepting = False
    key_edit = False
    value_edit = False
    difference = []

    # print("+++ suggestion task", suggestion_task)
    # print("+++", list(suggestion_task.keys())[0])
    # print("+++", list(user_task.keys())[0])

    matcher = SequenceMatcher(None, yaml.dump(suggestion_task, sort_keys=False).splitlines(), yaml.dump(user_task, sort_keys=False).splitlines())
    match_percentage = matcher.ratio() * 100

    if(match_percentage == 100):
        edit_analysis["match_percentage"] = match_percentage
        edit_analysis["same_module"] = same_module
        edit_analysis["deleted_after_accepting"] = deleted_after_accepting
        edit_analysis["key_edit"] = key_edit
        edit_analysis["value_edit"] = value_edit
        edit_analysis["difference"] = difference
        return edit_analysis
    
    # get actual text difference
    differ = Differ()
    difference = list(differ.compare(yaml.dump(suggestion_task, sort_keys=False).splitlines(), yaml.dump(user_task, sort_keys=False).splitlines()))

    # check the module

    if(len(list(user_task.keys())) < 1):
        same_module = False
        deleted_after_accepting = True
        
        edit_analysis["match_percentage"] = match_percentage
        edit_analysis["same_module"] = same_module
        edit_analysis["deleted_after_accepting"] = deleted_after_accepting
        edit_analysis["key_edit"] = key_edit
        edit_analysis["value_edit"] = value_edit
        edit_analysis["difference"] = difference
        return edit_analysis

    suggestion_module = list(suggestion_task.keys())[0]
    user_module = list(user_task.keys())[0]

    if(suggestion_module != user_module):
        same_module = False
        
        edit_analysis["match_percentage"] = match_percentage
        edit_analysis["same_module"] = same_module
        edit_analysis["deleted_after_accepting"] = deleted_after_accepting
        edit_analysis["key_edit"] = key_edit
        edit_analysis["value_edit"] = value_edit
        edit_analysis["difference"] = difference
        return edit_analysis

    suggestion_task_flatten = {}
    user_task_flatten = {}

    for i, key, value in recursive_items(suggestion_task, 1):
        suggestion_task_flatten[f"{i}_{key}"] = value

    for i, key, value in recursive_items(user_task, 1):
        user_task_flatten[f"{i}_{key}"] = value

    suggestion_task_keys = list(suggestion_task_flatten.keys())
    user_task_keys = list(user_task_flatten.keys())

    # check for key and value edits
    if(len(suggestion_task_keys) != len(user_task_keys)):
        key_edit = True
        value_edit = True
    
    if(len(suggestion_task_keys) == len(user_task_keys)):
        for i in range (len(suggestion_task_keys)):
            s_key = suggestion_task_keys[i]
            u_key = user_task_keys[i]
            if(s_key != u_key):
                key_edit = True
            
            if(suggestion_task_flatten[s_key] != user_task_flatten[u_key]):
                    value_edit = True

    edit_analysis["match_percentage"] = match_percentage
    edit_analysis["same_module"] = same_module
    edit_analysis["deleted_after_accepting"] = deleted_after_accepting
    edit_analysis["key_edit"] = key_edit
    edit_analysis["value_edit"] = value_edit
    edit_analysis["difference"] = difference
    return edit_analysis