# About the project

This framework analyzes the user modification patterns after they have accpeted the suggestion received by ansible-lightspeed service.

## How to use

1. Place the the raw `.jsonl` file at the root of the project.
2. Run `group_data_processing.py` (for extracting a user groups data) or `user_data_processing` (for extracting a particular user's data) based on the requirement. Before running this code, make sure to update the placeholders in the code files. Execution of the code will do the followings:
    * Create a `data` folder in the root.
    * Create filtered data files and place it inside `data/`.
    * Segregate users from the group and create individual data files for each user and place it inside `data/user_files/`.
    * Sort the events in individual user files based on the event timestamp.
3. Run `data_analysis.py` to start the analysis of individual user files.
_NOTE:  Make sure that `data/user_files` contains user files before running the analysis code_
4. Analysis code will print info in the terminal output as well as create analysis files for individual users under `data/user_files/analysis/`.
5. There are some miscellaneous code present in the `misc_code` directory. You can run these as standalones.
