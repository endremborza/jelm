from typing import Optional


class Node:

    def __init__(self,
                 id: str,
                 attributes: Optional[dict] = None):
        self.id = id
        self.attributes = attributes or {}

    def get_dict(self) -> dict:
        if self.attributes:
            optionals = {'attributes': self.attributes}
        else:
            optionals = {}
        return {
            'type': 'node',
            'id': self.id,
            **optionals
        }