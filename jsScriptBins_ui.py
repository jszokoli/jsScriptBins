import maya.cmds as cmds
import sys
import os
import getpass
import json
import subprocess


from . import jsScriptBinsCore
from . import settings

# scriptBin_Testing = True
# scriptBinPath = '/job/comms/pipeline/dev/jszokoli/scriptBin/'
# scriptBinLibraryName = 'scriptBinLibrary'
# descriptionDictName = 'descriptions'


class ScriptBins_ui(object):

    def __init__(self):
        print 'Initialized jsScriptBins_ui'
        self.SB = jsScriptBinsCore.ScriptBins()
        

    if sys.platform == 'darwin':
        def openFolder(self, path):
            subprocess.check_call(['open', '--', path])
    elif sys.platform == 'linux2':
        def openFolder(self, path):
            subprocess.check_call(['nautilus', '--', path])
    elif sys.platform == 'win32':
        def openFolder(self, path):
            subprocess.check_call(['explorer', path])


    def load_user_python_file(self, scriptPath, selectedScript, fullScriptPath):
        # print scriptPath
        if scriptPath not in sys.path:
            sys.path.append(scriptPath)
        #print selectedScript
        cmds.evalDeferred("execfile('{0}')".format(scriptPath+selectedScript))


    def load_python_file(self, scriptPath, selectedScript, fullScriptPath):
        # print scriptPath
        if scriptPath not in sys.path:
            sys.path.append(scriptPath)
        # print selectedScript
        cmds.evalDeferred("execfile('{0}')".format(fullScriptPath))
        # cmds.evalDeferred("import %s;%s.launch_ui()") %selectedScript


    def load_python_module(self, scriptPath,selectedScript,fullScriptPath):
        cmds.warning('Create Package Launcher .py file for packages')
        # packagePath = fullScriptPath[:-11]
        # print packagePath
        # packageName = selectedScript[:-12]
        # print packageName
        # if packagePath not in sys.path:
        #     sys.path.append(packagePath)
        # #LINK TO UTILITIES
        # deleteModules(packageName)
        # cmds.evalDeferred("import %s; %s.launch_ui()" %(packageName, packageName) ) 


    def ui_open_user_folder(self, *args):
        currentUser = getpass.getuser()
        if os.path.isdir(settings.scriptBinPath+currentUser):
            self.openFolder(settings.scriptBinPath+currentUser)
        else:
            os.mkdir(settings.scriptBinPath+currentUser)
            self.openFolder(settings.scriptBinPath+currentUser)


    def updateDescriptionJson(self, *args):
        newDescriptionValue = cmds.scrollField('ui_description_textField',query=True,tx=True)
        print newDescriptionValue
        cmds.deleteUI('ui_Description')
        currentUser = cmds.textScrollList('UserScrollList',query=True,selectItem=True) or None
        if currentUser[0] != "All":
            currentScript = cmds.textScrollList('ScriptScrollList',query=True,selectItem=True)[0] or None
            if os.path.isfile(settings.scriptBinPath+currentUser[0]+'/'+settings.descriptionDictName+'.json'):
                jsonIn = self.SB.readJson(settings.scriptBinPath+currentUser[0]+'/' ,settings.descriptionDictName )
                for script, description in jsonIn.iteritems():
                    if currentScript == script:
                        jsonIn[script] = newDescriptionValue
                        # print jsonIn
                        self.SB.writeJson(settings.scriptBinPath+currentUser[0]+'/', settings.descriptionDictName, jsonIn )
                        cmds.scrollField('descriptionField',edit=True,tx=newDescriptionValue)
            else:
                print "Can't Find Description Json."
        else:
            pass

    def ui_updateDescriptionJson(self, args=None):
        currentUser = cmds.textScrollList('UserScrollList',query=True,selectItem=True) or None

        currentScript = cmds.textScrollList('ScriptScrollList',query=True,selectItem=True) or None
        if currentUser != None:
            if currentUser != ['All']:
                StarterText = cmds.scrollField('descriptionField',query=True,tx=True)

                #If window exists delete 
                if cmds.window('ui_Description', exists=True):
                    cmds.deleteUI('ui_Description')
                #Create Initial Window
                cmds.window('ui_Description', title= 'jsScriptBins Description Editor', s = False, widthHeight=[400, 400])
                cmds.columnLayout()
                cmds.scrollField('ui_description_textField',
                editable=True,
                w=398,
                h=350,
                wordWrap=True,
                text=StarterText )
                cmds.button('Updated Description',w=398,h=50,c=self.updateDescriptionJson)
                cmds.setParent('..')
                cmds.showWindow( 'ui_Description' )


    def ui_switch_to_user_scripts(self, *args):
        currentUser = cmds.textScrollList('UserScrollList',query=True,selectItem=True) or None
        if currentUser != ["All"]:
            # print currentUser
            cmds.textScrollList('ScriptScrollList', edit = True, removeAll = True)

            if os.path.isfile(settings.scriptBinPath+settings.scriptBinLibraryName+'.json'):
                jsonIn = self.SB.readJson(settings.scriptBinPath,settings.scriptBinLibraryName )

                userScripts = self.SB.get_user_scripts_fromDict(jsonIn,currentUser)
                cmds.textScrollList('ScriptScrollList', edit = True, append = userScripts)
                cmds.scrollField('descriptionField',edit=True,tx="")
        else:
            self.ui_switch_to_allUsers_scripts()



    def ui_switch_to_allUsers_scripts(self, *args):
        #currentUser = "All"
        # print currentUser
        scriptDict = self.SB.readJson(settings.scriptBinPath,settings.scriptBinLibraryName)
        userNameList = []
        for userName,scripts in scriptDict.iteritems():
            userNameList.append(userName)
        cmds.textScrollList('ScriptScrollList', edit = True, removeAll = True)
        fullUserScripts = []
        for user in userNameList:
            if os.path.isfile(settings.scriptBinPath+settings.scriptBinLibraryName+'.json'):
                jsonIn = self.SB.readJson(settings.scriptBinPath,settings.scriptBinLibraryName )
                userScripts = self.SB.get_user_scripts_fromDict(jsonIn,[user])
                for script in userScripts:
                    fullUserScripts.append(user+'/'+script)

        cmds.textScrollList('ScriptScrollList', edit = True, append = fullUserScripts)
        cmds.scrollField('descriptionField',edit=True,tx="")



    def ui_switch_script_description(self, *args):
        currentUser = cmds.textScrollList('UserScrollList',query=True,selectItem=True)or None
        currentScript = cmds.textScrollList('ScriptScrollList',query=True,selectItem=True)[0]
        if currentUser[0] != "All":
            if os.path.isfile(settings.scriptBinPath+currentUser[0]+'/'+settings.descriptionDictName+'.json'):
                jsonIn = self.SB.readJson(settings.scriptBinPath+currentUser[0]+'/' ,settings.descriptionDictName )
                for script, description in jsonIn.iteritems():
                    if currentScript == script:
                        jsonDescription = jsonIn[script]
                        cmds.scrollField('descriptionField',edit=True,tx=jsonDescription)
            else:
                #print "Can't Find Description Json."
                cmds.scrollField('descriptionField',edit=True,tx="Can't Find Description Json.")
        else:
            if os.path.isfile(settings.scriptBinPath+currentScript.split('/')[0]+'/'+settings.descriptionDictName+'.json'):
                jsonIn = self.SB.readJson(settings.scriptBinPath+currentScript.split('/')[0]+'/', settings.descriptionDictName )
                for script, description in jsonIn.iteritems():
                    if script in currentScript:
                        jsonDescription = jsonIn[script]
                        cmds.scrollField('descriptionField',edit=True,tx=jsonDescription)
            else:
                #print "Can't Find Description Json."
                cmds.scrollField('descriptionField',edit=True,tx="Can't Find Description Json.")


    def ui_run_selected_script(self, *args):
        currentUser = cmds.textScrollList('UserScrollList',query=True,selectItem=True)or[]
        selectedScript = cmds.textScrollList('ScriptScrollList',query=True,selectItem=True)or []

        if len(currentUser) > 0:
            currentUser=currentUser[0]
        else:
            currentUser='DONTDO'

        if len(selectedScript) > 0:
            selectedScript=selectedScript[0]
        else:
            selectedScript='DONTDO'

        fullScriptPath = settings.scriptBinPath+currentUser+'/'+selectedScript
        # print currentUser
        if currentUser != "All":
            scriptPath = settings.scriptBinPath+currentUser+'/'
        else:
            scriptPath = settings.scriptBinPath
        # print settings.scriptBinPath
        if 'DONTDO' not in fullScriptPath:
            if '/' in selectedScript:
                if currentUser == "All":
                    self.load_user_python_file(scriptPath,selectedScript,fullScriptPath)
                else:
                    self.load_python_module(scriptPath,selectedScript,fullScriptPath)
            else:
                # print 'THIS AINT A MODULE'
                self.load_python_file(scriptPath,selectedScript,fullScriptPath)



    def ui_searchScripts(self, *args):
        currentSearchField = cmds.textField('scriptBinSearchField',query=True,text=True)

        currentUser = cmds.textScrollList('UserScrollList',query=True,selectItem=True) or None
        if currentUser != None:
            if currentUser[0] != 'All':
                if os.path.isfile(settings.scriptBinPath+settings.scriptBinLibraryName+'.json'):
                    jsonIn = self.SB.readJson(settings.scriptBinPath,settings.scriptBinLibraryName )

                    userScripts = self.SB.get_user_scripts_fromDict(jsonIn,currentUser)
                    filteredScripts = []
                    for userScript in userScripts:
                        if currentSearchField.lower() in userScript.lower():
                            filteredScripts.append(userScript)
                    cmds.textScrollList('ScriptScrollList', edit = True, removeAll = True)
                    cmds.textScrollList('ScriptScrollList', edit = True, append = filteredScripts)
                    cmds.scrollField('descriptionField',edit=True,tx="")
            else: 
                if os.path.isfile(settings.scriptBinPath+settings.scriptBinLibraryName+'.json'):
                    jsonIn = self.SB.readJson(settings.scriptBinPath,settings.scriptBinLibraryName )
                    userList =  self.SB.get_user_fromDict(jsonIn)
                    filteredScripts = []
                    for user in userList:
                        userScripts = self.SB.get_user_scripts_fromDict(jsonIn,[user])
                        for userScript in userScripts:
                            if currentSearchField.lower() in userScript.lower():
                                filteredScripts.append(user+'/'+userScript)
                    cmds.textScrollList('ScriptScrollList', edit = True, removeAll = True)
                    cmds.textScrollList('ScriptScrollList', edit = True, append = filteredScripts)
                    cmds.scrollField('descriptionField',edit=True,tx="")






    def ui_ScriptBins(self):

        scriptDict = self.SB.readJson(settings.scriptBinPath,settings.scriptBinLibraryName ) or {}
        print scriptDict
        #If window exists delete 
        if cmds.window('ui_ScriptBins', exists=True):
            cmds.deleteUI('ui_ScriptBins')

        #Create Initial Window
        mainWindow = cmds.window('ui_ScriptBins', title= 'jsScriptBins',menuBar=True)
        cmds.menu( label='Edit', tearOff=True ,parent='ui_ScriptBins' )
        cmds.frameLayout("ScriptEdit")

        cmds.flowLayout()
        cmds.iconTextStaticLabel( st='iconOnly', i1='search.png')
        cmds.textField('scriptBinSearchField',w=224,textChangedCommand = self.ui_searchScripts)
        cmds.button('Open Folder',c=self.ui_open_user_folder)
        cmds.button('Edit Description',c=self.ui_updateDescriptionJson )
        cmds.button('Register Scripts', c = self.SB.register_Scripts )
        cmds.setParent('..')
        userNameList = ['All']
        scriptList = []

        for userName,scripts in scriptDict.iteritems():
            userNameList.append(userName)
            scriptList.append(scripts)
            
        #print userNameList,scriptList

        #testList1 = ['jszokoli','msohn']
        cmds.flowLayout()

        cmds.columnLayout(w=150)

        cmds.textScrollList('UserScrollList',
        w=150,
        h=200,
        append=userNameList,
        selectCommand= self.ui_switch_to_user_scripts )

        cmds.setParent('..')

        cmds.columnLayout(w=200)

        cmds.textScrollList('ScriptScrollList',
        w=200,
        h=200,
        selectCommand = self.ui_switch_script_description)

        cmds.setParent('..')

        cmds.columnLayout(w=220)
        #cmds.textField('descriptionField',w=145,h=175,tx='',ed=0)
        cmds.scrollField('descriptionField',w=145,h=175,tx='',ed=0,wordWrap=True)
        cmds.button('RunScript',w=145,l='Execute Selected Script',c=self.ui_run_selected_script)
        # cmds.button()
        # cmds.button()
        cmds.setParent('..')

        cmds.setParent('..')
        #cmds.button()
        cmds.setParent('..')

        cmds.showWindow( 'ui_ScriptBins' )
        cmds.window('ui_ScriptBins', edit=True, s = False, widthHeight=[500, 275])
        #cmds.window('ui_ScriptBins', query=True, widthHeight=True)

    #print cmds.window('ui_ScriptBins', query=True, widthHeight=True)

#self.ui_ScriptBins( self.SB.readJson(settings.scriptBinPath,settings.scriptBinLibraryName ) )


def launch_ui():
    uiObject = ScriptBins_ui()
    uiObject.ui_ScriptBins()
    #register_Scripts()


