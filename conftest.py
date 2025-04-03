import pytest


# Registrujemo markere kako bi izbegli pytest upozorenja
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "sensitive: testovi koji zahtevaju visoku preciznost"
    )
    config.addinivalue_line(
        "markers",
        "golden: testovi protiv referentnih vrednosti"
    )
    config.addinivalue_line(
        "markers",
        "edge: testovi graničnih slučajeva"
    )


# Fixture za zajedničke podatke
@pytest.fixture
def standard_loan():
    return {
        'principal': 100000,
        'rate': 5.0,
        'term': 120
    }
