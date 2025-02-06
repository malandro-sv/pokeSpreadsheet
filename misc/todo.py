#TODO:

"""
Aug 2nd: fixed on Aug3rd!
    it seems like spreadsheets.values.get
    will return majorDimension="ROWS" only.
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
    so far, that's what I've got. check further if this is definite
    or if something can be done.

    req = ss.values.get(spreadsheetId=ssId, range=A1Notation, majorDimension = "COLUMNS")

    return req.execute()

July 29th: COMPLETED
    regex to read cells from a sheet's Range
    and return next available row

    pending -- connect these three procedures/
            make them have sense together:

            ss.buildRange
            ss.getValues
            ss.nextValidRange

July 14th: COMPLETED
    catch KeyboardInterrupt
    check if the file is Trashed
    rename old json file --add last modified timestamp in rename.
    need to add condition for whenever a new file is crated,
    said new file has to write to json.
       else:
               print("wanna link another spreadsheet? ")
    return useful data when creating new sheet or loading existing to json

May 22nd. * COMPLETED on May 31st *
new pokemon object should return:
    1st, basic info
    2nd, stats

May 21st: * COMPLETED on May 22nd *
    - build untangledObject
    - separate object builders/extractors
      from objects created as vars.


DONE too: pokemon['game_indices'] with keys
    "game_index" and "version['name']" should
    be used at a separate sheet/table; same
    with game_indices, moves, sprites,


DONE (~june 20) May 31st:
    procedure that checks if the default jsonFile
    "workSpreadsheet.json" exists.

    if not, ask to either
        - fetch an existing sheet, link it to the jsonFile
            - has to be owned by user
            - has to be 'trashed' = False
        - create a new sheet, and save it as json file.

    June 12th:
        check if SS is not deleted.
        drive api > files.get has labels.trashed key
        warn if it is. ask what to do (create new one,
        or recover trashed SS if user = owner)


ways a range can be input like; eg:
Sheet1:A, Sheet1!A:A, Sheet1!A1, etc.
https://developers.google.com/sheets/api/guides/concepts#cell #
ways that do NOT work: Sheet1!A:, Sheet1!A

ways that do work for a same column:
Sheet1!A, Sheet1!A1, Sheet1!A:A Sheet1!A1:A
from a column to another: Sheet1!A:B, Sheet1!A1:B

done: the following below is a todo for a procedure that
always fetches 'name' along with its index (whichever it is)
out of pokemonKeys and that it pushes it to index 0 instead.
This should become the column Headers On a Sheet for main pokemon data

colHeaders are presented on the very first row:

rowOne = "!1:1"
raichu = getPokemon('raichu')
raichuSheet = getSingleSheet(psychSheet, 2)['title']
pokemonKeys = [i for i in pokemon.keys()]
rRange = rSheet['title'] + rowOne

colHeaders = valueRange(rRange, 'ROWS', pokemonKeys)

[k for k in raichu.keys()]
[n for n in range(0, len(raichu.keys()))]


# extract 'names' index#:
raichuKeys = [i for i in raichu.keys()]
[(i, raichuKeys[i]) for i in range(0,len(raichuKeys))]
# switching "name" to index 10:
raichuKeys.insert(0, raichuKeys[10])
# removing "name" from index 11:
raichuKeys.pop(11)
updateSheet(psychSheet, colHeaders)

june 26th, 2022:
mv stdOut/stdErr messages to a separate .py

dec7th:
extract sheet id and use it as "default" sheet
--done, Dec 14th

dec9th:
basic info goes into sheet id 0 if storing
additional information on additional sheets,
add their IDs into fullJson.
-- done, Dec 14th

dec 15th:
    clean stdOut whenever an action is completed
    -- hide it from frontend.

dec 16th: might need to update/write
array of sheetIds after deleting/adding
new sheets to a spreadsheet file.
for another project -- figure out
how to bulk delete multiple sheets.

#TODO: dec 24th- done on 25th:
       return a fully filtered [{sheet[i]Prop}]
       w/relevant eys:values. solution below:
    # these two procedures:
    #sheeTitle = lambda self, id: self.sheetInfo(prop="title", spreadsheetId=id)
    #sheetIds =  lambda self, id: self.sheetInfo(prop="sheetId", spreadsheetId=id)
    # are replaced with the procedures below:

        sheetProps = [i["properties"] for i in
                        ss.Sheet().fullSS(ss.crocs)["sheets"]]

        for key in [desiredKeys]:
            {sheetProperties[item]}.get(key)

        def keyExtraction(desiredKeys):
            return [{sheetproperties[index]}.get(key) for key in desiredKeys]

        def keyExtraction2(desiredKeyList):
            return [sheetProps[0][key] for key in desiredKeyList]

        def nuDict(self, ssId, i): #desiredKeyList):
            return  [self.fullSS(ssId)["sheets"][i]["properties"].get(key)
                    for key in desiredKeyList]

        sheetProps = self.getSheets(ssId)
        return  {k:v for k,v in sheetProps[i]["properties"].items()
                 if k in ["index", "sheetId", "title"]}

        # the above are prettyPrints for this list comprehension:
        #       [   {
        #               k:v for k,v in
        #               self.getSheets(ssId)[i]["properties"].items()
        #               if k in ["index", "sheetId", "title"]
        #               }
        #           for i in range(len(self.getSheets(ssId)))
        #       ]


    def sheetProps(self, ssId, targetProps):
        #   Takes [{sheetProps}] & [targetProps]; returns
        #    new [{sheetProps}] w/desired keys:values.

        sheetProps = self.getSheets(ssId)
        rng = range(len(sheetProps))
        nuDict = lambda i: {k:v for k,v in sheetProps[i]["properties"].items()
                            if key in targetProps}

        return [nuDict(i) for i in rng]

    #sheeTitles  = partialmethod(sheetProps, targetProps=["title"])
    sheetIds    = partialmethod(sheetProps, targetProps=["sheetId"])


#TODO:  include sheetRange for each sheet:
        completed on Jan 7th, as sheetProps update.

#TODO:  dec 14th: create general procedure to manage
        httpError/any error on any procedure.
        merge both Drive and Sheet into a single class,
        so the fullDict comes out as a method of a single object.

#TODO, jan 21st: include last json write timestamp.
                completed on the same date.
#TODO if no target.json file is found, create one. --done on Jan 23st.

Jan 23rd:   check columns headers, capabilities, trashed,
            modifiedByMe, nextRange, lastModTime, and others.
            valid before fetching additional pokemons.
            stdOut all faulty keys at once. might need
            to create a dict and feed it either thru:
            a) multiple calls to soundJson() or
            b) or by making soundJson() take multiple
            dicts at once.
            "a)" is failing to report all faulty values.
            not necessarily all at once, but they can
            be accumulated by another dict.
            DONE --procedure that ensures access/edit rights.

Jan 21st    toJson() has to include props/fields
#TODO, Jan 24th: DONE!
       this needs to be cross-referenced with the
       props in the cloud; call them and compare.
       {k:v for k,v in localDict.items()
       if k,v in cloudDict}

       keys in cloud only if also in local:
       [k for k in cloud["capabilities"].keys()
       if k in local["capabilities"]]#.keys()]

       by the same token:
       {k:v for k,v in cloud["capabilities"].keys()
       if k in local["capabilities"]}
       ==
       {k:v for k,v in cloud.items()
       if k in local.keys()}

       {k:v for k,v in local.items()
       if k in cloud and v == cloud[k]}

#TODO, Jan 31st: done, 17hr later.
        fetch file from the cloud and compare its props
        with the ones stored by the local .json.

Might not need this:
#localJson == full Json object, not path
def jsonDelta(localJson, cloudJson, keys):
#        Takes both local and cloud prop dicts,
#        returns k:v from local.items() if
#        k in cloud.items() and v != cloud[k]

    # the values of the following props
    # don't match between local and cloud json:
    deltaVals = [k for k,v in localJson.items()
                 if k in keys and v != cloud[k]]

    # values as set in the cloud:
    cloudDelta = {k:v for k,v in cloudJson.items()
                  if k in keys and v != localJson[k]}
    #TODO   Jan 31st: need a procedure for whenever
    #       a file isn't available anymore.
    #       furthermore, alert when a file was trashed
    #       and proceed accordingly.
    return deltaVals,  cloudDelta
#TODO March 15th, alert: localJson doesn't exist.
#TODO March 15th: list all specific
#   kwargs that are to be used.

#TODO alert of success/error for newInstance()
#TODO: change time() to elapsedTime.  """

