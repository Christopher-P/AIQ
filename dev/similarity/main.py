import json



names = ["CB", "COPA", "MultiRC", "RTE", "WiC", "WSC", "BoolQ", "ReCoRD"]

keys = set()

for name in names:
    file_path = "../jiant/data/" + name + "/test.jsonl"

    with open(file_path, 'r') as json_file:
        json_list = list(json_file)

    for json_str in json_list:
        result = json.loads(json_str)
        
        #print(isinstance(result, dict))
    keys.add(tuple(result.keys()))
    print(result.keys())
    print(len(keys))
