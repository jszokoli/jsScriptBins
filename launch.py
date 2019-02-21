import sys
from os.path import expanduser
home = expanduser("~")
userPath = home+"/maya/scripts/jsTK/"
if userPath not in sys.path:
    sys.path.append(userPath)

import jsScriptBins.utilities
jsScriptBins.utilities.deleteModules('jsScriptBins')

import jsScriptBins
jsScriptBins.launch_ui()