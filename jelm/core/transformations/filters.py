from jelm.utils import dict_subset

from typing import TYPE_CHECKING, Iterable, Callable

if TYPE_CHECKING:
    from jelm import Node, Jelm  # pragma: no cover


def restrict_to_neighborhood(n: "Node", node_set: Iterable):

    node_klass = type(n)

    return node_klass(
        id=n.id,
        attributes=n.attributes,
        source_neighbors=dict_subset(n.source_neighbors, node_set),
        target_neighbors=dict_subset(n.target_neighbors, node_set),
    )


def attribute_filter(el: "Jelm", filter_function: Callable[[dict], bool]):
    jelm_klass = type(el)

    return jelm_klass(
        metadata=el.metadata,
        objects=[o for o in el.objects if filter_function(o.attributes)],
    )
