import requests
import re
import json
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime

from prospect_parser.Prospect import Prospect

Link = tuple[str, str]
StoreLinks = list[Link]


class ProspectParser:
    def __init__(self, category: str='/hypermarkte/') -> None:
        self.category: str = category
        self.website: str = 'https://www.prospektmaschine.de'
        self.prospects: list['Prospect'] = []
        self.store_links: StoreLinks = []

    def _extract_dates(self, dates: str) -> list[datetime]:
        matched = re.findall(r'\d{2}\.\d{2}\.\d{4}', dates)
        return [datetime.strptime(d, '%d.%m.%Y')
                for d in matched]

    def _fetch_html(self, res: str) -> BeautifulSoup:
        site = requests.get(res)
        return BeautifulSoup(site.content, 'html.parser')

    def _get_store_links(self) -> None:
        soup = self._fetch_html(self.website + self.category)
        container = soup.find(id='left-category-shops')
        if not container:
            return

        for link in container.find_all('a'):
            href = link['href']
            store = link.get_text()
            if not isinstance(href, str):
                continue
            self.store_links.append((self.website + href, store))

    def _create_prospect(self,tag: Tag, store: str) -> 'Prospect':
        title = tag.find("h2")
        image = tag.find("img", src=True)
        src = image.get('src') if image else None
        date = tag.find("span", class_="hidden-sm")
        dates = self._extract_dates(date.get_text()) if date else []

        return Prospect(
            store,
            title.get_text(strip=True) if title else None,
            src if isinstance(src, str) else None,
            dates[0] if len(dates) > 0 else None,
            dates[1] if len(dates) > 1 else None,
            datetime.today()
        )

    def _fetch_store_prospects(self) -> None:
        for link, store in self.store_links:
            soup = self._fetch_html(link)
            container = soup.find(class_='page-body')
            if not container:
                continue

            for tag in container.find_all(class_='brochure-thumb',
                                          name='div'):
                prospect = self._create_prospect(tag, store.strip())
                self.prospects.append(prospect)

    def create_json(self) -> None:
        data = []
        for prospect in self.prospects:
            if prospect.valid:
                data.append(prospect.get_data())

        jsoned = json.dumps(data, indent=4, ensure_ascii=False)
        with open('prospects.json', 'w', encoding='UTF-8') as f:
            f.write(jsoned)

    def run(self) -> None:
        self._get_store_links()
        self._fetch_store_prospects()
        self.create_json()