#TODO:   Jan 14th:
#       urllib3.connection.HTTPSConnection
#       ss.SSLEOFError and TimeoutError
#       this might help with fecthing deletion times
#       self.changes = build("drive", "v3", credentials=self.creds).changes()
#TODO, March 23rd: this could be generalized a bit more
#   once receiving the "headers" (column titles) from
#   a pokemon object during first fetch. So, the total of
#   properties/attrs of the pokemon obj become the number of cols.
#TODO,  April 9th: check that targets == 1 in
#       file[n]["activities"][m]["targets"]
"""
# this is a user list, not to be played with here:
#11qWeCBsFHFdiuW0JN37sO5WNynwKlIdC7pTfT-0DXR4

# this is a user list, not to be played with here:
#11qWeCBsFHFdiuW0JN37sO5WNynwKlIdC7pTfT-0DXR4
#TODO:  Jan23th; make sure to return True only if
#       every value == theCorrectBool
#       a count based on len([relevantPropList]) should do.
#       done on the same day, minutes later
#       after conceptualizing it :D
#bulk delete all these files:
#TODO jan 23rd: create handlers for server responses.

#TODO Feb 5th,  move all prints to info.py
#as of Feb 5th, cloud faulty props return before local's
#if I fix cloud props (as in "if I untrash the ss in Drive",
#then this procedure will return faulty local props.
#I need to address this and return wrong props from both cloud
#AND LOCAL.
