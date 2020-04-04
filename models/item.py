import re
import uuid
from typing import Dict

import requests
from bs4 import BeautifulSoup

from models.model import Model


class Item(Model):
    URL = 'https://www.johnlewis.com/2020-apple-ipad-pro-11-inch-a12z-bionic-ios-wi-fi-256gb' \
          '/space-grey/p4949055'
    TAG_NAME = 'p'
    QUERY = {'class': 'price price--large'}
    collection = 'items'

    def __init__(self, url: str=URL, tag_name: str=TAG_NAME, query: Dict=QUERY, _id: str = None):
        super().__init__()
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return f"<Item {self.url}>"

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(name=self.tag_name, attrs=self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d*,?\d*\.\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "query": self.query,
        }
