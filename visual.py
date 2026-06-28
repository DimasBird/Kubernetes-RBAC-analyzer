import json

def return_fast_result(args, result: dict):

    only_dangerous_flag = args.only_dangerous

    fast_result = []

    for sign in result.keys():

        for rule in result[sign]:

            matched_len = len(rule["matched"])

            if matched_len == 0 and only_dangerous_flag:
                continue
                
            cat = "@safe: " if matched_len == 0 else "!not safe: "

            scope = "  scope ---> " + rule["scope"]

            role = "  " + rule["kind"] + ":" + rule["role"]

            apiGroups = "  apiGroups: " + str(rule["apiGroups"])
            resources = "  resources: " + str(rule["resources"])
            verbs = "  verbs:     " + str(rule["verbs"])

            matched = "" if matched_len == 0 else f"\n  {rule['matched']}"

            fast_result.append(cat + sign + "\n" \
                                + scope + "\n"    \
                                + role + "\n"      \
                                + apiGroups + "\n" \
                                + resources + "\n" \
                                + verbs \
                                + matched)
                
    return "\n\n".join(fast_result) + "\n"

def return_json_result(args, result):
    
    only_dangerous_flag = args.only_dangerous

    if not only_dangerous_flag:
        return json.dumps(result, indent=4)
    
    json_result = {}

    for sign in result.keys():

        for rule in result[sign]:

            matched_len = len(rule["matched"])

            if matched_len == 0:
                continue

            if sign not in json_result:
                json_result[sign] = [rule]

            else:
                json_result[sign].append(rule)

    json_result = json.dumps(json_result, indent=4)

    return json_result