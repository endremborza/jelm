import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jelm import Jelm  # pragma: no cover


def json_dumps(el: "Jelm") -> str:
    return json.dumps(el.dict())


def json_dump(el: "Jelm", fp) -> None:
    try:
        json.dump(el.dict(), fp)
    except AttributeError:
        if isinstance(fp, str):
            json.dump(el.dict(), open(fp, "w"))
        else:
            raise TypeError(
                """either pass something with a .write() method, 
            or a string pointing to a valid path to Jelm.json_dump"""
            )
