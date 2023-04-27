"""works package."""
import time
import requests


class Works:
    "This is a paper finding class on Open Alex."

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

    def related_works(self):
        "Related works function."
        rworks = []
        for rw_url in self.data["related_works"]:
            related_works = Works(rw_url)
            rworks += [related_works]
            time.sleep(0.101)
        return rworks

    def citing_works(self):
        "Citing works function."
        information = []
        cited_by = self.data["cited_by_api_url"]
        citing_works = requests.get(cited_by).json()
        results = citing_works["results"]
        for i in results:
            title = i["title"]
            year = i["publication_year"]
            title_year = title + ", " + str(year)
            information.append(title_year)

        print("\n".join(information))

    def references(self):
        "References function."
        referenced_data = []
        ref = self.data["referenced_works"]
        for i in ref:
            doi = i[21:]
            url1 = "https://api.openalex.org/works/" + str(doi)
            time.sleep(0.2)
            data1 = requests.get(url1).json()
            title = data1["title"]
            year = data1["publication_year"]
            title_year = title + ", " + str(year)
            referenced_data.append(title_year)

        print("\n".join(referenced_data))

    @property
    def bibtex(self):
        "Bibtex function."
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
