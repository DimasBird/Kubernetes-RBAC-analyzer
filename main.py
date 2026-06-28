import argparse
from yaml_analyzer import load_unsafe_rules, load_manifests
from parser import parse_roles, parse_bindings
from rbac_resolver import resolve_permissions
from rule_analyzer import check_rule
from visual import return_fast_result, return_json_result
from saver import send_report
from kubernetes import client, config
from kubernetes_functions import load_kubernetes_manifests, convert_roles, convert_bindings

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
                    prog='RBAC analyzer',
                    description='Analyzes RBAC roles and rules')
    
    subparser = parser.add_subparsers(dest="command", required=True)

    # Добавляем вариант манифестного управления
    analyze_manifest = subparser.add_parser("manifests")

    # Добавляем параметры для манифестного управления
    analyze_manifest.add_argument("--paths", nargs="+")
    analyze_manifest.add_argument("--unsafe-rules", required=False, default="configs/unsafe_rules.yaml")
    analyze_manifest.add_argument("--only-dangerous", required=False, action="store_true")
    analyze_manifest.add_argument("--json", required=False, action="store_true")
    analyze_manifest.add_argument("--save", required=False, default=False, action="store_true")

    # Добавляем вариант получения манифестов из API
    analyze_k8s = subparser.add_parser("k8s")

    # Добавляем параметры для манифестного управления
    analyze_k8s.add_argument("--unsafe-rules", required=False, default="configs/unsafe_rules.yaml")
    analyze_k8s.add_argument("--only-dangerous", required=False, action="store_true")
    analyze_k8s.add_argument("--json", required=False, action="store_true")
    analyze_k8s.add_argument("--save", required=False, default=False, action="store_true")

    return parser


def analyze(args, bindings, roles):
    unsafe_rules = load_unsafe_rules(args.unsafe_rules)  # Загрузка небезопасных правил

    permission = resolve_permissions(bindings, roles)

    result = {}

    for subject, rules in permission.items():

        subject_matches = []

        for rule in rules:
            match = check_rule(unsafe_rules, rule)

            if match:
                subject_matches.append(match)
        
        result[subject] = subject_matches
    
    return result


def analyze_manifests(args):
    docs = load_manifests(args.paths)

    roles = parse_roles(docs)        # Внутри доки разделятся на роли и привязки
    bindings = parse_bindings(docs)

    result = analyze(args, bindings, roles)

    return result
        

def analyze_kubernetes(args):
    config.load_kube_config()

    manifests = load_kubernetes_manifests()

    roles = convert_roles(manifests)
    bindings = convert_bindings(manifests)

    result = analyze(args, bindings, roles)

    return result


def return_report(args, result):
    use_json = args.json

    if not use_json:
        return return_fast_result(args, result)
    else:
        return return_json_result(args, result)


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "manifests":
        result = analyze_manifests(args)
        report = return_report(args, result)
        send_report(args, report)

    elif args.command == "k8s":
        result = analyze_kubernetes(args)
        report = return_report(args, result)
        send_report(args, report)

    else:
        print(f"{args.command} is unknown")