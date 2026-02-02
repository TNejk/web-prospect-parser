import requests
from bs4 import BeautifulSoup

# read content of a website
# find list of stores and store it
# iterate through the list and find valid prospects
# build JSON file


Prospect = tuple[str]
ValidProspects = list[Prospect]
Storage = dict[str, ValidProspects]


class ProspectParser:
    def __init__(self, website: str, id_filter: str):
        self.website: str = website
        self.id_filter: str = id_filter
        self.prospects: Storage = {}


    def _fetch_content(self, website, id_filter):
        res = requests.get(website)
        soup = BeautifulSoup(res.content, 'html.parser')
        return soup.find(id = id_filter)


    def _get_valid_prospects(self, content):
        pass


    def fill_storage(self):
        links = self._fetch_content()
        if content:
            valid_prospects: ValidProspects = self._get_valid_prospects(content)


class JSONBuilder:
    def __init__(self):
        pass


def reformat(dates: str) -> list[str]:
    formated: list[str] = []
    dates = dates.split(' - ')
    for date in dates:
        splited = reversed(date.split('.'))
        formated.append('-'.join(splited))
    return formated


website = 'https://www.prospektmaschine.de'
id_filter = 'left-category-shops'

res = requests.get(website + '/hypermarkte/')
soup = BeautifulSoup(res.content, 'html.parser')
content = soup.find(id=id_filter)

if content:
    for link in content.find_all('a'):
        print('============')
        print(link.get_text())
        res = requests.get(website + link.get('href'))
        soup = BeautifulSoup(res.content, 'html.parser')
        content = soup.find(class_='brochure-thumb')
        if content:
            data = content.find_all(['h2', 'img', 'span'])
            #print(data)
            for entry in data:
                #print(entry)
                if entry.name == 'img':
                   print(entry.get('src'))
                if entry.name == 'span' and 'hidden-sm' in entry.get('class', []):
                    print(reformat(entry.get_text()))
                    
            # for image in images:
            #     print(image.get('src'))
            # dates = content.find_all('span', class_='hidden-sm')
            # formatedDates = []
            # for dateTuple in dates:
            #     ndates = dateTuple.get_text().split(' - ')
            #     for date in ndates:
            #         ndate = date.split('.')
            #         ndate.reverse()
            #         stringified = ''
            #         for val in ndate:
            #             stringified += val + '-'
            #         print(stringified)
        else:
            print("No brochures found")
else:
    print("No article content found.")