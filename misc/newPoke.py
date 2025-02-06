#!/user/bin/env python

import requests

class A:

    def __new__(cls, name):

        if fetch(name):
            return super().__new__(cls)

        #if fetch(name):
        #    return super().__new__(cls)

        else:
            return False


    def __init__(self, name):

        self.name = name
        self.basicCols = ["id", "name", "type", "weight",\
                        "height", "base_experience",\
                        "type"]


    def fetch(self):

        try:
            url = "https://pokeapi.co/api/v2/pokemon/"
            return requests.get(url + self.name)

        except requests.exceptions.ConnectionError as err:
            print("Connection error!\n{}".format(err))

        except requests.exceptions.HTTPError as err:
            print("HTTPError!\n{}".format(err))

        except requests.exceptions.JSONDecodeError as err:
            print(err)


    def stats(self):

        stats = self.singleKey("stats")
        return {i["stat"]["name"]:i["base_stat"] for i in stats}


    def moves(self):

        moves = self.singleKey("moves")
        return [i["move"]["name"] for i in moves]


    def fullJson(self):

        return self.fetch().json()


    def singleKey(self, key):
        """ Takes one key, returns its value. """

        try:
            return self.fullJson()[key]

        except TypeError as err:
            print("Key '{}' not found.".format(key))

        except KeyError as err:
            print("Key '{}' not found.".format(key))


    def pushToSheet(self):

        return {**{k:v for k,v in self.fullJson().items()
                if k in self.basicCols },
                **self.stats(),
                **{"type":
                    self.singleKey("types")[0]["type"]["name"]},
                    }

    #TODO,  sept 26th:
    #       add remaining clases
    #       from pokemon.py
    #       oct 2nd: added most things needed. double check.


    #too tangled:
    #keys = [i["stat"]["name"] for i in stats]
    #values = [i["base_stat"] for i in stats]

    #return {keys[i]:values[i] for i in range(len(keys))}

    # way simpler:
    #return {i["stat"]["name"]:i["base_stat"] for i in stats}

    # { key:value for key,value
    #    in pokemonName.values()
    #    if key in desiredKeys }

    # THIS IS IT! DO NOT CONTINUE ON SIDE QUESTS!
    # [ value for key,values
    #   in pokemonExemplar.items()
    #   if key in desiredKeys ]
