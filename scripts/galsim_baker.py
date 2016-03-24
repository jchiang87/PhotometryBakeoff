"""
Use GalSim to compute colors and execution times for LSST bands for a
grid of redshifts and the provided library of SEDs.
"""
import os
from collections import OrderedDict
import time
import numpy as np
import galsim

# Numbers for LSST.
_effective_diameter = 667. # cm
_exptime = 15. # s

class GalSimPhotometry(object):
    """
    Class to compute colors for LSST bands using the GalSim
    chromaticity tools.
    """
    def __init__(self, photometry_baker_dir='..'):
        """
        Read in the throughput data and SED filenames from the package
        data subfolder.
        """
        # Read throughput data for each band.
        bp_dir = os.path.join(photometry_baker_dir, 'data', 'bandpass')
        self.bandpasses = OrderedDict()
        for band in 'ugrizy':
            bp = galsim.Bandpass(os.path.join(bp_dir, 'total_%s.dat' % band))
            self.bandpasses[band] = bp.withZeropoint('AB', _effective_diameter,
                                                     _exptime)

        # Read the SED filenames.
        self.sed_dir = os.path.join(photometry_baker_dir, 'data', 'sed')
        self.sed_names = sorted([x for x in os.listdir(self.sed_dir)
                                 if 'spec' in x and 'ang' not in x])

    def colors(self, sed_name, redshift):
        """
        Return the ug, gr, ri, iz, zy colors and execution times for
        the specifed SED and redshift.
        """
        # Use the SED files that have the wavelength values converted
        # to Angstroms since the flux units are erg/cm^2/s/A.
        sed_fn = os.path.join(self.sed_dir, sed_name + ".ang")
        sed = galsim.SED(sed_fn, wave_type='Ang').atRedshift(redshift)
        tstart = time.time()
        my_mags = []
        for bp in self.bandpasses.values():
            flux = sed.calculateFlux(bp)
            my_mags.append(-2.5*np.log10(flux) + bp.zeropoint)
        time_spent = time.time() - tstart
        row = [mag0 - mag1 for mag0, mag1 in zip(my_mags[:-1], my_mags[1:])]
        row.extend([sed_name, redshift, time_spent])
        return tuple(row)

if __name__ == '__main__':
    phot_tool = GalSimPhotometry()
    redshift_grid = np.arange(0, 2.1, 0.2)
    with open('galsim_bakeoff_output.txt', 'w') as output:
        for redshift in redshift_grid:
            for sed_name in phot_tool.sed_names:
                output.write('%e %e %e %e %e %s %e %e\n' %
                             phot_tool.colors(sed_name, redshift))
