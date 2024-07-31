import json
input_file_name = "data/_filtered.jsonl"

with open(input_file_name, "r") as input_file:
    lines = input_file.readlines()

    completion_events = 0
    accepted_events = 0
    for i, line in enumerate(lines):
        line = json.loads(line.strip())
        if(line["event"] == "inlineSuggestionFeedback"):
            # print(completion_events)
            completion_events = completion_events + 1

            # print(line)
            if("action" in line["properties"] and line["properties"]["action"] == '0'):
                accepted_events = accepted_events + 1


    print("total events: ", completion_events)
    print("accepted events: ", accepted_events)
