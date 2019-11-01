from jelm.core.edge_class import Edge


def test_edge_repr():

    e1 = Edge(source="n1", target="n2")

    rep_string = e1.__repr__()

    assert e1.source in rep_string
    assert e1.target in rep_string

    e2 = Edge(source="n0", target="n1", id="e0")

    assert e2.id in e2.__repr__()
