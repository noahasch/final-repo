"""This file formats OpenAlex papers in either a RIS or Bibtex format."""
import requests


class Works:
    "This is a paper formatting class."

    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        return "str"

    def __repr__(self):
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]
        volume = self.data["biblio"]["volume"]
        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        open_alex = self.data["id"]
        string = f'{authors}, {title}, {volume}{issue}{pages}, ({year}), \
                    {self.data["doi"]}. cited by: {citedby}. {open_alex}'
        return string

    @property
    def ris(self):
        "Ris function for paper formatting."
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        return ris

    @property
    def bibtex(self):
        "Bibtex function for paper formatting."
        author = self.data["authorships"][0]["author"]["display_name"].split(" ")[-1]
        year = str(self.data["publication_year"])
        bibtex = f"""@ARTICLE{{{author}{year},
            author =	 {{{self.data['authorships'][0]['author']['display_name']}}},
            title =	 {{{self.data['title']}}},
            journal =	 {{{self.data['host_venue']['display_name']}}},
            volume =	 {{{str(self.data['biblio']['volume'])}}},
            number =	 {{{str(self.data['biblio']['issue'])}}},
            pages =	 {{{f"{self.data['biblio']['first_page']}-{self.data['biblio']['last_page']}"}}},
            year =	 {{{str(self.data['publication_year'])}}},
            doi =		 {{{self.data['doi'][16:]}}},
            url =		 {{{self.data['doi']}}},
            }} """

        return bibtex
