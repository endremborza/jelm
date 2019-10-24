from typing import Optional


class Edge:
    """jelm edge class

    - must have a source and a target
    - might have an id
    - can have arbitrary json serializable attributes
    """

    def __init__(self,
                 source: str,
                 target: str,
                 id: Optional[str] = None,
                 attributes: Optional[dict] = None):

        self.source = source
        self.target = target
        self.id = id
        self.attributes = attributes or {}

    def get_dict(self) -> dict:
        optionals = {
            k: self.__getattribute__(k)
            for k in ['id', 'attributes'] if self.__getattribute__(k)
        }
        return {
            'type': 'edge',
            'source': self.source,
            'target': self.target,
            **optionals
        }

    def __str__(self):

        return "::jelm Edge connecting {} to {}{}::".format(self.source,
                                                            self.target,
                                                            " (id: {})".format(self.id) if self.id else "")

    def __repr__(self):

        return self.__str__()
