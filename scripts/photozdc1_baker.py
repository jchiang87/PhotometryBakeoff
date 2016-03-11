"""Bake off script for PhotoZDC1
   
   Returns a numpy record array of LSST colors for each galaxy SED at a grid of redshifts

   To run this script, add location of PhotoZDC1/src to your PYTHONPATH environment 
   variable
"""
import sys
import numpy as np
import time

try:
    import sedFilter
    import photometry as phot
except ImportError:
    emsg = "You must add location of PhotoZDC1/src to your PYTHONPATH environment "
    emsg += "variable"
    raise ImportError(emsg)


def bake(): 

	# get SED list
	listOfSedsFile = "lsst.seds"
	sedLib = sedFilter.createSedDict(listOfSedsFile, "../data/sed/")
	sedList = sedLib.keys()
	nSED = len(sedLib)


	# get LSST filters
	listOfFiltersFile = "lsst.filters"
	filterLib = sedFilter.createFilterDict(listOfFiltersFile, "../data/bandpass/")
	filterList = sedFilter.orderFiltersByLamEff(filterLib)
	nFilter = len(filterLib)


	# instantiate photometric calculations
	pcalcs = []
	for sedname, sed in sedLib.items():
		pcalcs.append(phot.PhotCalcs(sed, filterLib))


	# redshift grid
	zgrid = np.arange(0, 2., 0.2)
	nz = len(zgrid)


	# output file (for checking)
	#fout = open('bake_off.txt', 'w')

	# record array to return
	records = np.recarray((nz*nSED,),
				dtype=[('redshift', float), ('sedname', str), ('ug', float), ('gr', float), 
					   ('ri', float), ('iz', float), ('zy', float), ('time', float) ]) 

    # loop over redshifts
	for z in zgrid:

        # each SED in lib
		for ised, sedname in enumerate(sedList):
			#fout.write(str(z) + "  " + sedname + "  ")
	
	        # time calculation of *all* colors for this redshift+SED
			start_time = time.time()
			colors = []
			for ifilt in range(nFilter-1):
		
				mag = pcalcs[ised].computeColor(filterList[ifilt], filterList[ifilt+1], z)
				colors.append(mag)
				#fout.write(str(mag) + "  ")
			
			end_time = time.time()
			#fout.write(str(end_time-start_time) + "\n")
		
		
		    # add to record array
			rec = np.array([(z, sedname, colors[0], colors[1], colors[2], colors[3], 
							 colors[4], end_time-start_time)], dtype=records.dtype)
							 
			records = np.append(records, rec)

		 
	#fout.close()
	return records
	
	
def main(argv):
    print bake()

if __name__ == "__main__":
    main(sys.argv[1:])