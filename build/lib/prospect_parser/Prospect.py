from datetime import datetime


ProspectType = dict[str, str | datetime | None]


class Prospect():
    def __init__(self, shop_name: str,  title: str | None,
                 thumbnail: str | None, valid_from: datetime | None,
                 valid_to: datetime | None, parsed_time: datetime) -> None:
        self.shop_name = shop_name
        self.title= title
        self.thumbnail= thumbnail
        self.valid_from = valid_from
        self.valid_to= valid_to
        self.parsed_time = parsed_time
        self.valid: bool = self.validate()

    def validate(self) -> bool:
        # validate content
        if any((self.title is None, 
                self.thumbnail is None,
                self.valid_from is None)):
            return False

        # validate dates
        now = datetime.today()
        if self.valid_from and self.valid_from > now:
            return False
        if self.valid_to and self.valid_to < now:
            return False

        return True

    def get_data(self) -> ProspectType:
        return{
            'shop_name': self.shop_name,
            'title': self.title,
            'thumbnail': self.thumbnail,
            'valid_from': self.valid_from.strftime('%Y-%m-%d')\
                if self.valid_from else None,
            'valid_to': self.valid_to.strftime('%Y-%m-%d')\
                if self.valid_to else None,
            'parsed_time': self.parsed_time.strftime('%Y-%m-%d %H:%M:%S')
        }