import sys
from os.path import expanduser
home = expanduser("~")
sys.path.append(home+"/maya/scripts/jsTK/")

import jsScriptBins.utilities
jsScriptBins.utilities.deleteModules('jsScriptBins')

import jsScriptBins
jsScriptBins.launch_ui()