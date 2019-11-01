import pytest

from jelm import Jelm, Node, Edge

from jelm.tests.network_case_set_class import NetwokCaseTemplate


def test_eq(jelm_pair_case: NetwokCaseTemplate):

    jelm_pair_case.evaluate_fun(non_altering_function=lambda x: x)

    assert not (10 == Jelm())
    assert not ("fing" == Jelm())


def test_jelm_repr(jelm_pair_case: NetwokCaseTemplate):
    def repr_check(el: Jelm):

        repr_string = el.__repr__()

        assert "jelm" in repr_string
        assert str(len(el.nodes.keys())) in repr_string

        return el

    jelm_pair_case.evaluate_fun(non_altering_function=repr_check)


def test_neighbors(jelm_pair_case: NetwokCaseTemplate):
    def neighbor_check(el: Jelm):

        for nid, n in el.nodes.items():

            for nid2 in n.neighbors.keys():

                assert nid in el.get_node(nid2).neighbors.keys()

            for nid3 in n.target_neighbors.keys():

                assert nid in el.get_node(nid3).source_neighbors.keys()

        return el

    jelm_pair_case.evaluate_fun(non_altering_function=neighbor_check)


def test_add_node_as_object_w_cases(jelm_pair_case: NetwokCaseTemplate):
    def add_node_as_obj(el: Jelm):

        el.add_object({"type": "node", "id": "n10"})
        return el

    def assert_node_as_obj_added(el: Jelm):
        assert isinstance(el.get_node("n10"), Node)

    def catch_node_as_obj_add(el: Jelm, e):

        assert isinstance(e, ValueError)
        assert isinstance(el.get_node("n10"), Node)

    jelm_pair_case.evaluate_fun(
        altering_function=add_node_as_obj,
        assert_alteration=assert_node_as_obj_added,
        catch_alteration_exception=catch_node_as_obj_add,
    )


def test_add_edge_as_object_w_cases(jelm_pair_case: NetwokCaseTemplate):
    def add_edge_as_obj(el: Jelm):

        el.add_object({"type": "edge", "source": "n1", "target": "n2"})
        return el

    def assert_edge_as_obj_added(el: Jelm):

        n = el.get_node("n1")

        assert "n2" in n.neighbors.keys()
        assert "n1" in el.get_node("n2").neighbors
        assert "n2" in n.target_neighbors.keys()

    def catch_edge_as_obj_add(el: Jelm, e):

        assert isinstance(e, KeyError)

        assert ("n1" not in el.nodes.keys()) or ("n2" not in el.nodes.keys())

    jelm_pair_case.evaluate_fun(
        altering_function=add_edge_as_obj,
        assert_alteration=assert_edge_as_obj_added,
        catch_alteration_exception=catch_edge_as_obj_add,
    )


def test_add_edge_jelm_object_w_cases(jelm_pair_case: NetwokCaseTemplate):
    def add_edge_jelm_obj(el: Jelm):

        el.add_object(Edge(source="n1", target="n2", id="fing"))
        return el

    def assert_edge_jelm_obj_added(el: Jelm):

        n = el.get_node("n1")

        assert "n2" in n.neighbors.keys()
        assert "n1" in el.get_node("n2").neighbors
        assert "n2" in n.target_neighbors.keys()

        edge_ids = [e.id for e in n.neighbors["n2"]]

        assert "fing" in edge_ids

    def catch_edge_jelm_obj_add(el: Jelm, e):

        assert isinstance(e, KeyError)

        assert ("n1" not in el.nodes.keys()) or ("n2" not in el.nodes.keys())

    jelm_pair_case.evaluate_fun(
        altering_function=add_edge_jelm_obj,
        assert_alteration=assert_edge_jelm_obj_added,
        catch_alteration_exception=catch_edge_jelm_obj_add,
    )


def test_init():

    el = Jelm(metadata={"author": "John Doe"}, objects=[])

    with pytest.raises(ValueError):
        el2 = Jelm(bad_kwarg="fing")

    assert isinstance(el.objects, list)
    assert isinstance(el.metadata, dict)


def test_add_object():

    el = Jelm()

    el.add_object({"type": "node", "id": "n1"})

    el.add_object(Node(id="n2"))

    el.add_object({"type": "edge", "source": "n1", "target": "n2"})

    el.add_object(Node(id="n3", attributes={"priority": "low"}))

    with pytest.raises(ValueError):
        el.add_object({"no": "type"})

    with pytest.raises(ValueError):
        el.add_object({"type": "wrong"})

    with pytest.raises(ValueError):
        el.add_object(10)

    el.add_edge("n3", "n2")

    el.add_node("n4", {"order": "latest"})

    assert len(set([type(o) for o in el.objects])) > 1
    assert isinstance(el.objects[0], Node)
    assert isinstance(el.objects[2], Edge)


def test_iter():

    el = Jelm(
        metadata={"author": "John Doe"},
        objects=[
            {"type": "node", "id": "n1"},
            {"type": "node", "id": "n2"},
            {"type": "edge", "source": "n1", "target": "n2"},
        ],
    )

    for idx, o in enumerate(el):
        if idx < 2:
            assert isinstance(o, Node)
        else:
            assert isinstance(o, Edge)
