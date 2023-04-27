"""works package."""
import time
import base64
import requests
import bibtexparser
import matplotlib.pyplot as plt
from IPython.core.pylabtools import print_figure


class Works:
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        return "str"

    def __repr__(self):
        _authors = [au["author"]["display_name"]
                    for au in self.data["authorships"]]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]

        journal = self.data["host_venue"]["display_name"]
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

        oa = self.data["id"]
        s = f'{authors}, {title}, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. {oa}'
        return s

    def _repr_markdown_(self):
        _authors = [
            f'[{au["author"]["display_name"]}]({au["author"]["id"]})'
            for au in self.data["authorships"]
        ]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1]

        title = self.data["title"]

        journal = f"[{self.data['host_venue']['display_name']}]({self.data['host_venue']['id']})"
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

        oa = self.data["id"]

        # Citation counts by year
        years = [e["year"] for e in self.data["counts_by_year"]]
        counts = [e["cited_by_count"] for e in self.data["counts_by_year"]]

        fig, ax = plt.subplots()
        ax.bar(years, counts)
        ax.set_xlabel("year")
        ax.set_ylabel("citation count")
        data = print_figure(fig, "png")  # save figure in string
        plt.close(fig)

        b64 = base64.b64encode(data).decode("utf8")
        citefig = f"![img](data:image/png;base64,{b64})"

        s = f'{authors}, *{title}*, **{journal}**, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. [Open Alex]({oa})'

        s += "<br>" + citefig
        return s

    @property
    def ris(self):
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
        print(ris)
        ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}" download="ris">Download RIS</a>'
        from IPython.display import HTML

        return HTML(uri)

    def related_works(self):
        rworks = []
        for rw_url in self.data["related_works"]:
            rw = Works(rw_url)
            rworks += [rw]
            time.sleep(0.101)
        return rworks

    def citing_works(self):
        Sum = []
        cited_by = self.data["cited_by_api_url"]
        citing_works = requests.get(cited_by).json()
        results = citing_works["results"]
        for i in results:
            title = i["title"]
            year = i["publication_year"]
            title_year = title + ", " + str(year)
            Sum.append(title_year)

        print("\n".join(Sum))

        return

    def references(self):
        Sum = []
        ref = self.data["referenced_works"]
        for i in ref:
            W_plus = i[21:]
            url1 = "https://api.openalex.org/works/" + str(W_plus)
            time.sleep(0.2)
            data1 = requests.get(url1).json()
            title = data1["title"]
            year = data1["publication_year"]
            title_year = title + ", " + str(year)
            Sum.append(title_year)

        print("\n".join(Sum))

        return

    @property
    def bibtex(self):
        bibtex = f"""@ARTICLE{{{self.data['id']},
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

        with open("bibtex.bib", "w") as bibfile:
            bibfile.write(bibtex)
        with open("bibtex.bib") as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)

        bibtex = bib_database.entries

        bibtex_list = list(bibtex[0].items())

        for i in bibtex_list:
            print(i[0] + " = " + i[1])
