import requests
import re
import json
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime


Filter = str | None
Link = tuple[str, str]
StoreLinks = list[Link]
Prospect = dict[str, str | list[str] | None]
Storage = list[Prospect]


class ProspectParser:
    def __init__(self) -> None:
        self.category: str = '/hypermarkte/'
        self.website: str = 'https://www.prospektmaschine.de'
        self.prospects: Storage = []
        self.store_links: StoreLinks = []

    def _reformat_dates(self, dates: str) -> list[str]:
        new_dates: list[str] = []
        matched = re.findall(r'\d{2}.\d{2}.\d{4}', dates)
        for match in matched:
            formated = datetime.strptime(match, '%d.%m.%Y')
            new_dates.append(formated.strftime('%Y-%m-%d'))
        return new_dates

    def _is_valid_prospect(self, dates: list[str]) -> bool:
        current_date = datetime.today().strftime('%Y-%m-%d')
        start = dates[0]
        end = dates[1] if len(dates) > 1 else None

        if start > current_date:
            return False
        if end and end < current_date:
            return False
        return True

    def _fetch_content(self, res: str,
                       id_filter: Filter = None,
                       class_filter: Filter = None) -> Tag | None:
        request = requests.get(res)
        soup = BeautifulSoup(request.content, 'html.parser')
        if class_filter is not None:
            return soup.find(class_=class_filter)
        if id_filter is not None:
            return soup.find(id=id_filter)
        return None

    def _get_store_links_from_website(self) -> None:
        soup = self._fetch_content(self.website + self.category,
                                   id_filter='left-category-shops')
        if not soup:
            return

        for link in soup.find_all('a'):
            href = link['href']
            store = link.get_text()
            if not isinstance(href, str):
                continue
            self.store_links.append((self.website + href, store))

    def _fetch_validate_store_prospects(self) -> None:
        for link, store in self.store_links:
            prospects = self._fetch_content(link, class_filter='page-body')
            if not prospects:
                return

            for prospect in prospects.find_all(class_='brochure-thumb',
                                               name='div'):
                prospect_data = prospect.find_all(['h2', 'img', 'span'])
                title = prospect.find("h2")
                image = prospect.find("img", src=True)
                date_span = prospect.find("span", class_="hidden-sm")

                if any((title is None, image is None, date_span is None)):
                    continue

                temp_storage: Prospect = {'shop_name': store.strip()}

                for data in prospect_data:
                    if data.name == 'h2':
                        temp_storage['title'] = data.get_text().strip()
                    elif data.name == 'img':
                        temp_storage['thumbnail'] = data['src']
                    elif data.name == 'span' and 'hidden-sm' in data['class']:
                        dates: list[str] = self._reformat_dates(data.get_text())

                        if self._is_valid_prospect(dates):
                            temp_storage['valid_from'] = dates[0]
                            if len(dates) == 2:
                                temp_storage['valid_to'] = dates[1]
                            else:
                                temp_storage['valid_to'] = None
                        else:
                            break

                if len(temp_storage) == 5:
                    temp_storage['parsed_time'] = \
                        datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    self.prospects.append(temp_storage)

    def fill_storage(self) -> None:
        self._get_store_links_from_website()
        self._fetch_validate_store_prospects()

    def create_json(self) -> None:
        jsoned = json.dumps(self.prospects, indent=4, ensure_ascii=False)
        with open('prospects.json', 'w', encoding='UTF-8') as f:
            f.write(jsoned)
