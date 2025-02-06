#!/usr/bin/env python

#import re
#from __future__ import print_function
from sys import path
from random import randint
from json import dump, dumps
from time import time, sleep

from functools import partialmethod
from google.auth.transport.requests import Request
#from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
sheetMime = "mimeType='application/vnd.google-apps.spreadsheet'"
#TODO: handle googleapiclient.errors.HttpError

path.insert(0, "misc/")
path.insert(0, "utils/")
from info import Message as Message
from creds import creds, scopes

class Drive():
    def __new__(cls):
        if creds(scopes):
            return super().__new__(cls)

    def __init__(self):
        self.scopes = scopes
        self.creds = creds(scopes)
        self.drive = build("drive", "v3",
                           credentials=self.creds).files()
        self.activity = build("driveactivity", "v2",
                              credentials=self.creds).activity()

    def search(self, queryTerms):
        #TODO: more comprehensive queries.
        """ q="mimeType='application/vnd.google-apps.spreadsheet'
            and name='pokemon"                              """
        # get.list(q="starred and trashed").execute()
        # other queries that work: q="(trashed=true) and starred")
        return self.drive.list(q=queryTerms).execute()

    def get(self, id, fields="*"):
        return self.drive.get(fileId=id, fields=fields).execute()

    def newSS(self, name):
        body = {"name": name,
                "mimeType": "application/vnd.google-apps.spreadsheet"}
        return self.drive.create(body=body).execute()

    def trashUntrash(self, ssId, bool):
        if bool == self.get(ssId)["trashed"]:
            Message.trashUntrash(ssId)
            return False
        else:
            Message().success()
            return self.drive.update(fileId=ssId,
                                     body={"trashed": bool}).execute()
    def inquire(self, body=None):
        # body={"filter": "detail.action_detail_case:DELETE"}
        return self.activity.query(body=body).execute()

    def deletionHistory(self, ssId):
        """ This wrapped request returns an activities/nextPageToken
            json response; 'activities' key is a list of all related
            "DELETED/RESTORE" events associated with a spreadsheet. """
        itemName = f'items/{ssId}'
        body = {
                "itemName": itemName,
                "filter": "detail.action_detail_case:(DELETE RESTORE)"
                }
        restoreTimes = delTimes = 0
        deletedRestored = self.inquire(body=body)
        return deletedRestored

    def latestDeleteRestore(self, ssId):
        global activities
        activities = self.deletionHistory(ssId)["activities"]
        timestamp = lambda index: activities[index]["timestamp"]
        action = lambda index: list(activities[index]["actions"][0]["detail"].keys())[0]

        def counter(action):
            count = 0
            timestamps = []
            for entry in activities:
                if action in entry["actions"][0]["detail"].keys():
                    timestamps.append(entry["timestamp"])
                    count += 1
            print(f"\nAction '{action}' has been applied {count} times:")
            for timestamp in timestamps:
                #TODO april 17th: regex timestamp
                print(timestamp)
            if timestamps:
                return True

        print(f"Last '{action(0)}' operation occured on {timestamp(0)}.")
        if action(0) == "delete":
            pass
            #if timestamp <= 20 days, restore.


    #TODO:
    #   It may be possible to check when exactly a file
    #   was deleted; visit DriveActivity (API v2):
    #   developers.google.com/drive/activity/v2/reference/rest/v2/activity/driveactivity

    def fullQuery(self, localJson, maxPages=None):
        """ fetches DriveActivity jsons and creates
            a new meta json as list of dicts. """
        try:
            out = []
            counter = 0
            start = time()
            q = self.inquire()
            while (counter < maxPages) if maxPages \
            else q["nextPageToken"] is not None:
                counter += 1
                print(f'{counter}: {time() - start}')
                out.append(q)
                sleep(.7)
                q = self.inquire(body={"pageToken":
                                       q["nextPageToken"]})
        except KeyError as err:
            Message().lastPageToken()
        except KeyboardInterrupt:
            print(f"Process interrupted at iteration {counter}.")
        finally:
            Message.doNotDelete(localJson)
            with open(localJson, "w") as file:
                file.write(dumps(out,indent=2))
            print(f"Elapsed time: {time() - start}")
            Message.downloadSuccess(localJson)
            return True

    def newQuery(self, maxPages=None, pageToken=None):
        out = []
        counter = 0
        query = self.inquire(body={"pageToken": pageToken})
        try:
            while (counter < maxPages) if maxPages \
            else query["nextPageToken"] is not None:
                counter += 1
                print(f'{counter}: {time()}')
                out.append(query)
                query = self.inquire(body={"pageToken":
                                       query["nextPageToken"]})
                sleep(.7)
        finally:
            return out

    def allSheetActivity(self, json):
        allSheets = []
        pageCount = totalActi = 0
        sheetMime = "application/vnd.google-apps.spreadsheet"
        try:
            for page in json:
                partialActivityCount = 0
                if "activities" in page:
                    for activity in page["activities"]:
                        if activity["targets"][0]["driveItem"]["mimeType"] == sheetMime:
                            allSheets.append(activity)
                            partialActivityCount +=1
                            totalActi += 1
                print(f'Page {pageCount}, Sheet related entries: {partialActivityCount}')
                pageCount +=1
        except KeyError:
            print("****")
        finally:
            print(f'Total pages: {pageCount}, Activities: {totalActi}')
            return allSheets

    def deleteActivity(self, fullActivity):
        sheets = []
        sheetMime = "application/vnd.google-apps.spreadsheet"
        try:
            for page in fullActivity:
                if "activities" in page:
                    for activity in page["activities"]:
                        #TODO: insert the procedure here.
                        if activity["targets"][0]["driveItem"]["mimeType"] == sheetMime:
                            sheets.append(activity)

        #if "delete" in ["primaryActionDetail"]:
        finally:
            return sheets

    """
    if "delete" in fullHistory[m]["activities"][n]["primaryActionDetail"]:
        list.append(activity)

    if "delete" in fullHistory[m]["activities"][n]["primaryActionDetail"]:
        list.append(activity)
    if "items/ssId" in activity["targets"][0]["driveItem"]["name"]
    if "items/ssId" in fullHistory[m]["activities"][n]["targets"][0]["driveItem"]["name"]
    "items/1BppCSXu9QWkvHItysK44T_LFjeol_mRZ"
    def activitySummary(self, activityJson):

        pageCount = totalActi = 0
        try:
            for page in activityJson:
                activitiesPerPage = 0
                if "activities" in page:
                    for activity in page["activities"]:
                        activitiesPerPage +=1
                        totalActi += 1
                pageCount +=1
                print(f'Page {pageCount}, activities: {activitiesPerPage}')
        finally:
            print(f'Total: {pageCount} activityJson, {totalActi} activities.')
        #       also, fetch from file[n]["activities"][m].keys() as well:
        #       targets[0]["driveItem"]["name"], actions, timestamp.
        #for page in file:
        #   for activity in page["activities"]:
        #       do something if len(activity["targets"]) >1
    """

