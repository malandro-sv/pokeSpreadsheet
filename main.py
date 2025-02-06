#!/usr/bin/env python

import os
from pprint import pprint
from functools import partial
from ss import Drive, Spreadsheet
from time import time_ns, asctime
from info import Prompt as Prompt
from info import Message as Message
from json import dumps, load, decoder

def jsonWorker(jsonFile, **kwargs):
    """ kwargs = mode, fields, ssId, content """

    with open(jsonFile, kwargs["mode"]) as file:
        try:
            if kwargs["mode"] == "w":
                return file.write(dumps(kwargs["content"],
                                        indent=4))
            elif os.path.exists(jsonFile):
                return load(file)

        except decoder.JSONDecodeError as err:
            print("File is not in .json format.")
        except FileNotFoundError as err:
            return err
        except AttributeError as err:
            return err
        except FileNotFoundError as err:
            print(err)
        except KeyError as err:
            print(err)

# newInstance and updateInstance could be
# implemented through "partial" method
# as toJson and fromJson have.
def newInstance():
    #TODO:
    # advise if either json or sheet
    # exist with the name the user inputs.
    ssName  = Prompt().newSpreadsheet()
    ssId    = Drive().newSS(ssName)["id"]

    try:
        return toJson(Prompt().newLocalJson(),
                      ssId=ssId,
                      content={
                          **{"last write to this json": {
                              "ns": time_ns(),
                              "pretty printed": asctime()}},
                          **Drive().get(ssId,
                                        fields=fields),
                          **Spreadsheet().ssProps(ssId)
                          }, indent=4)
    except HttpError as err:
        return err

def updateLocalJson(localJson):
    local = fromJson(localJson)
    ssId = Drive().get(local["id"])
    return toJson(localJson,
                  ssId=ssId, content=ssId)

toJson   = partial(jsonWorker, mode="w")
fromJson = partial(jsonWorker, mode="r")

def loadCreate():
    answer = Message().loadCreate()
    if answer == "1":
        return newInstance()
    elif answer == "2":
        ssId = Prompt().getExistingSS()
        return Drive().get(ssId.strip("\'"),
                           fields=fields)
    else:
        Message().invalid(answer)
        return False

def flatten(jsonObj, desiredKeys):

    flat = {}
    def recurse(dictionary, filters, accumulator):

        for key,value in dictionary.items():
            if type(value) != dict:
                flat[key] = value
            elif type(value) == dict:
                recurse(value, filters, accumulator)
        return accumulator
    return recurse(jsonObj, desiredKeys, flat)

def filterProp(jsonObj, keys, expectedVal):

    flat = flatten(jsonObj, keys).items()
    if type(keys) == list:
        if len([v for k,v in flat if k in keys
                and v == expectedVal]) == len(keys):
            return True
        else:
            return {
                    k:v for k,v in flat
                    if k in keys
                    and v != expectedVal
                    }
    else:
        return Message().notAlist(keys)

def localNcloud(local, cloud):
    """ Takes a local json, it uses its "id" to
        retrieve a file from the cloud and it checks that
        it is editable, deletable and owned by the user. """

    keys = ["canEdit",
            "canTrash",
            "canUntrash",
            "ownedByMe",
            "canModifyContent"]

    both = [filterProp(cloud, keys, True),
            filterProp(local, keys, True)]
    if not (culprit:=
            [i for i in both if i is not True]):
        return True
    else:
        return culprit

def crankUp(localJson="spreadsheetSettings.json" ):

    """ It takes the local json, it reads its id and
        checks that its corresponding spreadsheet file
        still exists on Google Drive.  """

    if os.path.exists(localJson):
        local = fromJson(localJson)
        ssId = Drive().get(local["id"])

        if not Drive().trashed(local["id"])["trashed"]:
            return localNcloud(local,
                               Drive().get(local["id"]))
        else:
            #Message().trashedSheet(local["id"])
            print("trying to update local file: ")
            updateInstance(local)
    else:
        Message.notFound(localJson)
        return False

            # update local json accordingly; prompt to take action.
            #toJson(update local json accordingly.)
            #return Drive().restoreSS(local["id"])
            # see if spreadsheet can be restored (lines 51-55
            # at ss.py for further info on this.

    #TODO once it's all good:
    # work on reformatting per PEP8
    # https://peps.python.org/pep-0008/
    #TODO, handle 404s
fields = "id, name, owners(emailAddress), ownedByMe,"     \
        "modifiedTime, trashed, createdTime, explicitlyTrashed,"\
        "capabilities(canEdit, canShare, canTrash, canUntrash),"\
        "lastModifyingUser(me, permissionId, kind, emailAddress)"

awesmId =  "141t1LIo6BNwRxgV9MuHYBxIfAcpst-cblNRPhFgGSlE"
cloud   = Drive().get(awesmId)
ccaps = Drive().get(awesmId)["capabilities"]
delFol2 = "0B1ds37a-9FkpaUpjQlhYUldZZVk"
delFol1 = "0B1ds37a-9FkpVU55UWZwU1JfWm8"
