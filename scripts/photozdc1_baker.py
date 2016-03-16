"""Bake off script for PhotoZDC1

   Returns a numpy record array of LSST colors for each galaxy SED at
   a grid of redshifts

   To run this script, add location of PhotoZDC1/src to your
   PYTHONPATH environment variable
"""
import sys
import numpy as np
import time

import sedFilter
import photometry as phot

def bake(zgrid):
    # get SED list
    listOfSedsFile = "lsst.seds"
    sedLib = sedFilter.createSedDict(listOfSedsFile, "../data/sed/")
    sedList = sorted(sedLib.keys())
    nSED = len(sedLib)

    # get LSST filters
    listOfFiltersFile = "lsst.filters"
    filterLib = sedFilter.createFilterDict(listOfFiltersFile,
                                           "../data/bandpass/")
    filterList = sedFilter.orderFiltersByLamEff(filterLib)
    nFilter = len(filterLib)

    # instantiate photometric calculations
    pcalcs = {}
    for sedname, sed in sedLib.items():
        pcalcs[sedname] = phot.PhotCalcs(sed, filterLib)

    nz = len(zgrid)

    # record array to return
    n_rows = nSED*nz
    dtype = np.dtype([('sedname', str, 300), ('redshift', np.float),
                      ('ug', np.float), ('gr', np.float), ('ri', np.float),
                      ('iz', np.float), ('zy', np.float), ('time', np.float)])
    dummy = ('aaaa', 1.0, 1, 1, 1, 1, 1, 1.0)
    records = np.array([dummy]*n_rows, dtype=dtype)

    i = 0
    # loop over redshifts
    for z in zgrid:
        # each SED in lib
        for sedname in sedList:
            # time calculation of *all* colors for this redshift+SED
            start_time = time.time()
            colors = []
            for ifilt in range(nFilter-1):
                mag = pcalcs[sedname].computeColor(filterList[ifilt],
                                                   filterList[ifilt+1], z)
                colors.append(mag)
            end_time = time.time()
            rec = np.array([(sedname, z, colors[0], colors[1], colors[2],
                             colors[3], colors[4], end_time-start_time)],
                           dtype=records.dtype)
            records[i] = rec
            i += 1

    return records

if __name__ == '__main__':
    zgrid = np.arange(0, 2.1, 0.2)
    records = bake(zgrid)
    with open('photozdc1_bakeoff_output.txt', 'w') as output:
        for ug, gr, ri, iz, zy, name, redshift, time in \
            zip(records['ug'], records['gr'], records['ri'], records['iz'],
                records['iz'], records['sedname'], records['redshift'],
                records['time']):
            output.write('%e %e %e %e %e %s %e %e\n' %
                         (ug, gr, ri, iz, zy, name, redshift, time))
