import json
drop_indexes_file = open("missing-data.json")

drop_indexes = json.load(drop_indexes_file)
drop_indexes.sort()


with open("new-missing-data.json", "w") as outfile:
    json.dump(drop_indexes, outfile, skipkeys=True, indent=4)
