import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_number_data(is_data):
    try:
        return int(is_data.text.strip())
    except ValueError:
        pass


class Brasileiro:
    def __init__(self, year, series):

        if type(year) is not int:
            raise TypeError("year value must be 'int'")
        elif year < 2012:
            raise ValueError("year must be greater than 2012")
        elif series.lower() not in ["a", "b"]:
            raise ValueError("series must be 'A' or 'B'")

        self._year = year
        self._teams = 20
        self._series = series.lower()

    def get_data(self):
        url = ("https://www.cbf.com.br/futebol-brasileiro/competicoes/"
               f"campeonato-brasileiro-serie-{self._series}/{self._year}")
        table = requests.get(url)
        soup = BeautifulSoup(table.content, "html.parser")

        rank_html = soup.find_all(name="span", attrs={"class": "hidden-xs"})
        ranks = [rank.text for rank in rank_html]

        points_html = soup.find_all(name="th",
                                    attrs={"class": None, "scope": "row"})
        points = [int(point.text) for point in points_html]

        all_points = [x for x in map(get_number_data, soup.find_all(name="td"))
                      if x is not None]

        values = []
        for n in range(10, 201, 10):
            values.append(all_points[0 if n == 10 else n - 10: n])

        self._df = pd.DataFrame({"Position": range(1, self._teams + 1),
                                 "Team": ranks,
                                 "Points": points,
                                 "Games": [val[0] for val in values],
                                 "Wins": [val[1] for val in values],
                                 "Draws": [val[2] for val in values],
                                 "Defeats": [val[3] for val in values],
                                 "Scored Goals": [val[4] for val in values],
                                 "Against Goals": [val[5] for val in values],
                                 "Goal Balance": [val[6] for val in values],
                                 "Yellow Cards": [val[7] for val in values],
                                 "Red Cards": [val[8] for val in values],
                                 "Points %": [val[9] for val in values]})

    def show_data(self):
        try:
            return self._df.head(self._teams)
        except AttributeError:
            print(None)

    def save_data(self, file_name, file_format="xlsx"):
        if file_format not in ["xlsx", "csv"]:
            raise ValueError("available file formats: 'xlsx' and 'csv'")
        try:
            if file_format == "xlsx":
                self._df.to_excel(f"{file_name}.{file_format}", index=False)
            elif file_format == "csv":
                self._df.to_csv(f"{file_name}.{file_format}", index=False)
        except AttributeError:
            print(None)
