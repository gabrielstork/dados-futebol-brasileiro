import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_number_data(is_data):
    try:
        return int(is_data.text.strip())
    except ValueError:
        pass


class Brasileiro:
    def __init__(self,
                 year,
                 series):

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

        data = []
        for n in range(10, 201, 10):
            data.append(all_points[0 if n == 10 else n - 10: n])

        self._df = pd.DataFrame({"Position": range(1, self._teams + 1),
                                 "Teams": ranks,
                                 "Points": points,
                                 "Games": [value[0] for value in data],
                                 "Wins": [value[1] for value in data],
                                 "Draws": [value[2] for value in data],
                                 "Defeats": [value[3] for value in data],
                                 "Scored Goals": [value[4] for value in data],
                                 "Against Goals": [value[5] for value in data],
                                 "Goal Balance": [value[6] for value in data],
                                 "Yellow Cards": [value[7] for value in data],
                                 "Red Cards": [value[8] for value in data],
                                 "Points %": [value[9] for value in data]})

    def show_data(self):
        self._df.head(self._teams)

    def save_data(self, file_name, file_format="xlsx"):
        if file_format == "xlsx":
            self._df.to_excel(f"{file_name}.{file_format}", index=False)
        elif file_format == "csv":
            self._df.to_csv(f"{file_name}.{file_format}", index=False)
