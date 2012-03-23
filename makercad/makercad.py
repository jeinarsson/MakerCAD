
DEBUG = True

if DEBUG:
    import sys
    print sys.path[0]
    sys.path.append(sys.path[0]+'/../adm/vs2010/Debug')

import makercore

print "Hello from Python!\n"
makercore.hello_from_c()

raw_input() # only to keep window open