import json
import os
from pathlib import Path

import requests

from config import *
from exceptions import *


class Yugioh:
    def __init__(self):
        self.card_params = card_params
        self.endpoints   = endpoints

    def dealer(self, data):
        if data['type'] in monster_types:
            return Monster_Card(data)
        elif data['type'] == "Spell Card":
            return Spell_Card(data)
        elif data['type'] == "Trap Card":
            return Trap_Card(data)
        else:
            print(f"Error: The card type '{data['type']}' is unknown.")
            return None

    def get_card(self, **kwargs):
        endpoint = self.endpoints['card_information']

        for key in kwargs.keys():
            if key not in self.card_params:
                del kwargs[key]

        if ('id' in kwargs.keys()) and ('name' in kwargs.keys()):
            raise Exception(
                "id and name can't be passed together as arguments.")
        elif not len(kwargs):
            raise EmptyQueryError()

        r = requests.get(endpoint, params=kwargs)

        if r.status_code == 200:
            response = json.loads(r.content)
            cards = []
            for card in response['data']:
                cards.append(self.dealer(card))
            return cards

        elif r.status_code == 400:
            response = json.loads(r.content)
            raise QueryError(response['error'])

        else:
            return None


class Monster_Card:
    def __init__(self, data):
        self.archetype_   = data['archetype']
        self.atk_         = data['atk']
        self.attribute_   = data['attribute']
        self.card_images_ = data['card_images']
        self.card_prices_ = data['card_prices']
        self.card_sets_   = data['card_sets']
        self.def_         = data['def']
        self.desc_        = data['desc']
        self.id_          = data['id']
        self.level_       = data['level']
        self.name_        = data['id']
        self.race_        = data['race']
        self.type_        = data['type']
        self.card_images_ = data['card_images']

    def get_card_sets(self):
        card_sets = []
        for card_set in self.card_sets_:
            card_sets.append(Card_Set(card_set))
        return card_sets

    def get_all_card_images(self, size="big"):
        # Create 'ygopro/images' directory in home
        home = Path.home()
        if "ygopro" not in os.listdir(home):
            os.makedirs(os.path.join(home, "ygopro", "images"))

        for image in self.card_images_:
            filename = f"{image['id']}.jpg"

            if size == "big":
                r = requests.get(image['image_url'])
            elif size == "small":
                r = requests.get(image['image_url_small'])
            else:
                print("Error: Given size is not valid.")
                continue

            if r.status_code == 200:
                blob = r.content()
                with open(os.path.join(home, "ygopro", "images", filename), "wb") as f:
                    f.write(blob)
            else:
                print("Error: Server returned an unsuccessful status code.")
                continue

    def get_card_image(self, index=0, size="big"):
    # Create 'ygopro/images' directory in home
        home = Path.home()
        if "ygopro" not in os.listdir(home):
            os.makedirs(os.path.join(home, "ygopro", "images"))

        if index in range(len(self.card_images_)):
            image     = self.card_images_[index]
            filename  = f"{image['id']}.jpg"
            file_path = os.path.join(home, "ygopro", "images", filename)

            if size == "big":
                r = requests.get(image['image_url'])
            elif size == "small":
                r = requests.get(image['image_url_small'])
            else:
                print("Error: Given size is not valid.")
                return None

            if r.status_code == 200:
                blob = r.content()
                with open(file_path, "wb") as f:
                    f.write(blob)
                return file_path
            else:
                print("Error: Server returned an unsuccessful status code.")
                return None

        else:
            print("Error: The given index is exceeds the number of images.")
            return None

    def get_lowest_price(self):
        prices = list(self.card_prices_[0].items())
        lowest = prices[0]

        for price in prices[1:]:
            if price[1] < lowest[1]:
                lowest = price

        if lowest[0] == "cardmarket_price":
            return (lowest, "eur")
        else:
            return (lowest, "usd")

class Spell_Card:
    def __init__(self, data):
        print(data['type'])


class Trap_Card:
    def __init__(self, data):
        print(data['type'])

class Card_Set:
    def __init__(self, data):
        self.set_code_        = data['set_code']
        self.set_name_        = data['set_name']
        self.set_price_       = data['set_price']
        self.set_rarity_      = data['set_rarity']
        self.set_rarity_code_ = data['set_rarity_code']

if __name__ == "__main__":
    yugioh = Yugioh()
    yugioh.get_card(name="Dark Magician")
