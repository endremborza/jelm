from .network_cases import case_set


def pytest_addoption(parser):
    parser.addoption("--big", action="store_true", help="run all combinations")


def pytest_generate_tests(metafunc):
    if "jelm_pair_case" in metafunc.fixturenames:

        #if metafunc.config.getoption("big"):
        #    from .network_cases import BiggerNetRef

        #    case_set.cases.append(BiggerNetRef(node_count=2000,
        #                                       edge_count=5000))

        metafunc.parametrize("jelm_pair_case", case_set)
