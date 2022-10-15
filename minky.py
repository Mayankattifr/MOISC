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

plt.ioff()
width = 250
height = 250
fov = 0.005

import pandas as pd

df=pd.read_csv('list_ADFOSC.csv')


name=np.array(df['Name'])
    

fov =0.05
hips_list = ['PanSTARRS/DR1/z']

i=0
ap=[]
while(i<len(name)):

    obj = name[i]
    sc = SkyCoord.from_name(obj)
    ra = sc.icrs.ra.deg
    dec = sc.icrs.dec.deg
    for hips in hips_list:
        url = 'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?hips={}&width={}&height={}&fov={}&projection=TAN&coordsys=icrs&ra={}&dec={}'.format(quote(hips), width, height, fov, ra, dec)
        hdu = fits.open(url)
        wcs = WCS(hdu[0].header)
        plt.figure()
        plt.subplot(projection=wcs)
        im = hdu[0].data
        norm = ImageNormalize(im, interval=MinMaxInterval(),
                      stretch=AsinhStretch())
        file_name = '{}-{}.jpg'.format(obj, hips.replace('/', '_'))
        ap.append(file_name)
        plt.imshow(im, cmap='Greys', norm=norm,origin='lower')
        px, py = wcs.wcs_world2pix(ra, dec, 1)
        plt.scatter(px,py,c='g',s=50)
        plt.title('{} - {}'.format(obj, hips))
        plt.xlabel('RA')
        plt.ylabel('DEC')
        print(file_name)
        plt.savefig(file_name)
    i=i+1
        
    
#%%

import img2pdf








with open("Finding_chart.pdf", "wb") as f:
    f.write(img2pdf.convert([ap for ap in ap]))
