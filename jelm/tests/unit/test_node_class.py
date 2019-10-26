import pytest

from jelm import Node, Edge


def test_node_repr():

    n = Node('n1')

    assert 'n1' in n.__repr__()


def test_add_edge():

    n = Node(id='n1')

    n.add_edge(Edge(source='n1',
                    target='n2'))

    assert 'n2' in n.neighbors.keys()
    assert 'n2' in n.target_neighbors.keys()

    with pytest.raises(ValueError):

        n.add_edge(Edge(source='n3',
                        target='n4'))
