import os
from data_handling_code.sort_data import sort_file_data

def get_user_data(file, user):
    """Extract data of a particular user from the filtered data file

    Args:
        file (string): file uri of the filtered data file
        group (strip): user id

    Returns:
        string: folder uri where the extracted user's data file is located
    """

    input_file_name = file

    output_folder = "data/user_files"
    os.makedirs(output_folder, exist_ok=True)
    
    output_file_name = os.path.join(output_folder, f"{user}_filtered_file.jsonl")
    # output_file_name = f"{user}_output_file.jsonl"

    search_substring = f'"userId":"{user}"'
    print("search substring -> ", search_substring)

    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        for line in input_file:
            if search_substring in line:
                output_file.write(line)

    input_file.close()
    output_file.close()

    # sort file
    sort_file_data(output_file_name)

    # remove the filtered file as the final file is the sorted file
    os.remove(output_file_name)
    

    return output_folder


