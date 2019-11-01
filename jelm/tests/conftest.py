from .network_cases import case_set


def pytest_generate_tests(metafunc):
    if "jelm_pair_case" in metafunc.fixturenames:
        metafunc.parametrize("jelm_pair_case", case_set)
