import makercore
import numpy as np
print "Hello from Python!\n"
makercore.hello_from_c()

block1 = makercore.Body.MakeBlock(1.,2.,1.)
block1.test()

block2 = makercore.Body.MakeBlock(.5,2.4,1.23)

thing = makercore.Body.DoUnion(block1, block2)

print thing

raw_input() # only to keep window open