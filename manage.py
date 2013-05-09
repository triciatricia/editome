#!/usr/bin/env python
import os
import sys
sys.path.append("/afs/ir/users/g/o/gokulr/cgi-bin/python_virtualenv/lib/python2.7/site-packages")
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "editdatabase.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
