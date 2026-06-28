def check_matches(a: set, b: set) -> bool:
    star_in_a = "*" in a
    star_in_b = "*" in b
    simple_collision = bool(set(a) & set(b))
    return star_in_a or star_in_b or simple_collision

def get_matches(a: set, b: set) -> list:
    if "*" in b: return ["*"]
    elif "*" in a: return list(b)
    else: return list(a & b)


def analyze_rule(unsafe_rules, rule):
    verbs_rule = set([] if "verbs" not in rule else rule["verbs"])
    resources_rule = set([] if "resources" not in rule else rule["resources"])
    apiGroups_rule = set([] if "apiGroups" not in rule else rule["apiGroups"])

    matched = []

    for unsafe_rule in [] if "unsafe_rules" not in unsafe_rules else unsafe_rules["unsafe_rules"]:

        unsafe = unsafe_rule["rule"]

        unsafe_verbs = [] if "verbs" not in unsafe else unsafe["verbs"]
        unsafe_resources = [] if "resources" not in unsafe else unsafe["resources"]
        unsafe_apiGroups = [] if "apiGroups" not in unsafe else unsafe["apiGroups"]

        verb_match_bool = check_matches(verbs_rule, unsafe_verbs)
        resources_match_bool = check_matches(resources_rule, unsafe_resources)
        apiGroups_match_bool = check_matches(apiGroups_rule, unsafe_apiGroups)

        if verb_match_bool and resources_match_bool and apiGroups_match_bool:
            matched.append(
                {
                    "unsafe_rule_name": unsafe_rule["name"],
                    "matched_verbs": get_matches(verbs_rule, set(unsafe_verbs)),
                    "matched_resources": get_matches(resources_rule, set(unsafe_resources)),
                    "matched_api_groups": get_matches(apiGroups_rule, set(unsafe_apiGroups))
                }
            )

    return matched
    
def check_rule(unsafe_rules, rule):
    matched = analyze_rule(unsafe_rules, rule["rule"])

    if rule["rule"]["kind"] == "ClusterRole":
        scope = "cluster"
    else:
        scope = rule["namespace"]

    return {
        "role": rule["rule"]["role"],
        "scope": scope,
        "kind": rule["rule"]["kind"],
        "apiGroups": rule["rule"].get("apiGroups", []),
        "resources": rule["rule"].get("resources", []),
        "verbs": rule["rule"].get("verbs", []),
        "matched": matched       # Может быть пуст
    }