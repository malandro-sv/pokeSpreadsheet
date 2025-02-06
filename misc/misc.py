#!/user/bin/env python

import requests

def fetchPokemon(pokemon):
    """ bare function """

    url = "https://pokeapi.co/api/v2/pokemon/"
    req = requests.get(url + pokemon)

    if req.status_code == 200:
        return req.json()

    else:
        return None

def filterProps(pokeProps, filter):
    """ takes pokemon.json(), returns
        a ll keys that are the same type"""

    return [i for i in pokeProps if type(pokeProps[i]).__name__ == filter]


def allPropTypes(pokemon):
    """ informative, console based only:
        will print each key along with its type. """

    [print("{}: {}".format(i, type(i)))
            for i in pokemon.keys()]



def listAllKeys(pokemon):
    """ Returns all keys for any pokemon. """

    if pokemon.exists():
        return [i for i in pokemon.buildPokemon().keys()]


def exists(self):

    if self.fetchPokemon().status_code == 200:
        return True


def buildPokemon(self):
    """ Returns the basic json object
        with data for a given pokemon. """

    if self.exists():
        return self.fetchPokemon().json()


def excludeIrrelevant(self, aTaskList, exclude=True):
    """ This one is from Tasks() """
    if exclude:
        return [
                {
                    k:v for k,v in i.items()
                    if k not in self.irrelevant
                    and bool(v) != False
                    }
                for i in aTaskList
                ]
    else:
        return [
                {
                    k:v
                    for k,v in i.items()
                    }
                for i in aTaskList
                ]

def compareSepQueries(self, q1, q2):
    # check if good idea to import inside
    # a function instead of at the beginning.
    randIndex = randint(0, len(q1["activities"]) -1)
    #randKey = lambda q: list(q.keys())["activities"]
    #return q1["activities"][randIndex]
    randKey = lambda q: (q)["activities"][randIndex]
    #return {
    #        "equal": randKey(q1) == randKey(q2),
    #        "index": randIndex,
    #        "timestamp": {
    #                        "f{q1}'s timestamp": q1["activities"][randIndex]["timestamp"],
    #                        "f{q2}'s timestamp": q2["activities"][randIndex]["timestamp"]
    #                        }
    #        }
    #return q1["activities"][randint(0,
    #                                len(q1["activities"]) -1)]
    #return q1["activities"][randIndex]

    print(f"{randKey(q1)['timestamp']}",
          f"\n{randKey(q2)['timestamp']}")
    return randKey(q1) == randKey(q2)


"""
    #def sheetProp(self, ssId, keys):
    ##TODO,  Jan 14th: might not need sheetProp; could fetch
    ##       sheeTitles and sheetIds thru ssProps instead.
    #    return [{k:v for k,v in i["properties"].items() if k in keys}
    #            for i in self.getSheets(ssId)]

    ## Shorthands for extracting titles and sheetIds:
    #sheeTitles  = partialmethod(sheetProp, keys="title")
    #sheetIds    = partialmethod(sheetProp, keys="sheetId")

        # Reads current range; returns next new range;
        # that is, range starting on next row. for this,
        # a regex w/the following match groups is used:
        #
        # 1       = sheet name.
        # 2 & 5   = column name
        # 4       = colon between start and end cells
        # 3 & 6   = row numbers.
        #

        #name = "(.*?[!])"
        #cell = "([A-Za-z]*)([1-9][0-9]*)"
        #target = re.compile(r"{}{}([:]){}".format(name, cell, cell))

        #if match := target.search(fullRange):

        #    group = lambda num: match.group(num)
        #    rowGroup = lambda num: str(int(match.group(num)) + 1)

        #    return "".join( group(1) +
        #                    group(2) + rowGroup(3) + ":" +
        #                    group(5) + rowGroup(6))

def main():

    if creds:

        try:
            service = build('sheets', 'v4', credentials=creds)

            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=lucho,
                                        range=sampleRange).execute()

            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            print('Name, Major:')
            for row in values:
                #TODO: print values getRangeVal(range)
                print('%s, %s' % (row[0], row[1]))

        except HttpError as err:
            print(err)


if __name__ == '__main__':
    main()

    #creds = creds(scopes['sheets'])
    #ss = build('sheets', 'v4', credentials=creds).spreadsheets()
    #values = ss.values()
    #get  = values.get
    #update = values.update
"""
