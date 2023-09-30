from code.filter_data import filter_data
from code.get_group_data import get_group_data
from code.segregate_users import segregate_users_from_group

# create data files for analysis
original_file = "all.jsonl"

# filter the file
print("filtereing file...")
filtered_file_name = filter_data(original_file)
print("FINISHED!")
print(f"file pulished: {filtered_file_name}\n")

# get group data
group_to_analyze = "ansible-sme"
print("getting group data...")
group_data_file_name = get_group_data(filtered_file_name, group_to_analyze)
print("FINISHED!")
print(f"file pulished: {group_data_file_name}\n")

# segregate users from the group
print("segregating users...")
users_folder = segregate_users_from_group(group_data_file_name)
print("FINISHED!")
print(f"files pulished inside: {users_folder}\n")


# analysis part

