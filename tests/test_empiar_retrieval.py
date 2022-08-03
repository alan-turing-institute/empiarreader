from intake_cryoem.empiar import EmpiarCatalog, EmpiarSource

def test_empiar():
    cat = EmpiarCatalog(10340)

    assert "Unaligned movies for Case 1" in cat.keys()

    ds = cat["Unaligned movies for Case 1"]

    assert isinstance(ds, EmpiarSource)

    assert ds.directory == "data/Movies/Case1"

    # Note: ds.read() is expensive
