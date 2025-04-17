from src.threepio.lockfile import hash_key_value_pair


def retrieve_nom_source_keys(key_value_hashes: set[str], source_dict: dict[str, str]):
    "nom stands for new or modified"
    nom_keys = set()
    for k, v in source_dict.items():
        _hash = hash_key_value_pair(k, v)
        if _hash not in key_value_hashes:
            nom_keys.add(k)

    return nom_keys
