import json

from jelm.core.jelm_class import Jelm


def reads_json(dump: str) -> Jelm:
    """turns a json string dump to a jelm graph"""

    return Jelm(**json.loads(dump))


def read_json(file_path: str) -> Jelm:
    """reads from a json file path"""

    with open(file_path) as fp:
        dump = fp.read()

    return reads_json(dump)
