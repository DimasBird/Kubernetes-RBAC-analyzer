import yaml
from pathlib import Path

def get_yaml(filename: str):
    with open(filename, 'r') as file:
        config = yaml.safe_load_all(file)
        return list(config)

def load_unsafe_rules(unsafe_rules_file):
    with open(unsafe_rules_file, "r") as file:
        docs = list(yaml.safe_load_all(file))
        return docs[0] if docs else {}     # Загрузка небезопасных правил из конфига
    
def load_manifests(paths) -> list:
    res = []

    for str_path in paths:
        path = Path(str_path)

        if path.is_file():               # Если это файл
            for doc in get_yaml(path):
                if doc is not None:
                    res.append(doc)
        elif path.is_dir():                                 # Если это папка
            for file in path.rglob("*.yaml"):
                for doc in get_yaml(file):
                    if doc is not None:
                        res.append(doc)
            for file in path.rglob("*.yml"):
                for doc in get_yaml(file):
                    if doc is not None:
                        res.append(doc)

        else:
            print(f"{str_path} was not found")

    return res