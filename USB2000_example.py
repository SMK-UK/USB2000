"""
Example script for controlling the Ocean Optics USB2000+ Spectrometer

Author: Sean Keenan
GitHub: SMK-UK
Date: 13/02/2024

"""

# import the relevant class
from OSA2000 import USB2000

# initialise the device
OSA = USB2000()
# set integration time of the device
OSA.set_int_time(10000)
# take a signel shot spectra: returns [wavelength, intensities]
single = OSA.take_spectra()
# take averaged spectra: returns [wavelength, intensities]
averaged = OSA.take_average(n_samples=10)
# disconnect from the device
OSA.disconnect()
