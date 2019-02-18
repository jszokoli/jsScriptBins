import maya.cmds as cmds
import sys
import os
import getpass

import json

from . import settings
# scriptBin_Testing = True
# scriptBinPath = '/job/comms/pipeline/dev/jszokoli/scriptBin/'
# scriptBinLibraryName = 'scriptBinLibrary'
# descriptionDictName = 'descriptions'


class ScriptBins(object):

    def __init__(self):
        print 'Initialized jsScriptBins'

    def build_Script_Library_Dictionary(self):

        if os.path.isfile(settings.scriptBinPath+settings.scriptBinLibraryName+'.json' ):
            # print 'yep'
            scriptDict = self.readJson(settings.scriptBinPath, settings.scriptBinLibraryName )
        else:
            scriptDict = {}

        jsonFiles = []
        currentUser = getpass.getuser()

        userNames = os.listdir(settings.scriptBinPath)
        for user in userNames:
            #If Testing Update all of Dictionary
            if settings.scriptBin_Testing:
                currentUser = user
            if currentUser == user:
                #Clears User Dictionary
                scriptDict.pop(currentUser, None)
                #Check if child of directory is a file
                if os.path.isfile(settings.scriptBinPath+user):
                    #Checks Top Level Bin Folder for json files
                    topLevelFile = settings.scriptBinPath+user
                    if '.json' in topLevelFile:
                        jsonFiles.append(topLevelFile)
                else:
                    #If child of directory is another directory
                    userPath = settings.scriptBinPath+user+'/'
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

    def filterDictInformation(self,inputDict):
        print inputDict
        for k,v in inputDict.iteritems():
            print k,v


    def get_user_scripts_fromDict(self,inputDict,user):
        #print inputDict
        for k,v in inputDict.iteritems():
            if k == user[0]:
                return v

    def get_user_fromDict(self,inputDict):
        #print inputDict
        userList = []
        for k,v in inputDict.iteritems():
            userList.append(k)
        return userList

    def writeJson(self,fPath,fileName,dataIn):
        nodeDictionaryTest = json.dumps(dataIn)
        convertedNodeDict = json.loads(nodeDictionaryTest)
        #Write json
        #print fPath+fileName+'.json'
        with open(fPath+fileName+'.json', 'w') as outfile:
            json.dump(convertedNodeDict, outfile)


    def readJson(self,fPath,fileName):
        #Read json
        if os.path.isfile(fPath+fileName+'.json' ):
            with open(fPath+fileName+'.json') as json_data:
                convertedJsonData = json.load(json_data)
                return convertedJsonData


    def build_Script_Description_Dictionary(self):
        currentUser = getpass.getuser()
        # print settings.scriptBinPath+settings.scriptBinLibraryName
        if os.path.isfile(settings.scriptBinPath+settings.scriptBinLibraryName+'.json'  ):
            scriptDict = self.readJson(settings.scriptBinPath, settings.scriptBinLibraryName )
        else:
            scriptDict = {}

        if os.path.isfile(settings.scriptBinPath+currentUser+'/'+settings.descriptionDictName+'.json' ):
            descDict = self.readJson(settings.scriptBinPath+currentUser+'/', settings.descriptionDictName )
        else:
            descDict = {}
        jsonFiles = []

        # print scriptDict
        # print descDict
        userNames = os.listdir(settings.scriptBinPath)
        for user in userNames:
            if os.path.isdir(settings.scriptBinPath+user):
                #If Testing Update all of Dictionary
                # if settings.scriptBin_Testing:
                #     currentUser = user
                if currentUser == user:
                    for user,scripts in scriptDict.iteritems():
                        for script in scripts:
                            if script not in descDict:
                                descDict[script] = ""
        return descDict

    def register_Scripts(self,*args):
        currentUser = getpass.getuser()
        self.writeJson(settings.scriptBinPath,settings.scriptBinLibraryName, self.build_Script_Library_Dictionary() )
        self.writeJson(settings.scriptBinPath+currentUser+'/', settings.descriptionDictName, self.build_Script_Description_Dictionary() )




