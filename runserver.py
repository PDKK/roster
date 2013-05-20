#!/usr/bin/python
from roster import app
import roster.models 

import sys, getopt

def main(argv):
    _init_db = False
    _add_test_data = False
    try:
        opts, args = getopt.getopt(argv,"h",["init-db","init-test-db"])
    except getopt.GetoptError:
        print 'runserver.py [--init-db | --init-test-db] '
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'runserver.py [--init-db | --init-test-db]'
            sys.exit()
        elif opt in ("--init-db"):
            _init_db = True
        elif opt in ("--init-test-db"):
            _init_db = True
            _add_test_data = True
    if _init_db:
        roster.models.init_db()
        sys.exit()
    if _add_test_data:
        roster.models.init_db()
        roster.models.add_test_data()
        sys.exit()
    app.run(host='0.0.0.0',debug=True)
   

if __name__ == "__main__":
   main(sys.argv[1:])


