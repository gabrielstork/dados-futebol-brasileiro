import pathlib
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Brasileiro:
    def __init__(self, year: int, series: str) -> None:
        if year < 2012:
            raise ValueError('year must be greater than 2012')
        elif series.lower() not in ['a', 'b']:
            raise ValueError("series must be 'A' or 'B'")

        self.year = year
        self.series = series.lower()

        self._df = pd.DataFrame()
        self._url = (
            'https://www.cbf.com.br/futebol-brasileiro/competicoes/'
            f'campeonato-brasileiro-serie-{self.series}/{self.year}'
        )
        self._response = requests.get(self._url)
        self._soup = BeautifulSoup(self._response.content, 'html.parser')

    def _get_teams(self) -> list:
        teams_html = self._soup.find_all(
            name='span', attrs={'class': 'hidden-xs'}
        )
        teams = [team.text for team in teams_html]

        return teams

    def _get_points(self) -> list:
        points_html = self._soup.find_all(
            name='th', attrs={'class': None, 'scope': 'row'}
        )
        points = [int(point.text) for point in points_html]

        return points

    def _get_matches(self) -> list:
        matches_html = self._soup.find_all(
            name='td', attrs={'class': None}
        )
        matches_text = []

        for item in matches_html:
            try:
                matches_text.append(int(item.text))
            except ValueError:
                # If the item can not be converted to 'int', it is useless
                # so we simply 'pass'
                pass

        matches = [list(n) for n in zip(*[iter(matches_text)] * 4)]

        return matches

    def _get_others(self) -> list:
        others_html = self._soup.find_all(
            name='td', attrs={'class': 'hidden-xs'}
        )
        others_text = [other.text for other in others_html]
        others = [list(n) for n in zip(*[iter(others_text)] * 6)]

        return others

    def get_data(self) -> None:
        teams = self._get_teams()
        points = self._get_points()
        matches = self._get_matches()
        others = self._get_others()

        info = {
            'Position': range(1, len(teams) + 1),
            'Team': teams,
            'Points': points,
            'Games': [n[0] for n in matches],
            'Wins': [n[1] for n in matches],
            'Draws': [n[2] for n in matches],
            'Defeats': [n[3] for n in matches],
            'Scored Goals': [n[0] for n in others],
            'Against Goals': [n[1] for n in others],
            'Goal Balance': [n[2] for n in others],
            'Yellow Cards': [n[3] for n in others],
            'Red Cards': [n[4] for n in others],
            'Points %': [n[5] for n in others],
        }

        self._df = pd.DataFrame(data=info)

    def show_data(self) -> None:
        teams = self._df.shape[0]
        print(self._df.head(teams))

    def save_data(self, path: str) -> None:
        file = pathlib.Path(path)

        if file.suffix == '.csv':
            self._df.to_csv(path, index=False)
        elif file.suffix == '.xlsx':
            self._df.to_excel(path, index=False)
