from pkg import Works

ref_bibtex = "[('url', 'https://doi.org/10.1021/acscatal.5b00538'), ('doi', '10.1021/acscatal.5b00538'), ('year', '2015'), ('pages', '3894-3899'), ('number', '6'), ('volume', '5'), ('journal', 'ACS Catalysis'), ('title', 'Examples of Effective Data Sharing in Scientific Publishing'), ('author', 'John R. Kitchin'), ('ENTRYTYPE', 'article'), ('ID', 'https://openalex.org/W2288114809')]"


def test_bibtex():
    w = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert ref_bibtex == w.bibtex