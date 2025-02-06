#!/usr/bin/env python

class Message():
    #def __init__():

    def invalid(self, input):
        print("Invalid input '{}'".format(input))

    def unable(self, *args):
        print("\nUnable to proceed!\n",
           "\nThe Spreadsheet '{}'\ncan't be used "\
           "as one or more of its keys has/have incorrect value(s).".format(*args),
           "\nPlease review further and make changes accordingly:")

    def pathExists(self, localJson):
        print("File '{}' was found locally!".format(localJson))

    def printItems(self, *args):
        print("Property '{}' in '{}' is set to {}.".format(*args))

    def successfulCreation(self, localJson, ssId):
        print("\nLocal file '{}' was successfully created!".format(localJson),
              "\nRemote '{}' file was successfully created!".format(ssId))

    def wrongPropVals(self, *args):
        print("Setting '{}' has the incorrect value of '{}'"
              .format(*args ))

    def notAlist(self, allegedList):
        print("'{}' isn't a list... Exiting.".format(allegedList))

    def notFound(fileName):
        print("File '{}' not found".format(fileName))

    def trashUntrash(ssId):
        print(  "File '{}' is already at desired status".format(ssId),
                "No changes made.")
    def trashedSheet(self, ssId):
        print("Spreadsheet with id '{}' is in Trash.\n".format(ssId),
              "You'll need to either restore if possible,\n",
              "or create a new one to proceed.")

    def attemptRestore(self, ssId):
        yes = ["y", "ye", "yes"]
        if input("Attempt a restoration? [Y/N]") in yes:
            print("Attempting to restore spreasheet with '{}'".format(ssId))
        else:
            print("Approval not received. No further action will be performed." )

    def success(self):
        print("Action was successfully completed!")

    def lastPageToken(self):
        print("Reached the last page with relevant data.")

    def doNotDelete(file):
        print(f"Do not remove/rename {file}")

    def downloadSuccess(self, localJson):
        print(f'Activity downloaded to {localJson}')
    #def differentIds(self, localJson, cloudJson):
    #    print("The json objects presented have different Ids:",
    #          "\n"
    #          "Local json file has Id {}".format(localJson["id"]),
    #          "\n"
    #          "Cloud json has Id {}".format(cloudJson["id"]))

class Prompt():

    def loadCreate(self):
        print("\nTo get started, choose an option:",
              "\n1. Create new Spreadsheet + local json.",
              "\n2. Enter the ID of an existing Spreadsheet.")
        return input("Choose option [1/2]: ")

    def newSpreadsheet(self):
        return input("Give your new Spreadsheet a name: ")

    def newLocalJson(self):
        return input("give your Json file a name: ") + ".json"

    def newShebang(self):

        print("\nEnter the Spreadsheet ID",
              "\n(Remove single ['] or double [\"]",
              "quotes from the ID first): ")
        return input()

    def getExistingSS(self):
        return input("Enter the Spreadsheet Id without \"\"\
                     \n[quotation marks]:  ")

