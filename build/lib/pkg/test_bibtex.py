"Bibtex pytest file."
from pkg import Works

REF = """@ARTICLE{Kitchin2015,
            author =	 {John R. Kitchin},
            title =	 {Examples of Effective Data Sharing in Scientific Publishing},
            journal =	 {ACS Catalysis},
            volume =	 {5},
            number =	 {6},
            pages =	 {3894-3899},
            year =	 {2015},
            doi =		 {10.1021/acscatal.5b00538},
            url =		 {https://doi.org/10.1021/acscatal.5b00538},
            } """


def test_bibtex():
    "Function for assert."
    works = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert REF == works.bibtex
