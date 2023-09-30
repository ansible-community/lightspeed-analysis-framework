import os
import re


def segregate_users_from_group(file):
    """Segregate the user data from the group into separate user files

    Args:
        file (string): file uri of the raw group data

    Returns:
        string: folder uri where the user data files are located after segregation
    """

    input_file_name = file
    user_lines = {}
    unmatched_lines = []

    with open(input_file_name, "r") as input_file:
        for line in input_file:

            # match the "userId" pattern and segregate the data based on unique user IDs
            user_id_match = re.search(r'"userId":"([^"]+)"', line)

            if user_id_match:
                user_id = user_id_match.group(1)
                if user_id not in user_lines:
                    user_lines[user_id] = []
                user_lines[user_id].append(line)
            else:
                unmatched_lines.append(line)

    output_folder = "data/user_files"
    os.makedirs(output_folder, exist_ok=True)

    for user_id, lines in user_lines.items():
        output_file_name = os.path.join(output_folder, f"{user_id}_filtered_file.jsonl")
        with open(output_file_name, "w") as output_file:
            for line in lines:
                output_file.write(line)
            output_file.close()

    input_file.close()

    return output_folder

