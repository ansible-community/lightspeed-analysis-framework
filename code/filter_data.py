import re
import os

def filter_data(file):
    """Filter the necessary keys and event data from the raw data file

    Args:
        file (string): file uri of the raw data file

    Returns:
        string: file uri of the filtered data
    """

    input_file_name = file

    output_folder = "data"
    os.makedirs(output_folder, exist_ok=True)

    output_file_name = "data/filtered_data.jsonl"

    # regex of unnecesasary keys
    message_id_pattern = r'"messageId":"([a-f0-9\-]+)",'
    project_id_pattern = r'"projectId":"([a-zA-Z0-9]+)",'
    write_key_pattern = r',"writeKey":"([a-zA-Z0-9]+)"'
    version_key_pattern = r'"version":([0-9]),'
    image_tags_pattern = r'"imageTags":"(latest [\d].[\d].\d*)",'
    hostname_pattern = r'"hostname":"([A-Za-z0-9\-]*)",'

    # events to extract
    search_substrings = ['"event":"inlineSuggestionFeedback"', '"event":"completion"', '"event":"ansibleContentFeedback"']


    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        for line in input_file:
            if any(substring in line for substring in search_substrings):

                # remove unnecessary strings
                line = line.replace('"anonymousId":null,"channel":"server","context":{"library":{"name":"analytics-python","version":"2.2.2"}},', '')
                line = line.replace('"integrations":{},', '')
                line = line.replace('"type":"track",', '')
                line = line.replace('"modelName":"ansible-wisdom-v11",', '')
                
                # remove unnecessary keys
                line = re.sub(message_id_pattern, "", line)
                line = re.sub(project_id_pattern, "", line)
                line = re.sub(version_key_pattern, "", line)
                line = re.sub(write_key_pattern, "", line)
                line = re.sub(image_tags_pattern, "", line)
                line = re.sub(hostname_pattern, "", line)

                # if any event substring is found, write the line to the output file
                output_file.write(line)

    # Close both files
    input_file.close()
    output_file.close()

    return output_file_name
