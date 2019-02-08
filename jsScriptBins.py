import maya.cmds as cmds
import sys
import os
import getpass

import json


scriptBin_Testing = True
scriptBinPath = '/job/comms/pipeline/dev/jszokoli/scriptBin/'
scriptBinLibraryName = 'scriptBinLibrary'
descriptionDictName = 'descriptions'

def build_Script_Library_Dictionary():

    if os.path.isfile(scriptBinPath+scriptBinLibraryName+'.json' ):
        # print 'yep'
        scriptDict = readJson(scriptBinPath, scriptBinLibraryName )
    else:
        scriptDict = {}

    jsonFiles = []
    currentUser = getpass.getuser()

    userNames = os.listdir(scriptBinPath)
    for user in userNames:
        #If Testing Update all of Dictionary
        if scriptBin_Testing:
            currentUser = user
        if currentUser == user:
            #Clears User Dictionary
            scriptDict.pop(currentUser, None)
            #Check if child of directory is a file
            if os.path.isfile(scriptBinPath+user):
                #Checks Top Level Bin Folder for json files
                topLevelFile = scriptBinPath+user
                if '.json' in topLevelFile:
                    jsonFiles.append(topLevelFile)
            else:
                #If child of directory is another directory
                userPath = scriptBinPath+user+'/'
                childrenFiles = os.listdir(userPath)
                scripts = []
                fileDescriptionJson = []
                for file in childrenFiles:
                    if '.json' in file:
                        fileDescriptionJson.append(file)
                    else:
                        #checkIfDirPackage
                        if os.path.isfile(userPath+file):
                            if 'py' or 'mel' in packageChildren:
                                scripts.append(file)
                        else:
                            packageChildren = os.listdir(userPath+file)
                            if '__init__.py' in packageChildren:
                                pass
                                #scripts.append(file+'/'+'__init__.py')


                scriptDict[user] = scripts
    # print jsonFile
    return scriptDict

def filterDictInformation(inputDict):
    print inputDict
    for k,v in inputDict.iteritems():
        print k,v

# filterDictInformation( build_Script_Library_Dictionary() )


def get_user_scripts_fromDict(inputDict,user):
    #print inputDict
    for k,v in inputDict.iteritems():
        if k == user[0]:
            return v

def get_user_fromDict(inputDict):
    #print inputDict
    userList = []
    for k,v in inputDict.iteritems():
        userList.append(k)
    return userList
#filterDictInformation( build_Script_Library_Dictionary() )



def writeJson(fPath,fileName,dataIn):
    nodeDictionaryTest = json.dumps(dataIn)
    convertedNodeDict = json.loads(nodeDictionaryTest)
    #Write json
    #print fPath+fileName+'.json'
    with open(fPath+fileName+'.json', 'w') as outfile:
        json.dump(convertedNodeDict, outfile)


def readJson(fPath,fileName):
    #Read json
    with open(fPath+fileName+'.json') as json_data:
        convertedJsonData = json.load(json_data)
        return convertedJsonData


def build_Script_Description_Dictionary():
    currentUser = getpass.getuser()
    # print scriptBinPath+scriptBinLibraryName
    if os.path.isfile(scriptBinPath+scriptBinLibraryName+'.json'  ):
        scriptDict = readJson(scriptBinPath, scriptBinLibraryName )
    else:
        scriptDict = {}

    if os.path.isfile(scriptBinPath+currentUser+'/'+descriptionDictName+'.json' ):
        descDict = readJson(scriptBinPath+currentUser+'/', descriptionDictName )
    else:
        descDict = {}
    jsonFiles = []

    # print scriptDict
    # print descDict
    userNames = os.listdir(scriptBinPath)
    for user in userNames:
        if os.path.isdir(scriptBinPath+user):
            #If Testing Update all of Dictionary
            # if scriptBin_Testing:
            #     currentUser = user
            if currentUser == user:
                for user,scripts in scriptDict.iteritems():
                    for script in scripts:
                        if script not in descDict:
                            descDict[script] = ""
    return descDict

def register_Scripts(*args):
    writeJson(scriptBinPath,scriptBinLibraryName, build_Script_Library_Dictionary() )
    writeJson(scriptBinPath+currentUser+'/', descriptionDictName, build_Script_Description_Dictionary() )



#register_Scripts()