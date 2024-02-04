def get_group_data(file, group):
    """Extract data of a particular group from the filtered data file

    Args:
        file (string): file uri of the filtered data file
        group (strip): group name

    Returns:
        string: file uri of the extracted group's data file
    """


    input_file_name = file
    output_file_name = f"data/{group}_filtered.jsonl"

    if(group):
        search_group_substring = group
    else:
        search_group_substring = r'"groups":[],'

    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        for line in input_file:
            if search_group_substring in line:
                output_file.write(line)

    # Close both files
    input_file.close()
    output_file.close()

    return output_file_name