#!/usr/bin/env python

import os
#import info
from info import Message as Message
from pprint import pprint
from functools import partial
from ss import Drive, Spreadsheet
from time import time_ns, asctime
from json import dumps, load, decoder

#TODO jan 23rd: create handlers for server responses.
def jsonWorker(jsonFile, **kwargs):
    with open(jsonFile, kwargs["mode"]) as file:
        try:
            if kwargs["mode"] == "w":
                return file.write(dumps(
                    {**{"last write to this json": {
                        "ns": time_ns(),
                        "pretty printed": asctime()}}, #more relevant k here.
                     **Drive().get(kwargs["ssId"], fields=kwargs["fields"]),
                     **Spreadsheet().ssProps(kwargs["ssId"])
                     }, indent=4))
            else:
                return load(file)
        except decoder.JSONDecodeError as err:
            print("File is not in .json format.")
        except FileNotFoundError as err:
            return err
        except AttributeError as err:
            return err
        except FileNotFoundError as err:
            print(err)

toJson   = partial(jsonWorker, mode="w")
fromJson = partial(jsonWorker, mode="r")

def jsonDelta(localJson, cloudJson, keys):
    """ Takes both local and cloud prop dicts,
        returns k:v from local.items() if
        k in cloud.items() and v != cloud[k]"""

    # the values of the following props
    # don't match between local and cloud json:
    deltaVals = [k for k,v in localJson.items()
                 if k in keys and v != cloud[k]]

    # the values as they appear in the cloud:
    cloudDelta = {k:v for k,v in cloudJson.items()
                  if k in keys and v != localJson[k]}
    #TODO   Jan 31st: need a procedure for whenever
    #       a file isn't available anymore.
    #       furthermore, alert when a file was trashed
    #       and proceed accordingly.
    return deltaVals,  cloudDelta

def loadCreate():
    print("\nTo get started, choose an option:",
          "\n1. Create new Spreadsheet + local json.",
          "\n2. Enter the ID of an existing Spreadsheet.")
    #TODO Jan 23rd, a validation procedure must exist,
    #               to ensure that existing sheet has
    #               correct headers before fetching
    #               additional pokemons.
    #   update, Jan 31st: headers must originate from pokemon.py
    answer = input("Choose option [1/2]: ")

    if answer == "1":
        ssName  = input("Give your new Spreadsheet a name: ")
        ssId    = Drive().newSS(ssName)["id"]
        toJson(localJson, ssId=ssId, fields=fields)
        print("\nThe local '{}' file was successfully created.".format(localJson),
              "\nRemote '{}' file was successfully created.".format(ssId))
        return True

    elif answer == "2":
        print("\nEnter the Spreadsheet ID",
              "\n(Remove single ['] or double [\"]",
              "quotes from the ID first):")
        ssId = input("")
        return Drive().get(ssId.strip("\'"), fields=fields)
    else:
        print("Invalid option. Exit program.")
        return False

def checkDict(dict, key, val):
    """ takes a spreadsheet's dict w/keys related to
        access/edit; it returns True if every key is
        contextually correct (e.g. canEdit == True;
        trashed == False); else, it returns the keys
        w/incorrect values: {k:undesiredVal}.
        required to be False: trashed.
        required to be True: ownedByMe,
        capabilities["canEdit,canTrash,canUntrash"]. """
    #TODO Jan 31st: check if 'any()' is
    #               more efficient/faster.
    wrongVals = {k:v for k,v in dict.items()
                 if k in key and v != val}
    if wrongVals:
        return wrongVals
    else:
        return True

isTrashed   = partial(checkDict, key="trashed", val=False)
ownedByMe   = partial(checkDict, key="ownedByMe", val=True)
capabilts   = partial(checkDict, key="canEdit,canTrash,canUntrash", val=True)

def crankUp(localJson="pokemonSettings.json"):
    #TODO, Jan 29th -- 1) write f(error) on a separate module.
    #       and offer additional details. 2) update timestamp
    #       in json file after edits. spot manual ones and !!
    try:
        if os.path.exists(localJson):
            props       = fromJson(localJson)
            trashStatus = isTrashed(props)
            meOwner     = ownedByMe(props)
            caps        = capabilts(props["capabilities"])
            target      = [caps, trashStatus, meOwner]

            if all(index is True for index in target):
                # messg here.
                return Drive().get(props["id"], fields="*")
            else:
                # return
                # TODO, jan 31st: this block must be
                #       handled by another procedure
                #       that does both: xreference and
                #       check relevant props in cloudJson.
                # TODO, jan 31st: should xreference
                # the output of these props w/those
                # returned by Drive().get
                Message().unable(props["id"], localJson)
                for item in target:
                    if item != True and item != None and type(item) == dict:
                        for key in item:
                            print("The key '{}' has a value of '{}'"
                                  .format(key, item[key]))

    except KeyboardInterrupt as err:
        print("\n\n... Operation aborted. Exited program.")
    except FileNotFoundError as err:
        print("\nFile '{}' not found.".format(localJson))
        return loadCreate()

pokem = "pokemonSettings.json"
fields = "id, name, owners(emailAddress), ownedByMe,"     \
        "modifiedTime, trashed, createdTime, explicitlyTrashed,"\
        "capabilities(canEdit, canShare, canTrash, canUntrash),"\
        "lastModifyingUser(me, permissionId, kind, emailAddress)"
awesome =  "141t1LIo6BNwRxgV9MuHYBxIfAcpst-cblNRPhFgGSlE"
cloud   = Drive().get(awesome)
local   = fromJson(pokem)

ccaps = Drive().get(awesome)["capabilities"]
caps  = fromJson(pokem)["capabilities"]
