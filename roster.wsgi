

import sys, os
sys.path.insert (0,'/var/www/roster')
os.chdir("/var/www/roster")

#activate_this = '/var/www/roster/venv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

from roster import app as application

