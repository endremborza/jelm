from jelm import Jelm

from jelm.tests.network_case_set_class import NetwokCaseTemplate


def test_neighborhood():

    el1 = Jelm(metadata={"fing": "boo"}, objects=[{"type": "node", "id": "n1"}])

    el2 = el1.get_neighborhood([])

    assert el2 != el1

    assert el2 == Jelm(metadata={"fing": "boo"})

    assert el1 == el1.get_neighborhood(["n1", "n2"], raise_if_missing=False)


def test_neighborhood_w_cases(jelm_pair_case: NetwokCaseTemplate):
    def get_whole_graph(el: Jelm):

        return el.get_neighborhood(el.nodes.keys())

    jelm_pair_case.evaluate_fun(non_altering_function=get_whole_graph)

    def check_drop(el: Jelm):

        nel = el.get_neighborhood(["n1", "n2"])

    # jelm_pair_case.evaluate_fun(catch_alteration_exception=)
