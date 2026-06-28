def parse_bindings(yaml_docs):
    result = []

    for doc in yaml_docs:
        if not doc:
            continue
            
        binding = parse_binding(doc)

        if binding:
            result.append(binding)
    
    return result

def parse_binding(yaml_doc):
    if "kind" not in yaml_doc:
        return None
    
    kind = yaml_doc["kind"]

    if kind not in ["RoleBinding", "ClusterRoleBinding"]:
        return None
    
    if "metadata" not in yaml_doc:
        return None
    
    metadata = yaml_doc["metadata"]

    binding_name = "*no_name*" \
        if "name" not in metadata \
        else metadata["name"]
    
    if kind == "RoleBinding":
        binding_namespace = "default" \
            if "namespace" not in metadata \
            else metadata["namespace"]
    else:
        binding_namespace = None

    role_ref = {} if "roleRef" not in yaml_doc else yaml_doc["roleRef"]

    role_kind = "*no_role_kind*" \
        if "kind" not in role_ref \
        else role_ref["kind"]

    role_name = "*no_role_name*" \
        if "name" not in role_ref \
        else role_ref["name"]
    
    subjects = [] \
        if "subjects" not in yaml_doc \
        else parse_subjects(yaml_doc["subjects"])
    
    result = dict()

    result["kind"] = kind
    result["name"] = binding_name
    result["namespace"] = binding_namespace

    result["roleRefKind"] = role_kind
    result["roleRefName"] = role_name

    result["subjects"] = subjects

    return result


def parse_subjects(subjects_yaml) -> list:
    result = []

    for subject in subjects_yaml:
        res = dict()

        res["kind"] = (
            "*no_kind*"
            if "kind" not in subject
            else subject["kind"]
        )

        res["name"] = \
            "*no_name*" \
            if "name" not in subject \
            else subject["name"]
        

        if res["kind"] == "ServiceAccount":
            res["namespace"] = \
                "default" \
                if "namespace" not in subject \
                else subject["namespace"]
            
        else:
            res["namespace"] = None

        result.append(res)

    return result

def parse_roles(yaml_docs) -> list:
    res = []
    for doc in yaml_docs:
        if not doc:
            continue
        rules = parse_role(doc)
        res.extend(rules)       # Добавление содержимого в список

    return res

def parse_role(yaml_doc : dict) -> list:
    if "kind" not in yaml_doc:
        return []

    kind = yaml_doc["kind"]

    if kind not in ["Role", "ClusterRole"]:
        return []
    
    if "metadata" not in yaml_doc:
        return []
    
    metadata = yaml_doc["metadata"]

    role_name = "*no_role_name*" if "name" not in metadata else metadata["name"]

    if kind == "Role":
        role_namespace = "default" if "namespace" not in yaml_doc["metadata"] \
            else yaml_doc["metadata"]["namespace"]
    else:
        role_namespace = None

    rules = [] if "rules" not in yaml_doc else yaml_doc["rules"]

    result = []

    for rule in rules:
        verbs = [] if "verbs" not in rule else rule["verbs"]
        resources = [] if "resources" not in rule else rule["resources"]
        api_groups = [] if "apiGroups" not in rule else rule["apiGroups"]

        res = dict()

        res["kind"] = kind
        res["role"] = role_name
        res["namespace"] = role_namespace
        res["verbs"] = verbs
        res["resources"] = resources
        res["apiGroups"] = api_groups

        result.append(res)

    return result