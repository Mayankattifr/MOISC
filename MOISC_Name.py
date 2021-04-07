# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 12:20:09 2020

@author: Mayank
"""

from astroquery.simbad import Simbad
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from urllib.parse import quote
import numpy as np
from astropy.wcs import WCS
from astropy.visualization import (MinMaxInterval, SqrtStretch, AsinhStretch,ImageNormalize)


width = 150
height = 150
fov = 0.01

case= input("1 for SIMABD Name or 2 for RA DEC in degs:")
print(case)
case=int(case)

if (case==1):
    num = input("Enter SIMABD Name :") 
    obj = num
    sc = SkyCoord.from_name(obj)
    ra = sc.icrs.ra.deg
    dec = sc.icrs.dec.deg

elif (case==2):
    ra=input('RA: ')
    dec= input('DEC: ')    
    obj=str(ra)+str(dec)
    ra=float(ra)
    dec=float(dec)

    

fov =input ("Enter cutout size :") 

hips_list = ['PanSTARRS/DR1/g', 'PanSTARRS/DR1/z', '2MASS/J', '2MASS/H', '2MASS/K', 'AllWISE/W3','AllWISE/W2','AllWISE/W1','AllWISE/W4']






for hips in hips_list:
    url = 'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?hips={}&width={}&height={}&fov={}&projection=TAN&coordsys=icrs&ra={}&dec={}'.format(quote(hips), width, height, fov, ra, dec)
    hdu = fits.open(url)
    wcs = WCS(hdu[0].header)
    plt.figure()
    plt.subplot(projection=wcs)
    im = hdu[0].data
    norm = ImageNormalize(im, interval=MinMaxInterval(),
                  stretch=AsinhStretch())
    file_name = '{}-{}.png'.format(obj, hips.replace('/', '_'))
    plt.imshow(im, cmap='magma', norm=norm,origin='lower')
    px, py = wcs.wcs_world2pix(ra, dec, 1)
    plt.scatter(px,py,c='g',s=100)
    plt.title('{} - {}'.format(obj, hips))
    plt.xlabel('RA')
    plt.ylabel('DEC')
    print(file_name)
    plt.savefig(file_name)
        