#Message.restoreAttempt(local["id"])
    trash   = partialmethod(trashUntrash, bool=True)
    untrash = partialmethod(trashUntrash, bool=False)
    trashed = partialmethod(get, fields="trashed")

    def restoreSS(self, ssId):
        if Message().attemptRestore(ssId):
            return self.untrash(ssId)

class Spreadsheet():
    def __new__(cls):
        #if creds(scopes['drive']):
        return super().__new__(cls)

    def __init__(self):
        self.creds =    creds(scopes['sheets'])
        self.ss =       build('sheets', 'v4',\
                        credentials=self.creds).spreadsheets()
        self.values =   self.ss.values()

    def wholeSS(self, ssId):
        return self.ss.get(spreadsheetId=ssId).execute()

    def body(self, ssId, range, vals, dimension="ROWS"):
        try:
            return {"range": self.nextRange(range),
                    "majorDimension": dimension,
                    "values": [vals]} #array of arrays
        except AttributeError as err:
            return err

    def getValues(self, ssId, range):
        """ Returns arrays of data from a range. if input
            is sheetName, it returns its whole content."""
        return self.values.get(spreadsheetId=ssId, range=range).execute()

    def nextRange(self, ssId, sheetName):
        """ Takes the name of the working sheet, it returns the next
            available row. If sheet is empty, it defaults to row#1. """
        try:
            row = 1 + len(self.getValues(ssId, sheetName + "!A:G")["values"])
            return sheetName + "!A{}:G{}".format(row, row)

        except KeyError as err:
            return sheetName + "!A1:G1"
        except HttpError as err:
            return err

    def updateValues(self, ssId, body):
        userInput = "USER_ENTERED" # might need others.
        return  self.values.update( spreadsheetId=self.ssId,
                                    range=body['range'], body=body,
                                    valueInputOption=userInput).execute()
    def action(self, ssId, **kwargs):
        i = kwargs["i"]
        request = [{"deleteSheet":  {"sheetId": None}},
                   {"addSheet":     {"properties":
                                     { "title": None}}},
                   {"updateSheetProp":
                                    {"properties": {"sheetId":  None,
                                                    "title":    None},
                                                    "fields": "title"}}]
        if i == 0:
            request[i]["addSheet"]["properties"]["title"] = kwargs["title"]
        elif i == 1:
            request[i]["deleteSheet"]["sheetId"] = kwargs["sheetId"]
        elif i == 2: #
            request[i]["updateSheetProp"]["properties"].update(
                    {"title": kwargs["title"], "sheetId": kwargs["sheetId"]})

        body = {"requests": [request[i]]}
        return self.ss.batchUpdate(spreadsheetId = ssId, #kwargs["ssId"],
                                   body = body).execute()

    # In the lambdas below, id = spreadsheetId
    getSheets = lambda self, ssId: self.wholeSS(ssId)["sheets"]
    addSheet = lambda self, id, title: self.action(i=0, ssId=id, title=title)
    delSheet = lambda self, id, shtId: self.action(i=1, ssId=id, sheetId=shtId)
    renameSheet = lambda self, id, shtId, title: self.action(i=2, id=id,
                                                   title=title, sheetId=shtId)
    def ssProps(self, ssId):
        """ returns props of every working sheet. """
        return {"workingSheets":
                [{
                **{k:v for k,v in i["properties"].items()
                   if k in "index,sheetId,title"},
                **{"nextRange":
                   self.nextRange(ssId, i["properties"]["title"])}
                } for i in self.getSheets(ssId)]}

