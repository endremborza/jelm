import json

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .edge_class import Edge  # pragma: no cover


class Node:
    """node class for jelm graphs

    - stores neighbors indexed locally
    - must have an id
    - can have arbitrary json serializable attributes
    """

    def __init__(
        self,
        id: str,
        attributes: Optional[dict] = None,
        source_neighbors: Optional[dict] = None,
        target_neighbors: Optional[dict] = None,
    ):
        self.id = id
        self.attributes = attributes or {}
        self.target_neighbors = target_neighbors or {}
        self.source_neighbors = source_neighbors or {}
        self.neighbors = {
            n: self.target_neighbors.get(n, []) + self.source_neighbors.get(n, [])
            for n in self.target_neighbors.keys() | self.source_neighbors.keys()
        }

    from .transformations.filters import restrict_to_neighborhood

    def get_dict(self) -> dict:
        if self.attributes:
            optionals = {"attributes": self.attributes}
        else:
            optionals = {}
        return {"type": "node", "id": self.id, **optionals}

    def add_edge(self, e: "Edge"):

        if e.source == self.id:
            neighbor_id = e.target
            relevant_dict = self.target_neighbors
        elif e.target == self.id:
            neighbor_id = e.source
            relevant_dict = self.source_neighbors
        else:
            raise ValueError(
                "Trying to add an edge to node {} whose ends are source: {} target: {}".format(
                    self.id, e.source, e.target
                )
            )

        for d in [relevant_dict, self.neighbors]:

            try:
                d[neighbor_id].append(e)
            except KeyError:
                d[neighbor_id] = [e]

    def _comparison_neighbors(self, way: str):

        if way == "in":
            edge_dic = self.source_neighbors
        else:
            edge_dic = self.target_neighbors

        return {
            n: sorted([json.dumps(e.get_dict(), sort_keys=True, indent=0) for e in el])
            for n, el in edge_dic.items()
        }

    def get_inward_comparison_neighbors(self):
        return self._comparison_neighbors("in")

    def get_outward_comparison_neighbors(self):
        return self._comparison_neighbors("out")

    def __str__(self):

        n = len(self.neighbors.keys())
        return "::jelm Node ({}) with {} neighbor{}::".format(
            self.id, n, "" if n == 1 else "s"
        )

    def __repr__(self):

        return self.__str__()
