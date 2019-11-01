from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from jelm import Jelm  # pragma: no cover


def get_neighborhood(
    el: "Jelm", node_set: Iterable, raise_if_missing: bool = True
) -> "Jelm":
    """restrict a network to a set of nodes

    this returns a new Jelm object, that is restricted to
    the set of nodes given"""

    if raise_if_missing:
        new_full_dic = {n: el.nodes[n] for n in node_set}
    else:
        new_full_dic = {n: el.nodes[n] for n in node_set if n in el.nodes.keys()}

    new_node_dict = {
        n.id: n.restrict_to_neighborhood(new_full_dic.keys())
        for n in new_full_dic.values()
    }

    jelm_klass = type(el)

    return jelm_klass(metadata=el.metadata, nodes=new_node_dict)
