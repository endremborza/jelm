from copy import deepcopy

from .edge_class import Edge
from .node_class import Node

from typing import Optional, Union, Dict


class Jelm:
    """jelm graph class

    - stores and serializes a jelm graph
    - has accessors for simple graph operations
    - a lot of data is stored redundantly for speedups
    """

    def __init__(
        self,
        metadata: Optional[dict] = None,
        objects: Optional[list] = None,
        nodes: Optional[Dict[str, Node]] = None,
    ):

        self.metadata = metadata or {}
        self.objects = []
        self.edges = []
        self.nodes = {}
        for n in (nodes or {}).values():
            self.add_node_jelmobject(n, strip_edges=False)

            for conns in n.target_neighbors.values():
                self.objects += conns

        for o in objects or []:
            self.add_object(o)

    def dict(self) -> dict:
        return {
            "metadata": self.metadata,
            "objects": [o.get_dict() for o in self.objects],
        }

    from .io.output import json_dumps, json_dump
    from .transformations.neighborhoods import get_neighborhood
    from .transformations.filters import attribute_filter

    def add_object(self, obj: Union[dict, Edge, Node]):

        if isinstance(obj, dict):
            jelm_kwargs = obj.copy()
            try:
                obj_type = jelm_kwargs.pop("type")
            except KeyError:
                raise ValueError(
                    "if dict is given, 'type' key needs to be set! (to either node or edge)"
                )

            if obj_type == "edge":
                parsed_obj = Edge(**jelm_kwargs)
                self.add_edge_jelmobject(parsed_obj)
            elif obj_type == "node":
                parsed_obj = Node(**jelm_kwargs)
                self.add_node_jelmobject(parsed_obj)
            else:
                raise ValueError(
                    "object type needs to be either node or edge it is {}".format(
                        obj_type
                    )
                )
        elif isinstance(obj, Edge):
            self.add_edge_jelmobject(obj)
        elif isinstance(obj, Node):
            self.add_node_jelmobject(obj)
        else:
            raise ValueError(
                "add_object takes either dict, Edge or Node, {} was given".format(
                    type(obj)
                )
            )

    def add_edge(
        self,
        source: str,
        target: str,
        id: Optional[str] = None,
        attributes: Optional[dict] = None,
    ):

        parsed_obj = Edge(source, target, id, attributes)

        self.add_edge_jelmobject(parsed_obj)

    def add_node(self, id: str, attributes: Optional[dict] = None):

        parsed_obj = Node(id, attributes)

        self.add_node_jelmobject(parsed_obj)

    def add_edge_jelmobject(self, edge: Edge):

        self.get_node(edge.source).add_edge(edge)
        self.get_node(edge.target).add_edge(edge)  # TODO: this might mess up loop-edges

        self.objects.append(edge)
        self.edges.append(edge)

    def add_node_jelmobject(self, node: Node, strip_edges: bool = True):

        if strip_edges:
            _node = Node(id=node.id, attributes=node.attributes)
        else:
            _node = node

        if node.id not in self.nodes.keys():
            self.nodes[node.id] = _node

        else:
            raise ValueError("node with id {} already present".format(node.id))

        self.objects.append(_node)

    def get_node(self, node_id: str) -> Node:

        return self.nodes[node_id]

    def get_comparison_dict(self):

        node_comp_dic = {
            nid: {
                "in": node.get_inward_comparison_neighbors(),
                "out": node.get_outward_comparison_neighbors(),
                "attributes": node.attributes,
            }
            for nid, node in self.nodes.items()
        }

        return {"metadata": self.metadata, "nodes": node_comp_dic}

    def copy(self):
        return self.__copy__()

    def __copy__(self):

        return type(self)(**deepcopy(self.dict()))

    def __iter__(self) -> Union[Edge, Node]:

        for o in self.objects:
            yield o

    def __eq__(self, other):

        if isinstance(other, type(self)):
            return self.get_comparison_dict() == other.get_comparison_dict()

        return False

    def __str__(self):

        nn = len(self.nodes.keys())
        en = len(self.objects) - nn

        return "::jelm Graph with {} node{} and {} edge{}::".format(
            nn, "" if nn == 1 else "s", en, "" if en == 1 else "s"
        )

    def __repr__(self):

        return self.__str__()
