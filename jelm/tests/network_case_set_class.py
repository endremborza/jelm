from jelm import Jelm

from typing import Callable, Optional, Type


class NetwokCaseTemplate:  # make this to a fixture

    el1 = Jelm()
    el2 = Jelm()
    same = True

    def evaluate_fun(
        self,
        non_altering_function: Optional[Callable] = None,
        altering_function: Optional[Callable] = None,
        assert_alteration: Optional[Callable] = None,
        catch_alteration_exception: Optional[Callable] = None,
    ):

        el_in = self.el1.copy()

        if altering_function is not None:
            try:
                el_out = altering_function(el_in)

            except Exception as e:
                if catch_alteration_exception is None:
                    raise e  # pragma: no cover
                else:
                    catch_alteration_exception(el_in, e)
            else:
                assert el_out != self.el1
                assert_alteration(el_out)

        if non_altering_function is not None:
            el_out = non_altering_function(el_in)
            assert el_out == self.el1
            assert (el_out == self.el2) == self.same

    def __repr__(self):
        return "Network pair case: {}".format(type(self).__name__)  # pragma: no cover


class NetworkCaseSet:
    def __init__(self):

        self.cases = []

    def register(self, network_case: Type[NetwokCaseTemplate]):

        self.cases.append(network_case())
        return network_case

    def __iter__(self):

        for case in self.cases:
            yield case


case_set = NetworkCaseSet()
