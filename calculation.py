# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 11:21:38 2021

@author: Nima
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import warnings

class Calculation():
    
    
    def cal_range(country, range_cl):
    
    #checking the wrong value
            for val in range(0,len(country)):
                if country[val]<0:
                    country[val] = 0
        
            stable_range = range_cl
            count = stable_range
            m = max(country)
            mi = min(country)
            steps = math.ceil((m-mi)/stable_range)
            print('steps   ' + str(steps))
            for x in range(0,steps):
                # print('+++ X' + str(x))
                for i in range(len(country)):
                    # print('---country= ' + str(country[i])+'---value of i= ' + str(i)) 
                    if country[i] < count and country[i] >= count-stable_range:
                        country[i] = count-1
                count = count + stable_range
            # print('value of count = ' + str(count))
            return country

    def remove_nan_withZero(listInput):
        for i in range(0,len(listInput)) :
            if str(listInput[i]) == 'nan':
                listInput[i] = 0
        return listInput
                
    def fftPlot(sig, dt=None, plot=True):
    # Here it's assumes analytic signal (real signal...) - so only half of the axis is required

        if dt is None:
            dt = 1
            t = np.arange(0, len(sig))
            xLabel = 'samples'
        else:
            t = np.arange(0, len(sig)) * dt
            xLabel = 'freq [Hz]'
    
        # if sig.shape[0] % 2 != 0:
        #     warnings.warn("signal preferred to be even in size, autoFixing it...")
        #     t = t[0:-1]
        #     sig = sig[0:-1]
    
        sigFFT = np.fft.fft(sig) / t.shape[0]  # Divided by size t for coherent magnitude
    
        freq = np.fft.fftfreq(t.shape[0], d=dt)
    
        # Plot analytic signal - right half of frequence axis needed only...
        firstNegInd = np.argmax(freq < 0)
        freqAxisPos = freq[0:firstNegInd]
        sigFFTPos = 2 * sigFFT[0:firstNegInd]  # *2 because of magnitude of analytic signal
    
        # if plot:
        #     plt.figure()
        #     plt.plot(freqAxisPos, np.abs(sigFFTPos))
        #     plt.xlabel(xLabel)
        #     plt.ylabel('mag')
        #     plt.title('Analytic FFT plot')
        #     plt.show()

        return sigFFTPos, freqAxisPos   
    def count_white(image):
        row, col = image.shape

        count = 0
        for i in range(0,row):
            for j in range(0,col):
                if image[i][j] == 255:
                    count +=1
        return count 
            