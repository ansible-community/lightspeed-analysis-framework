import csv
import re

# read the 'user_analysis.csv' file
with open("user_analysis.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)

total_users = len(data)
print("Total users analyzed:", total_users)

total_suggestions_analyzed = 0
total_accepted_suggestions = 0
total_rejected_suggestions = 0
total_fully_accepted_suggestions = 0
total_majorly_edited_suggestions = 0
total_minorly_edited_suggestions = 0
total_changed_key = 0
total_changed_value = 0
total_changed_module = 0
total_no_match = 0
total_deleted_after_accepting = 0

key_edits_in_minor_changes = 0
value_edits_in_minor_change = 0
module_edits_in_minor_changes = 0

for user in data:
    total_suggestions_analyzed += int(user["suggestions_analyzed"])
    total_accepted_suggestions += int(user['committed_suggestions'])
    total_rejected_suggestions += int(user["rejected_suggestion"])
    total_fully_accepted_suggestions += int(user['fully_accepted'])
    total_majorly_edited_suggestions += int(user['major_edits'])
    total_changed_key += int(user['changed_key'])
    total_changed_value += int(user['changed_value'])
    total_changed_module += int(user['changed_module'])
    total_no_match += int(user['no_match'])
    total_deleted_after_accepting += int(user["deleted_after_accepting"])
    total_minorly_edited_suggestions += int(user["minor_edits"])

    key_edits_in_minor_changes += int(user["minor_edit_key_change"])
    value_edits_in_minor_change += int(user["minor_edit_value_change"])
    module_edits_in_minor_changes += int(user["minor_edit_module_change"])

print("Total suggestions analyzed:", total_suggestions_analyzed)
print("Total accepted suggestions:", total_accepted_suggestions)
print("Total rejected suggestions:", total_rejected_suggestions)
print("\n")

print("Total fully accepted suggestions:", total_fully_accepted_suggestions)
print("Total majorly (>= 50%) edited suggestions:", total_majorly_edited_suggestions)
print("Total minorly (< 50%) edited suggestions:", total_minorly_edited_suggestions)
print("\n")

print("Total zero percent matched suggestions:", total_no_match)
print("Total deleted suggestions after accepting:", total_deleted_after_accepting)
print("\n")

print("Total changed key suggestions:", total_changed_key)
print("Total changed value suggestions:", total_changed_value)
print("Total changed module suggestions:", total_changed_module)
print("\n")

print("Total key changes in minor edits:", key_edits_in_minor_changes)
print("Total value changes in minor edits:", value_edits_in_minor_change)
print("Total module changes in minor edits:", module_edits_in_minor_changes)
print("\n")