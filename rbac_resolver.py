def get_role_rules(binding, roles):
    if "roleRefKind" not in binding:
        return []
    
    roleRefKind = binding["roleRefKind"]

    if "roleRefName" not in binding:
        return []
    
    roleRefName = binding["roleRefName"]

    result = []

    for role in roles:
        if role["kind"] == roleRefKind and role["role"] == roleRefName:
            result.append(role)

    return result

def resolve_binding(binding, roles):
    matched_rules = get_role_rules(binding, roles)
    
    result = []

    subjects = binding["subjects"] if "subjects" in binding else []

    namespace = "default" if "namespace" not in binding else binding["namespace"]

    for subject in subjects:
        result.append(
            {
                "subject": subject,
                "namespace": namespace,
                "rules": matched_rules
            }
        )
    
    return result

def resolve_permissions(bindings, roles):

    result = {}
    namespaces = {}

    for binding in bindings:
        resolved_binding = resolve_binding(binding, roles)

        for i in resolved_binding:
            subject = i["subject"]
            namespace = i["namespace"]
            rules = i["rules"]

            if subject["kind"] == "ServiceAccount":
                subject_id = \
                    subject["kind"] + ":" \
                    + subject["namespace"] + ":" \
                    + subject["name"]
            else:
                subject_id = \
                subject["kind"] + ":" \
                + subject["name"]

            if subject_id not in result:
                result[subject_id] = []

            for rule in rules:
                result[subject_id].append({
                    "namespace": namespace,
                    "rule": rule
                })

    return result