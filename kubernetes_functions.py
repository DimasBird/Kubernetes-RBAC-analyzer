from kubernetes import client

def load_kubernetes_manifests() -> dict:
    v1_rbac = client.RbacAuthorizationV1Api()
    v1 = client.CoreV1Api()

    roles = v1_rbac.list_role_for_all_namespaces()
    cluster_roles = v1_rbac.list_cluster_role()
    service_accounts = v1.list_service_account_for_all_namespaces()

    bindings = v1_rbac.list_role_binding_for_all_namespaces()
    cluster_bindings = v1_rbac.list_cluster_role_binding()

    return {
        "roles": roles,
        "cluster_roles": cluster_roles,
        "service_accounts": service_accounts,
        "bindings": bindings,
        "cluster_bindings": cluster_bindings
    }

# Преобразование ролей к общему формату
def convert_roles(manifests_dict: dict):
    result = []

    for role in manifests_dict["roles"].items:
        for rule in role.rules:
            verbs = [] if rule.verbs is None else list(rule.verbs)
            resources = [] if rule.resources is None else list(rule.resources)
            api_groups = [] if rule.api_groups is None else list(rule.api_groups)

            result.append({
                "kind": "Role",
                "role": role.metadata.name,
                "namespace": role.metadata.namespace,
                "verbs": verbs,
                "resources": resources,
                "apiGroups": api_groups
            })

    for role in manifests_dict["cluster_roles"].items:
        for rule in role.rules:
            verbs = [] if rule.verbs is None else list(rule.verbs)
            resources = [] if rule.resources is None else list(rule.resources)
            api_groups = [] if rule.api_groups is None else list(rule.api_groups)

            result.append({
                "kind": "ClusterRole",
                "role": role.metadata.name,
                "namespace": "cluster",
                "verbs": verbs,
                "resources": resources,
                "apiGroups": api_groups
            })
    
    return result

# Преобразование привязок ролей к общему формату
def convert_bindings(manifest_dict: dict):
    result = []

    for b in manifest_dict["bindings"].items:
        namespace = b.metadata.namespace

        role_ref = b.role_ref

        l = [] if b.subjects == None else b.subjects

        for subject in l:
            result.append({
                "kind": "RoleBinding",
                "name": b.metadata.name,
                "namespace": b.metadata.namespace,

                "roleRefKind": role_ref.kind if role_ref else None,
                "roleRefName": role_ref.name if role_ref else None,

                "subjects": [{
                    "kind": subject.kind,
                    "name": subject.name,
                    "namespace": subject.namespace if subject.kind == "ServiceAccount" else None
                }
                for subject in l]
            })

    for b in manifest_dict["cluster_bindings"].items:
        namespace = b.metadata.namespace

        role_ref = b.role_ref

        l = [] if b.subjects == None else b.subjects

        result.append({
            "kind": "ClusterRoleBinding",
            "name": b.metadata.name,
            "namespace": None,

            "roleRefKind": role_ref.kind if role_ref else None,
            "roleRefName": role_ref.name if role_ref else None,

            "subjects": [{
                "kind": subject.kind,
                "name": subject.name,
                "namespace": subject.namespace if subject.kind == "ServiceAccount" else None
            }
            for subject in l]
        })

    return result