class Tasks():
    def __new__(cls):
       if creds(scopes):
            return super().__new__(cls)

    def __init__(self):
        self.scopes = scopes
        self.creds = creds(scopes)
        self.tasks = build("tasks", "v1", credentials = self.creds)
        self.irrelevant = [
                "etag",
                "kind",
                "selfLink"
                ]
    def listAttrs(self, listId):
        """ Takes a tasklist Id; it returns
            its attrs but no list of tasks.  """
        return self.tasks.tasklists().get(
                tasklist=listId).execute()

    def exclude(self, aList, exclude=True):
        return [
                {
                    k:v for k,v in i.items()
                    if (exclude
                        and k not in self.irrelevant
                        and bool(v))
                    or (not exclude)
                    }
                for i in aList
                ]
    def fetchAllLists(self, exclude=True):
        """ Fetches all existing lists &
            returns their props but self.irrelevant. """
        lists = self.tasks.tasklists().list().execute()["items"]
        return self.exclude(lists, exclude=exclude)

    def fetchTasksinList(self, listId, exclude=True):
        """ Takes taskList, returns every task
            without self.irrelevant props. """
        rawList = self.tasks.tasks().list(
                tasklist=listId).execute()["items"]
        return self.exclude(rawList, exclude=exclude)

    def moveTask(self, taskId):
        pass

