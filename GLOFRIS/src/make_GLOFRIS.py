from distutils.core import setup
from bbfreeze import Freezer
import os


#vers=os.system('svnversion -n')
#print vers
#Binary dist
f = Freezer("../bin")
f.addScript("GLOFRIS.py")
#f.addScript("GLOFRIS_utils.py")
#f.addScript("changeGLCC.py")
#f.addScript("GLCC2PCRGLOB.py")
#f.addScript("GLOFRIS_risk.py")
#f.addScript("post_proc.py")
f()    # starts the freezing process
