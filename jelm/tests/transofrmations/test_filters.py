from jelm import Jelm

from jelm.tests.network_case_set_class import NetwokCaseTemplate


def test_attribute_filter_w_cases(jelm_pair_case: NetwokCaseTemplate):
    def filter_none(el: Jelm):

        el2 = el.attribute_filter(lambda x: True)
        print(el)
        print(el2)
        print(el == el2)
        return el2

    jelm_pair_case.evaluate_fun(non_altering_function=filter_none)


def test_attribute_filter2(jelm_pair_case: NetwokCaseTemplate):
    def filter_none(el: Jelm):

        el.attribute_filter(lambda x: True)
        return el

    jelm_pair_case.evaluate_fun(non_altering_function=filter_none)


def test_attribute_filter():
    node_list1 = [{"type": "node", "id": "n{}".format(i)} for i in range(1, 4)]

    edge_list1 = [
        {
            "type": "edge",
            "source": "n1",
            "target": "n2",
            "attributes": {"good_edge": True},
        },
        {
            "type": "edge",
            "source": "n1",
            "target": "n3",
            "attributes": {"good_edge": False},
        },
        {
            "type": "edge",
            "source": "n2",
            "target": "n3",
            "attributes": {"good_edge": False},
        },
    ]

    el1 = Jelm(objects=[*node_list1, *edge_list1])

    def filter_fun(atts):

        is_good_edge = atts.get("good_edge")

        if is_good_edge is None:
            return True

        return is_good_edge

    expected_el = Jelm(
        objects=[
            {"type": "node", "id": "n1"},
            {"type": "node", "id": "n2"},
            {"type": "node", "id": "n3"},
            {
                "type": "edge",
                "source": "n1",
                "target": "n2",
                "attributes": {"good_edge": True},
            },
        ]
    )

    assert expected_el == el1.attribute_filter(filter_fun)
