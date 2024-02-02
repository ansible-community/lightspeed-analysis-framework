# traverse recursively over the dict
def recursive_items(dictionary, i):
    for key, value in sorted(dictionary.items()):
        if type(value) is dict:
            yield from recursive_items(value, i+1)
        else:
            yield (i, key, value)

# sort the nested dict recursively 
def sort_nested_dict(nested_dict):
    sorted_dict = {}

    for key in sorted(nested_dict):
        if isinstance(nested_dict[key], dict):
            sorted_dict[key] = sort_nested_dict(nested_dict[key])
        else:
            sorted_dict[key] = nested_dict[key]
    
    return sorted_dict

# type cast keys to string in the nested dict recursively 
def type_cast_key_to_str(nested_dict):
    _dict = {}

    for key in nested_dict:
        if isinstance(nested_dict[key], dict):
            _dict[key] = type_cast_key_to_str(nested_dict[key])
        else:
            _dict[str(key)] = nested_dict[key]
    
    return _dict