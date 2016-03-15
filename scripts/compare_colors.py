import numpy as np
import pylab_plotter as plot
plot.pylab.ion()

names = 'ug gr ri iz zy sedname redshift time'.split()

lsst = np.recfromtxt('lsst_bakeoff_output.txt', names=names)
photozdc1 = np.recfromtxt('photozdc1_bakeoff_output.txt', names=names)
galsim = np.recfromtxt('galsim_bakeoff_output_zp_corr.txt', names=names)

# Test that sednames match.
for i in range(len(lsst['sedname']))[:10]:
    if lsst['sedname'][i] != photozdc1['sedname'][i].replace('_', '.'):
        print lsst['sedname'][i]

# Plot sims_photUtils color vs PhotoZDC1 color.
for color in names[:5]:
    win = plot.xyplot(lsst[color], photozdc1[color],
                      xname='sims_photUtils', yname='PhotoZDC1')
    plot.xyplot(lsst[color], galsim[color],
                xname='sims_photUtils', yname='GalSim',
                oplot=1, color='g')
    plot.xyplot(photozdc1[color], galsim[color],
                xname='sims_photUtils', yname='GalSim',
                oplot=1, color='r')
    plot.curve([-10, 10], [-10, 10], oplot=1, lineStyle=':')
    win.set_title(color)

for color in names[:5]:
    win = plot.histogram(photozdc1[color] - lsst[color])
    plot.histogram(galsim[color] - lsst[color], oplot=1, color='g')
    win.set_title(color)

xrange = (-2, -0.5)
plot.histogram(np.log10(lsst['time']), xrange=xrange)
plot.histogram(np.log10(photozdc1['time']), oplot=1, color='r', xrange=xrange)
plot.histogram(np.log10(galsim['time']), oplot=1, color='g', xrange=xrange)
