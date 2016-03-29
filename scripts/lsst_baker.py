"""
This is the code that will actually calculate magnitudes using the LSST
Sims stack
"""

try:
    from lsst.sims.photUtils import Sed, Bandpass
except:
    raise RuntimeError("It does not appear that you can import the LSST "
                       + "sims stack.  Are you sure you set it up?")

import os
import time
import numpy as np
from get_sed_names import get_sed_names


def run_lsst_baker(redshift_grid, sed_list=None):
    """
    Accepts a redshift grid (a numpy array).  Reads in all of the SEDs from
    ../data/sed/ and the calculates their colors in all of the lsst bands,
    given those redshifts

    Returns a structured numpy array containing
    sedname
    redshift
    ug
    gr
    ri
    iz
    zy
    time (the time spent calculating the magnitudes)
    """
    bandpass_dir = os.path.join('..', 'data', 'bandpass')
    bandpass_list = []
    for bp_name in ('total_u.dat', 'total_g.dat', 'total_r.dat', 'total_i.dat',
                    'total_z.dat', 'total_y.dat'):

        bp = Bandpass()
        bp.readThroughput(os.path.join(bandpass_dir, bp_name))
        bandpass_list.append(bp)

    sed_dir = os.path.join('..', 'data', 'sed')
    if sed_list is None:
        list_of_sed_names = sorted([nn for nn in os.listdir(sed_dir)
                                    if 'spec' in nn and 'ang' not in nn])
    else:
        list_of_sed_names = get_sed_names(os.path.join(sed_dir, sed_list))

    n_rows = len(list_of_sed_names)*len(redshift_grid)
    dtype = np.dtype([('sedname', str, 300), ('redshift', np.float),
                      ('ug', np.float), ('gr', np.float), ('ri', np.float),
                      ('iz', np.float), ('zy', np.float), ('time', np.float)])

    dummy = ('aaaa', 1.0, 1, 1, 1, 1, 1, 1.0)
    output_array = np.array([dummy]*n_rows, dtype=dtype)

    i_row = 0
    for redshift in redshift_grid:
        for sed_name in list_of_sed_names:
            ss = Sed()
#            t_start = time.clock()
            t_start = time.time()
            ss.readSED_flambda(os.path.join(sed_dir, sed_name))
            ss.redshiftSED(redshift)
            local_list = []
            for bp in bandpass_list:
                mm = ss.calcMag(bp)
                local_list.append(mm)
            #print local_list[0], local_list[1], local_list[0]-local_list[1]
#            time_spent = time.clock()-t_start
            time_spent = time.time()-t_start
            output_array[i_row][0] = sed_name
            output_array[i_row][1] = redshift
            output_array[i_row][2] = local_list[0]-local_list[1]
            output_array[i_row][3] = local_list[1]-local_list[2]
            output_array[i_row][4] = local_list[2]-local_list[3]
            output_array[i_row][5] = local_list[3]-local_list[4]
            output_array[i_row][6] = local_list[4]-local_list[5]
            output_array[i_row][7] = time_spent
            i_row += 1

    return output_array


if __name__ == "__main__":
#    sed_list = None
#    outfile = 'lsst_bakeoff_output.txt'
    sed_list = 'lsst_2.seds'
    outfile = 'lsst_bakeoff_output_2.txt'

    print "\n\nNOTE: running this script will produce a text file:"
    print "%s\n\n" % outfile
    redshift_grid = np.arange(0, 2.1, 0.2)
    recarr = run_lsst_baker(redshift_grid, sed_list=sed_list)
    with open(outfile, 'w') as output_file:
        for ug, gr, ri, iz, zy, name, redshift, time in \
        zip(recarr['ug'], recarr['gr'], recarr['ri'],
            recarr['iz'], recarr['zy'], recarr['sedname'],
            recarr['redshift'], recarr['time']):
            output_file.write('%e %e %e %e %e %s %e %e\n' %
                              (ug, gr, ri, iz, zy, name, redshift, time))
