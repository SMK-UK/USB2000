'''
Class for using Ocean Optics Spectrometers

Author: Sean Keenan
Date: 12/02/2024
GitHub: SMK-UK

'''

# import relevant modules
from numpy import array
import seabreeze.spectrometers as sb
import time

class USB2000():

    def __init__(self, verbose=True, display=False):
        '''
        initialise the class for communicating with 
        an Ocean Optics Spectrometer
        
        '''        
        self.display = display
        self.verbose = verbose
        # connect to device
        self.connect()
        
    def connect(self):
        '''
        Attempt to connect to an available device
        
        '''
        try:
            devices = sb.list_devices()
            # throw error if no device connected
            if len(devices) == 0:
                print("No spectrometer found, please check connection")
                return False
            # connect to solo device
            elif len(devices) == 1:
                self.device = devices[0]
                if self.verbose:
                    print(f"Attempting connection to {self.device}")
            # handle case of multiple spectrometers
            else:
                print("Multiple spectrometers found:")
                # loop through available devices
                for i, device in enumerate(devices):
                    print(f"{i+1}. {device}")
                # user enter correct device
                while True:
                    choice = input(f'Please enter spectrometer number (1-{len(devices)}): ')
                    try:
                        index = int(choice) - 1
                        self.device = devices[index]
                        break
                    except (ValueError, IndexError):
                        print("Invalid input, please enter a valid number")
            # connect to appropriate device
            self.spectrometer = sb.Spectrometer(self.device)
            time.sleep(0.2)             # wait for connection to establish
            self.device_name = self.spectrometer.model
            time.sleep(0.2)             # wait before executing new commands

            print(f"Connection to device {self.device_name} successful!")
        
        # raise error if connection fails
        except Exception as e:
            print(f"Error connecting to device {e}")
            return False
            
    def disconnect(self):
        '''
        Disconnect from the device

        '''
        try:
            # attempt to disconnect
            if self.spectrometer is not None:
                self.spectrometer.close()
                print('Spectrometer Disconnected')

        # throw error if no spectrometer connected
        except (NameError, AttributeError):
            print("No Spectrometer Connected!")
        
    def get_config(self):
        '''
        Returns the config of the device:

        Serial Number
        Max intensity (AU)
        Integration Time Limits
        Integration Time
        
        '''
        config = {'serial no.': self.spectrometer.serial_number,
                  'Max Intensity': self.spectrometer.max_intensity,
                  'Integration time limits': self.spectrometer.integration_time_micros_limits,
                  'Integration time': self.int_time}

        if self.verbose:
            print(config)

        return config
    
    def set_int_time(self, int_time=1):
        '''
        Set the integration time of the spectrometer
        
        <int_time>:
            Integration time in us
        
        '''
        self.int_time = int_time
        self.spectrometer.integration_time_micros(self.int_time)
        time.sleep(0.1)
        if self.verbose:
            save_verbose = self.verbose
            self.verbose = False
            set_time = self.get_config()['Integration time']
            print(f'Integration time set to {set_time} us')
            self.verbose = save_verbose
        
    def take_spectra(self):
        '''
        Record the current spectra
        
        '''
        try:
            # record wavelength and intensity data
            spectra = self.spectrometer.spectrum()
            if self.verbose:
                print('Spectra acquired')
            
            return spectra
        
        except Exception as e:
            print(f"Error collecting data: {e}")

    def take_average(self, n_samples=2):
        '''
        Record an average of spectra
        
        <n_samples>:
            number of averages to take
            
        '''
        #TO DO check need for array 
        try:
            # prevent print out for each spectra
            save_verbose = self.verbose
            self.verbose = False
            start = time.time()
            # begin averaging
            temp = 0
            for _ in range(n_samples):
                temp += self.take_spectra()
            # create averaged array
            averaged = array(temp/n_samples)
            stop = time.time()          # end time
            # reset verbose
            self.verbose = save_verbose
            if self.verbose:
                print(f'Averaged spectra aqcuired in {stop-start:.2f} s')

            return averaged
        
        except Exception as e:
            print(f"Error collecting data: {e}")
            return False


