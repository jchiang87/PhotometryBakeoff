import os
import numpy as np


i = 0
for f in os.listdir(os.getcwd()):
 
   if (f[:5]=="total" and f[-3:]=="dat"):
        print f
        #print f[:5], f[-3:]
        i+=1
        data = np.loadtxt(f)
        data[:,0]*=10.

        isNotFinite = np.invert(np.isfinite(data[:,1]))
        if len(data[isNotFinite,1])>0:
            print "File", f ,"has nan's"
        
        print "Saving", f+".ang"
        np.savetxt(f+".ang", data)



print "There were", i ,"files"
