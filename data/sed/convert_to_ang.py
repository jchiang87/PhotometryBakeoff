import os
import numpy as np


i = 0
for f in os.listdir(os.getcwd()):
 
   if f[-4:]=="spec":
        #print f
        i+=1
        data = np.loadtxt(f)
        data[:,0]*=10.

        isNotFinite = np.invert(np.isfinite(data[:,1]))
        if len(data[isNotFinite,1])>0:
            print "File", f ,"has nan's"
        
        np.savetxt(f+".ang", data)



print "There were", i ,"files"
