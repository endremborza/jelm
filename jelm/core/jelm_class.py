import json

from .edge_class import Edge
from .node_class import Node

from typing import Optional, Union


class Jelm:

    def __init__(self,
                 metadata: Optional[dict]=None,
                 objects: Optional[list]=None,
                 **kwargs):

        self.metadata = metadata or {}
        self.objects = []

        self.nodes = {}
        for o in objects or []:
            self.add_object(o)

        if kwargs:
            raise ValueError("Tried to create jelm object with additional kwargs {}"
                             .format(kwargs.keys()))

    def dict(self) -> dict:
        return {
            'metadata': self.metadata,
            'objects': [o.get_dict() for o in self.objects]
        }

    def json_dumps(self) -> str:
        return json.dumps(self.dict())

    def json_dump(self, fp) -> None:
        try:
            json.dump(self.dict(),
                      fp)
        except AttributeError:
            if isinstance(fp, str):
                json.dump(self.dict(),
                          open(fp, 'w'))
            else:
                raise TypeError("""either pass something with a .write() method, 
                or a string pointing to a valid path to Jelm.json_dump""")

    def add_object(self, obj: Union[dict, Edge, Node]):

        if isinstance(obj, dict):
            jelm_kwargs = obj.copy()
            try:
                obj_type = jelm_kwargs.pop('type')
            except KeyError:
                raise ValueError("if dict is given, 'type' key needs to be set! (to either node or edge)")

            is_node = False
            if obj_type == 'edge':
                parsed_obj = Edge(**jelm_kwargs)
            elif obj_type == 'node':
                parsed_obj = Node(**jelm_kwargs)
                is_node = True
            else:
                raise ValueError("object type needs to be either node or edge it is {}".format(obj_type))
        else:
            parsed_obj = obj
            is_node = isinstance(parsed_obj,
                                 Node)

        if is_node:

            if parsed_obj.id not in self.nodes.keys():
                self.nodes[parsed_obj.id] = parsed_obj
            else:
                raise ValueError("node with id {} already present".format(parsed_obj.id))

        self.objects.append(parsed_obj)

    def add_edge(self,
                 source: str,
                 target: str,
                 id: Optional[str] = None,
                 attributes: Optional[dict] = None):

        parsed_obj = Edge(source,
                          target,
                          id,
                          attributes)

        self.add_object(parsed_obj)

    def add_node(self,
                 id: str,
                 attributes: Optional[dict] = None):

        parsed_obj = Node(id, attributes)

        self.add_object(parsed_obj)

    def __iter__(self) -> Union[Edge, Node]:

        for o in self.objects:

            yield o
