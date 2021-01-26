#!/usr/bin/env python

# Useful libraries that are installed by default
import sys
import numpy as np
from scipy import signal
from numpy import *


# PyQt5
from PyQt5 import QtCore, QtGui, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import cv2

import pandas
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QCoreApplication

import datetime
from skimage import measure


import urllib.request
import threading
import webbrowser
from decimal import Decimal, ROUND_HALF_UP


# Import your GUI here : from "name of your file without extension" import "the main class"
# ...
from gui import Ui_MainWindow
from readingdata import ReadingData
from calculation import Calculation
from SetInfo import SetInfo


b_Canvas = b_Canvas2 = False
new_case = 'new_cases'
date_in = 'date'
radioState = True
tempCountry = ['France','China','Italy','Spain','Germany','United Kingdom']
dateInputTemp = '2020-01-01'
dateOnputTemp = '2020-12-27'
pageNumber = 1
# Signal is 1, Image is 2, Compare is 3
menuCheck = 1
pageNumberImage = 0
ch_THRESH_BINARY = ch_THRESH_TRUNC = ch_THRESH_TOZERO = 127
threshBinary = threshBinaryErosion = threshBinaryCompareCovid = threshBinaryCompareHealth = 0
x_data = y_data = 0
cannyThreshOne = 100
cannyThreshTwo = 200
methodToAnalysSignal = ['New cases','New death','New cases Vs New deathes']
methodToAnalysSignalTemp = ['New cases','New death']
methodToAnalysTwoCountries = ['New cases','New death']
methodToAnalysImage = ['Select Method', 'Histogram', 'Otsu Threshold' , 'Other Threshold Methods' , 'Contour Detection', 'Filters', 'Morphology', 'Compare']
textComMethod = ''
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
fileName = 'final_temp.csv'
checkCompreSelcte = False
countryList = ''
secondCountry = firstCountry = ''
valueSpinBox = 3
pageNumberFilter = 0
morphologyListName = ['erosion','dilation','opening','closing']

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent) # The 2 lines here are always presented like this
        QMainWindow.__init__(self, parent)         # Just to inialize the window

        self.ui = Ui_MainWindow()      # All the elements from our GUI are added in "self.ui"
        self.ui.setupUi(self)
        self.showMaximized()
        self.ui.gp_image.setVisible(False)
        self.ui.tx_download.setVisible(False)
        self.ui.pb_download.setVisible(False)
        self.ui.btn_load.clicked.connect(self.load_data)
        self.ui.btn_download_online.clicked.connect(self.load_data_online)
        self.ui.btn_process.clicked.connect(self.process_button)
        self.ui.btnImage.clicked.connect(self.image_button_push)
        self.ui.btnSignal.clicked.connect(self.signal_button_push)
        self.ui.binSlider.valueChanged.connect(self.get_valu_slider)
        self.ui.ch_temp.stateChanged.connect(self.checkBoxChangedAction)
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.ui.com_method.currentIndexChanged.connect(self.com_method_selectionchange)
        #compare two countries
        self.ui.gp_compare.setVisible(False)
        self.ui.btn_compare_country.clicked.connect(self.signal_compare_two_countries)
        self.ui.btn_process_compare.clicked.connect(self.process_compare_two_countries)
        self.ui.btn_load_Compare.clicked.connect(self.load_two_country)
        self.ui.comboBox_compare.currentIndexChanged.connect(self.comboBox_compare_selectionchange)
        self.ui.com_second_country.currentIndexChanged.connect(self.com_second_country_selectionchange)
        self.ui.com_method_compare.currentIndexChanged.connect(self.com_method_compare_selectionchange)
        # shift
        self.ui.com_shift.setVisible(False)
        ## image part #####################################################
        self.ui.btn_image_load.clicked.connect(self.load_image)
        self.ui.btn_process_tresh.clicked.connect(self.process_image_tresh)
        self.ui.btn_canny_process.clicked.connect(self.process_image_canny)
        self.ui.slider_threshold.valueChanged.connect(self.get_valu_slider_tresh)
        self.ui.slider_thresh_canny.valueChanged.connect(self.get_valu_slider_canny_outsuthresh)
        self.ui.slider_tresh1.valueChanged.connect(self.get_valu_slider_canny_thresh1)
        self.ui.slider_thresh2.valueChanged.connect(self.get_valu_slider_canny_thresh2)
        self.ui.com_image.currentIndexChanged.connect(self.com_image_selectionchange)
        self.ui.com_edge.currentIndexChanged.connect(self.com_edge_selectionchange)
        self.ui.btn_process_filters.clicked.connect(self.process_image_filter)
        self.ui.com_filter.currentIndexChanged.connect(self.com_filter_selectionchange)
        # Morphology
        self.ui.com_morphology.currentIndexChanged.connect(self.com_morphology_selectionchange)
        self.ui.btn_process_morphology.clicked.connect(self.process_image_morph)
        self.ui.slider_thresh_morph.valueChanged.connect(self.get_valu_slider_thresh_morph)
        # Compare
        self.ui.slider_tresh_compare.valueChanged.connect(self.get_valu_slider_thresh_compare)
        self.ui.btn_process_compare_image.clicked.connect(self.process_image_compare)
        self.ui.rd_covid_compare.clicked.connect(self.rd_covid_compare_check) 
        self.ui.rd_health_compare.clicked.connect(self.rd_health_compare_check) 
        self.ui.com_compare_type.currentIndexChanged.connect(self.com_compare_type_selectionchange)
        
    def load_data(self):
        global df,readingDataOB,date, countryList
        filename = QFileDialog.getOpenFileName(self, 'Open', "", "Case(*.csv)")[0]
        if filename != '':
        
            df = pandas.read_csv(filename)
            # add list of countries 
            countryList = ReadingData.name_of_country(df)
            self.fill_comboBox(countryList)
            self.fill_comboBox_method(methodToAnalysSignal)
            
            
    
    def load_data_online(self):
        
        webbrowser.open(url, new=2)
        # self.ui.pb_download.setVisible(True)
        # self.createNewDownloadThread(url,fileName)
        
        
   #####todo work to get online file ######################################################################       
        # self.set_date(ReadingData.detial_list(df,text,date))
        
    def Handle_Progress(self, blocknum, blocksize, totalsize): 
  
        ## calculate the progress 
        readed_data = blocknum * blocksize 
  
        if totalsize > 0: 
            download_percentage = readed_data * 100 / totalsize 
            convertD = int(download_percentage)
            # print(convertD)
            self.ui.pb_download.setValue(convertD) 
            QApplication.processEvents() 
            
        
            
    def download(self,link, filelocation):
        
        try:
            
            global df,readingDataOB,date, countryList
            
            print('Beginning file download with urllib2...')
            urllib.request.urlretrieve(link, filelocation,self.Handle_Progress)
            
            self.ui.pb_download.setVisible(False)
            self.ui.tx_download.setVisible(True)
            self.ui.tx_download.setText('Downlaod is complete')
            
            
            df = pandas.read_csv(fileName)
            # add list of countries 
            countryList = ReadingData.name_of_country(df)
            self.fill_comboBox(countryList)
            self.fill_comboBox_second_countries(countryList)
            self.fill_comboBox_method(methodToAnalysSignal)
           
            print('end of download')
            
        except:
            self.ui.pb_download.setVisible(False)
            self.ui.tx_download.setVisible(True)
            self.ui.tx_download.setText('There is an error try again')
            
    def createNewDownloadThread(self,link, filelocation):
        download_thread = threading.Thread(target=self.download, args=(link,filelocation))
        download_thread.start()
        print('thread start')
        return 'thread start'
    
    ##################compare two countries ##################################
    def signal_compare_two_countries(self):
        global countryList,checkCompreSelcte,menuCheck
        checkCompreSelcte = True
        menuCheck = 3
        
        self.remove_figures()
        self.ui.gp_image.setVisible(False)
        self.ui.gp_signal.setVisible(True)
        self.ui.gp_param.setVisible(False)
        self.ui.gp_compare.setVisible(True)
        self.ui.textBrowser.setVisible(True)
        
        
        
        self.fill_comboBox_method_compare(methodToAnalysTwoCountries)
        
        if len(countryList) > 0:
            self.fill_comboBox_second_countries(countryList)
            self.fill_comboBox_first_countries(countryList)
            
        
    def load_two_country(self):
        global df,readingDataOB,date, countryList
        filename = QFileDialog.getOpenFileName(self, 'Open', "", "Case(*.csv)")[0]
        if filename != '':
        
            df = pandas.read_csv(filename)
            # add list of countries 
            countryList = ReadingData.name_of_country(df)
            self.fill_comboBox_first_countries(countryList)
            self.fill_comboBox_second_countries(countryList)
            
    def fill_comboBox_method_compare(self,listCountries):
        self.ui.com_method_compare.clear() 
        self.ui.com_method_compare.addItems(['Select Data type'])
        self.ui.com_method_compare.addItems(listCountries)   
        
    def fill_comboBox_second_countries(self,listCountries):
        self.ui.com_second_country.clear() 
        self.ui.com_second_country.addItems(['Select Second Country'])
        self.ui.com_second_country.addItems(listCountries)
        
            
    def fill_comboBox_first_countries(self,listCountries):
        self.ui.comboBox_compare.clear() 
        self.ui.comboBox_compare.addItems(['Select First Country'])
        self.ui.comboBox_compare.addItems(listCountries)
        
            
    def com_second_country_selectionchange(self):
        # global date_in
        global secondCountry,firstCountry
        secondCountry = self.ui.com_second_country.currentText()
        if firstCountry != '' and firstCountry != 'Select Country' and secondCountry != '' and secondCountry != 'Select Second Country':
            self.set_date_two_countries(firstCountry,secondCountry)
            
    def comboBox_compare_selectionchange(self):
        # global date_in
        global secondCountry,firstCountry
        firstCountry = self.ui.comboBox_compare.currentText()
        if not firstCountry and firstCountry != 'Select Country' and not secondCountry  and secondCountry != 'Select Second Country':
            self.set_date_two_countries(firstCountry,secondCountry)
    
    def com_method_compare_selectionchange(self):
        # global date_in
        global pageNumberCompare
        text = self.ui.com_method_compare.currentText()
        pageNumberCompare = self.ui.com_method_compare.findText(text, QtCore.Qt.MatchFixedString)
        # check bin slider for compare cases
        
        
        
        # set date 
    def set_date_two_countries(self,firstCountry,secondCountry):
        
        global dateFromCompare, dateToCompare
        dateFirstCountry = ReadingData.detial_list(df,firstCountry,'date')
        dateSecondCountry = ReadingData.detial_list(df,secondCountry,'date')
        
        self.ui.date_from_compare.setDisplayFormat("dd/MM/yyyy")
        self.ui.date_to_compare.setDisplayFormat("dd/MM/yyyy")
        
        if len(dateFirstCountry) != 0 and len(dateSecondCountry) != 0  :
            
            dateFrom = dateFirstCountry[0]
            dateTo = dateFirstCountry[-1]
            date1String = dateFirstCountry[0].split('-')
            date2String = dateSecondCountry[0].split('-')
   
            date1 = datetime.date(int(date1String[0]), int(date1String[1]), int(date1String[2]))
            date2 = datetime.date(int(date2String[0]), int(date2String[1]), int(date2String[2]))
            
            if date1< date2:
                print('before')
                dateFrom = dateFirstCountry[0]
                
            elif date1> date2:
                dateFrom = dateSecondCountry[0]
                print('after')
            
                
                
            print(dateFrom + '---' + dateTo)
            firstDateSplit = dateFrom.split('-')
            lastDate = dateTo.split('-')
            d1 = QDateTime(int(firstDateSplit[0]), int(firstDateSplit[1].replace('0','')), 
                               int(firstDateSplit[2].replace('0','')), 10, 30) 
            d2 = QDateTime(int(lastDate[0]), int(lastDate[1].replace('0','')),
                               int(lastDate[2].replace('0','')), 10, 30)
            print(d2)
            self.ui.date_from_compare.setDateTime(d1) 
            self.ui.date_to_compare.setDateTime(d2) 
            self.ui.date_from_compare.setDateTimeRange(d1, d2) 
            self.ui.date_to_compare.setDateTimeRange(d1, d2) 
            
            dateFromCompare = dateFrom
            dateToCompare = dateTo
    
            # get date and time accorfing to edit time Gui for Compare two countries
    def GetDatetime_compare(self):
        
        global dateFromCompare, dateToCompare
        dt = self.ui.date_from_compare.dateTime()
        dt_string_From = dt.toString(self.ui.date_from_compare.displayFormat())
        dt_string_sFrom = dt_string_From.split('/')
        timeFrom = str(dt_string_sFrom[2] +'-'+dt_string_sFrom[1]+'-'+dt_string_sFrom[0])
        
        dt = self.ui.date_to_compare.dateTime()
        dt_string_TO = dt.toString(self.ui.date_to_compare.displayFormat())
        dt_string_sTo = dt_string_TO.split('/')
        timeTo = str(dt_string_sTo[2] +'-'+dt_string_sTo[1]+'-'+dt_string_sTo[0])
        dateFromCompare = timeFrom
        dateToCompare = timeTo
        
        # resultF = ReadingData.get_dat_according_time(df,countryName, dataType, timeFrom, timeTo)
        
        
        # print(dt_string_r)
        return dateFromCompare,dateToCompare
    
    # process button clcik
    def process_compare_two_countries(self):
        global pageNumberCompare
        self.ui.textBrowser.setVisible(False)
        print(pageNumberCompare)
        if pageNumberCompare == 1:
            self.show_scatter_plot_new_cases_countries()
            
        
        elif pageNumberCompare == 2:
            self.show_scatter_plot_new_deathes_countries()
    
    def show_scatter_plot_new_cases_countries(self):
        global pageNumberCompare,new_cases_first,new_cases_second
        pageNumberCompare = 1
        self.remove_figures()
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.845,bottom=0.165,left=0.11,right=0.9,hspace=0.5,wspace=0.2)
        
        # get data according to time
        dateFromCompare,dateToCompare = self.GetDatetime_compare()
        new_cases_first,new_cases_second = ReadingData.create_equal_list(df, firstCountry, secondCountry, 'new_cases', dateFromCompare, dateToCompare)
        
        SetInfo.set_info_compare_two_countries_new_cases(self, df, firstCountry, secondCountry, new_cases_first, new_cases_second)
         # Input signal
        # newCases = ReadingData.detial_list(df,text,new_case)
        # fig = plt.figure(figsize=(10,3))
        ax1f1 = fig.add_subplot(121)
        ax1f1.scatter(new_cases_first,new_cases_second,color = 'blue')
        ax1f1.set_title('New cases compare between ' + firstCountry + ' and ' + secondCountry,fontsize = 14)
        ax1f1.set_xlabel('New Cases in ' + firstCountry,fontsize = 12)
        ax1f1.set_ylabel('New Cases in ' + secondCountry,fontsize = 12)
        print('show_plot_next_page_temp pressed')
        
         # To generate some test data
        x = new_cases_first
        y = new_cases_second
        
        # fig = plt.figure() #create a canvas, tell matplotlib it's 3d
        ax1f2 = fig.add_subplot(122, projection='3d')
        
        xRange = max(new_cases_first)
        yRange = max(new_cases_second)
        print(yRange)
        hist, xedges, yedges = np.histogram2d(x, y, bins=(10,10), range = [[0,xRange],[0,yRange]]) # you can change your bins, and the range on which to take data
        # hist is a 7X7 matrix, with the populations for each of the subspace parts.
        xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])
        
        
        xpos = xpos.flatten()*1./2
        ypos = ypos.flatten()*1./2
        zpos = np.zeros_like (xpos)
        
        dx = xedges [1] - xedges [0]
        dy = yedges [1] - yedges [0]
        dz = hist.flatten()
        
        cmap = plt.get_cmap('jet') # Get desired colormap - you can change this!
        max_height = np.max(dz)   # get range of colorbars so we can normalize
        min_height = np.min(dz)
        # scale each z to [0,1], and get their rgb values
        rgba = [cmap((k-min_height)/max_height) for k in dz] 
        
        ax1f2.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
        ax1f2.set_title('New cases compare between ' + firstCountry + ' and ' + secondCountry,fontsize = 14)
        ax1f2.set_xlabel('New Cases in ' + firstCountry,fontsize = 12)
        ax1f2.set_ylabel('New Cases in ' + secondCountry,fontsize = 12)
        
        self.setting_for_figures()
    
        # show the number of deatehs in each countriy according to time
    def show_scatter_plot_new_deathes_countries(self):
        
        global pageNumberCompare,new_deathes_first,new_deathes_second
        pageNumberCompare = 2
        self.remove_figures()
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.845,bottom=0.165,left=0.11,right=0.9,hspace=0.5,wspace=0.2)
        
        # get data according to time
        dateFromCompare,dateToCompare = self.GetDatetime_compare()
        new_deathes_first,new_deathes_second = ReadingData.create_equal_list(df, firstCountry, secondCountry, 'new_deaths', dateFromCompare, dateToCompare)
        
        SetInfo.set_info_compare_two_countries_new_death(self, df, firstCountry, secondCountry, new_deathes_first, new_deathes_second)
         # Input signal
        # newCases = ReadingData.detial_list(df,text,new_case)
        # fig = plt.figure(figsize=(10,3))
        ax1f1 = fig.add_subplot(121)
        ax1f1.scatter(new_deathes_first,new_deathes_second,color = 'red')
        ax1f1.set_title('New deathes compare between ' + firstCountry + ' and ' + secondCountry,fontsize = 14)
        ax1f1.set_xlabel('New deathes in ' + firstCountry,fontsize = 12)
        ax1f1.set_ylabel('New deathes in ' + secondCountry,fontsize = 12)
        
        
         # To generate some test data
        x = new_deathes_first
        y = new_deathes_second
        
        # fig = plt.figure() #create a canvas, tell matplotlib it's 3d
        ax1f2 = fig.add_subplot(122, projection='3d')
        
        xRange = max(new_deathes_first)
        yRange = max(new_deathes_second)
        print(yRange)
        hist, xedges, yedges = np.histogram2d(x, y, bins=(10,10), range = [[0,xRange],[0,yRange]]) # you can change your bins, and the range on which to take data
        # hist is a 7X7 matrix, with the populations for each of the subspace parts.
        xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])
        
        
        xpos = xpos.flatten()*1./2
        ypos = ypos.flatten()*1./2
        zpos = np.zeros_like (xpos)
        
        dx = xedges [1] - xedges [0]
        dy = yedges [1] - yedges [0]
        dz = hist.flatten()
        
        cmap = plt.get_cmap('jet') # Get desired colormap - you can change this!
        max_height = np.max(dz)   # get range of colorbars so we can normalize
        min_height = np.min(dz)
        # scale each z to [0,1], and get their rgb values
        rgba = [cmap((k-min_height)/max_height) for k in dz] 
        
        ax1f2.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
        ax1f2.set_title('3D Histogram of new deathes between ' + firstCountry + ' and ' + secondCountry,fontsize = 14)
        ax1f2.set_xlabel('New deathes in ' + firstCountry,fontsize = 12)
        ax1f2.set_ylabel('New deathes in ' + secondCountry,fontsize = 12)
        
        self.setting_for_figures()
       
    ##########################################################################
    
    
    def fill_comboBox(self,listCountries):
        self.ui.comboBox.clear() 
        self.ui.comboBox.addItems(['Select Country'])
        self.ui.comboBox.addItems(listCountries)
        
    
        
    def fill_comboBox_method(self,listCountries):
        self.ui.com_method.clear() 
        self.ui.com_method.addItems(['Select Data type'])
        self.ui.com_method.addItems(listCountries)
        
    def set_date(self,dataList):
        
        self.ui.date_from.setDisplayFormat("dd/MM/yyyy")
        self.ui.date_to.setDisplayFormat("dd/MM/yyyy")
        
        if len(dataList) != 0:
            
            print(dataList[0] + '---' + dataList[-1])
            firstDateSplit = dataList[0].split('-')
            lastDate = dataList[-1].split('-')
            d1 = QDateTime(int(firstDateSplit[0]), int(firstDateSplit[1].replace('0','')), 
                               int(firstDateSplit[2].replace('0','')), 10, 30) 
            d2 = QDateTime(int(lastDate[0]), int(lastDate[1].replace('0','')),
                               int(lastDate[2].replace('0','')), 10, 30)
            print(d2)
            self.ui.date_from.setDateTime(d1) 
            self.ui.date_to.setDateTime(d2) 
            self.ui.date_from.setDateTimeRange(d1, d2) 
            self.ui.date_to.setDateTimeRange(d1, d2) 
            
    
    def process_button(self):
         
        global textCombobox, b_Canvas
        textCombobox = str(self.ui.comboBox.currentText())
        
        if b_Canvas == True:
            self.rm_mpl()
        else:
            self.ui.textBrowser.setVisible(False)
        ### 
        if radioState and textCombobox != 'Selsect The Country' :
            
            if pageNumber == 1:
                
                # print(text)
                self.show_plot_newcases()
                # set info in text
                self.set_info_new_case()
            elif pageNumber == 2:
                self.show_plot_next_page_death_reg()
                self.set_info_new_deathes()
                
            elif pageNumber == 3:
                # self.show_plot_next_page_death_reg()
                # self.set_info_new_case()
                self.show_plot_scatter_Compare()
                self.set_info_compare_new_deathes_new_cases()
                
        elif not radioState and textCombobox != 'Selsect The Country':
            if pageNumber == 1:
                 # print(text)
                self.show_plot_next_page_scatter_temp()
                # set info in text
                self.set_info_compare_temp_new_cases()
            elif pageNumber == 2:
                self.show_plot_scatter_plot_new_deathes()
                self.set_info_compare_temp_new_deathes()
                print('pageNumber == 2')
           
                

    
    def rm_mpl(self):
        global b_Canvas
        self.ui.verticalLayout.removeWidget(self.canvas)
        self.canvas.close()
        self.ui.verticalLayout.removeWidget(self.toolbar)
        self.toolbar.close()
        b_Canvas = False
        
    # show plot new cases for each country in specific time
    def show_plot_newcases(self):
        global b_Canvas,new_case, pageNumber, x_data, y_data, textCombobox
        
        self.remove_figures()
            
        pageNumber = 1
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(hspace = 0.6)
        
        # get data according to time
        new_case = self.GetDatetime(textCombobox,'new_cases')
        new_case = Calculation.remove_nan_withZero(new_case)
        
        self.get_valu_slider()
        
         # Input signal
        # newCases = ReadingData.detial_list(df,text,new_case)
        ax1f1 = fig.add_subplot(311)
        
        # check marker or not
       
        if self.ui.ch_marker.isChecked():
            
            
            textstr = self.calculate_date_new_case()
            
            # print(textstr)
            
            ax1f1_new_cases = ax1f1
            ax1f1.plot(new_case,color = 'blue',marker='o',markerfacecolor='green',markeredgecolor = 'red' ,markersize=3)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax1f1_new_cases.text(0.01, 0.95, textstr, transform=ax1f1_new_cases.transAxes, fontsize=14,
                        verticalalignment='top', bbox=props)    #
            
            
            # if x_data == 0:
            # fig.canvas.callbacks.connect('button_release_event', self.onrelease)
            fig.canvas.callbacks.connect('button_press_event', self.callback)
            

        else:
            ax1f1.plot(new_case,color = 'blue')
            
        ax1f1.set_title('Number of cases ' + textCombobox,fontsize=14)
        ax1f1.set_xlabel('Days',fontsize=12)
        ax1f1.set_ylabel('new Cases',fontsize=12)
        
        
         # FFT Abs   
        ax1f2 = fig.add_subplot(312)
        binsNum = self.ui.binSlider.value()
        # rangeCal = Calculation.cal_range(newCases,500)
        # (mu, sigma) = norm.fit(newCases)
        # y = mlab.normpdf( 100, mu, sigma)
        # mu, sigma = norm.fit(newCases)
        # best_fit_line = norm.pdf(binsNum, mu, sigma)
        
        ax1f2.hist(new_case, bins = binsNum, color = "blue")
        # ax1f2.plot(binsNum, best_fit_line)
        ax1f2.set_title('Histogram of new cases in ' + textCombobox,fontsize=14)
        ax1f2.set_xlabel("Number of cases", fontsize=12)
        ax1f2.set_ylabel("Days", fontsize=12)
        # ax1f2.axis(xmin=-pi/2, xmax=pi/2)
        
        # parameter for other figure
        fftNum = 512
        w, Hh = signal.freqz(new_case, 1, whole=True, worN=fftNum)  # to get entire frequency domain
        wx = np.fft.fftfreq(len(w)) # to shift to center
         # FFT Abs 
        halfFFtCal = int(fftNum/2)
        wPI = w-pi
        halfFFT = wPI[halfFFtCal:]
        yhalf = abs(fft.fftshift(Hh))
        yHalfFFT = yhalf[halfFFtCal:]
        ax1f3 = fig.add_subplot(313)
        ax1f3.plot(halfFFT, yHalfFFT)
        ax1f3.set_title('FFT Graph of new cases for each day in ' + textCombobox,fontsize=14)
        # ax1f3.set_xlabel("Frequency", fontsize=12)
        # ax1f3.set_ylabel(r"$|H(\omega)| $", fontsize=12)
        ax1f3.axis(xmin=0, xmax=pi/2)
        
        self.canvas.draw()
        
        self.toolbar = NavigationToolbar(self.canvas, self.ui.mplwindow, coordinates=True)
        self.ui.verticalLayout.addWidget(self.toolbar)
        
        b_Canvas = True
    

    def callback_death(self,event):
            
        global x_data,y_data
        print('onpress')
        x_data = event.xdata
        y_data = event.ydata
        
        if str(x_data) != 'None':
            self.show_plot_next_page_death_reg()
            
    def callback(self,event):
            
        global x_data,y_data
        
        x_data = event.xdata
        y_data = event.ydata
        
        print('onpress' + str(x_data))
        if str(x_data) != 'None':
        
            self.show_plot_newcases()
    
    def onrelease(self,event):
            
        # global x_data,y_data
        print('onrelease')
        
    def calculate_date_new_case(self):
        
        try:
            
            global new_case, pageNumber, x_data, y_data, textCombobox
            indexX = Decimal(x_data).to_integral_value(rounding=ROUND_HALF_UP)
            val_newCase = new_case[int(indexX)]
            diffrentCase = abs(val_newCase - y_data)
            val = 'Number of new cases: ' 
            date = 'Date: ' 
            print('x_data ' + str(x_data))
            print('val_newCase ' + str(val_newCase))
            print('y_data ' + str(y_data))
            
            if diffrentCase < 2*np.mean(new_case) and y_data!= 0 :
                
                dateX = ReadingData.detial_list(df,textCombobox,'date')[int(indexX)]
                val = 'Number of new cases: ' + str(int(val_newCase))
                date = 'Date: ' + str(dateX)
                textstr = val + '\n' + date
                return textstr
            else:
                textstr = val + '\n' + date
                return textstr
        except :
            print('Error in clickng')
        
        
    def calculate_date_new_death(self):
        try:
            
            global new_death, pageNumber, x_data, y_data, textCombobox
            indexX = Decimal(x_data).to_integral_value(rounding=ROUND_HALF_UP)
            val_newCase = new_death[int(indexX)]
            diffrentCase = abs(val_newCase - y_data)
            val = 'Number of new death: ' 
            date = 'Date: ' 
            print('x_data ' + str(x_data))
            print('val_newCase ' + str(val_newCase))
            print('y_data ' + str(y_data))
            
            if diffrentCase < 2*np.mean(new_death) and y_data!= 0 :
                
                dateX = ReadingData.detial_list(df,textCombobox,'date')[int(indexX)]
                val = 'Number of new death: ' + str(int(val_newCase))
                date = 'Date: ' + str(dateX)
                textstr = val + '\n' + date
                return textstr
            else:
                textstr = val + '\n' + date
                return textstr    
        except :
            print('Error in clickng')   
        
    ##get the current ivent of combobox selct
    def selectionchange(self):
        # global date_in
        global textName
        textName = self.ui.comboBox.currentText()
        # set date 
        if radioState:
            
            
            print(textName + 'regular')
            self.set_date(ReadingData.detial_list(df,textName,date_in))

        # temp
        else:
            
            
            
            if (self.isNotBlank(textName)) & (textName != 'Select Country'):
                print(textName + 'temprrr')
                datD = ReadingData.detial_list(df,textName,date_in)
                self.set_date([datD[0],dateOnputTemp])

    def com_method_selectionchange(self):
        global textComMethod, pageNumber
        textComMethod = self.ui.com_method.currentText()
        pageNumber = self.ui.com_method.findText(textComMethod, QtCore.Qt.MatchFixedString)
        # check bin slider for compare cases
        if textComMethod == methodToAnalysSignal[2] :
            self.bins_value(False)
            self.ui.com_shift.setVisible(True)
            self.ui.ch_marker.setVisible(False)
    
        elif radioState:
            self.bins_value(True)
            self.ui.com_shift.setVisible(False)
            self.ui.ch_marker.setVisible(True)
            
        # print(pageNumber)
        
    
    def GetDatetime(self,countryName, dataType):
        
        global dateFrom, dateTo
        dt = self.ui.date_from.dateTime()
        dt_string_From = dt.toString(self.ui.date_from.displayFormat())
        dt_string_sFrom = dt_string_From.split('/')
        timeFrom = str(dt_string_sFrom[2] +'-'+dt_string_sFrom[1]+'-'+dt_string_sFrom[0])
        
        dt = self.ui.date_to.dateTime()
        dt_string_TO = dt.toString(self.ui.date_to.displayFormat())
        dt_string_sTo = dt_string_TO.split('/')
        timeTo = str(dt_string_sTo[2] +'-'+dt_string_sTo[1]+'-'+dt_string_sTo[0])
        dateFrom = timeFrom
        dateTo = timeTo
        
        resultF = ReadingData.get_dat_according_time(df,countryName, dataType, timeFrom, timeTo)
        
        
        # print(dt_string_r)
        return resultF
        
    def get_valu_slider(self):
        
        # print('Bins number: ' + str(self.ui.binSlider.value()))
        strBinNumber = 'Bins number: ' + str(self.ui.binSlider.value())
        self.ui.txt_slider_value.setText(strBinNumber)
        
    def radio_button_temp(self):
        print('radio_button_temp')
        global radioState 
        radioState = False
        
        self.fill_comboBox(tempCountry)
        # self.set_date([])
       
    def radio_button_reg(self):
        print('radio_button_reg')
        global radioState 
        radioState = True
        # add list of countries 
        self.fill_comboBox(countryList)
        
    def checkBoxChangedAction(self):
        global radioState 
        if self.ui.ch_temp.isChecked():
            print('ch temp')
            # global radioState 
            radioState = False
            self.bins_value(False)
            self.fill_comboBox(tempCountry)
            self.fill_comboBox_method(methodToAnalysSignalTemp)
            self.ui.ch_marker.setVisible(False)
        else:
            print('ch reg')
            # global radioState 
            radioState = True
            # add list of countries 
            self.fill_comboBox(countryList)
            # visible bin
            self.bins_value(True)
            self.ui.ch_marker.setVisible(True)
            self.fill_comboBox_method(methodToAnalysSignal)
                
       
        
    def isNotBlank (self,myString):
        return bool(myString and myString.strip())
    
    def signal_button_push(self):
        global menuCheck
        # self.ui.btn_next.setText('Next')
        # self.ui.btn_prev.setText('Previous')
        self.ui.gp_image.setVisible(False)
        self.ui.gp_signal.setVisible(True)
        self.ui.textBrowser.setVisible(True)
        self.ui.gp_compare.setVisible(False)
        self.ui.gp_param.setVisible(True)
        
        
        
        self.remove_figures()
        menuCheck = 1
   
    
        # next page with temp
    def show_plot_scatter_plot_new_deathes(self):
        
        global pageNumber,new_death,tempCountryDate
        pageNumber = 2
        self.remove_figures()
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.835,bottom=0.155,left=0.11,right=0.9,hspace=0.5,wspace=0.2)
        
        # get data according to time
        new_death = self.GetDatetime(textCombobox,'new_deaths')
        new_death = Calculation.remove_nan_withZero(new_death)
        tempCountryDate = ReadingData.temp_cal(textCombobox, dateFrom, dateTo)
        
         # Input signal
        # newCases = ReadingData.detial_list(df,text,new_case)
        # fig = plt.figure(figsize=(10,3))
        ax1f1 = fig.add_subplot(121)
        ax1f1.scatter(tempCountryDate,new_death,color = 'red')
        ax1f1.set_title('New deathes based on Temp ' + textCombobox,fontsize = 14)
        ax1f1.set_xlabel('Tempreture(C)',fontsize = 12)
        ax1f1.set_ylabel('New deathes',fontsize = 12)
        print('show_plot_next_page_temp pressed')
        
         # To generate some test data
        x = new_death
        y = tempCountryDate
        
        # fig = plt.figure() #create a canvas, tell matplotlib it's 3d
        ax1f2 = fig.add_subplot(122, projection='3d')
        
        xRange = max(new_death)
        yRange = max(tempCountryDate)
        print(yRange)
        hist, xedges, yedges = np.histogram2d(x, y, bins=(10,10), range = [[0,xRange],[0,yRange]]) # you can change your bins, and the range on which to take data
        # hist is a 7X7 matrix, with the populations for each of the subspace parts.
        xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])
        
        
        xpos = xpos.flatten()*1./2
        ypos = ypos.flatten()*1./2
        zpos = np.zeros_like (xpos)
        
        dx = xedges [1] - xedges [0]
        dy = yedges [1] - yedges [0]
        dz = hist.flatten()
        
        cmap = plt.get_cmap('jet') # Get desired colormap - you can change this!
        max_height = np.max(dz)   # get range of colorbars so we can normalize
        min_height = np.min(dz)
        # scale each z to [0,1], and get their rgb values
        rgba = [cmap((k-min_height)/max_height) for k in dz] 
        
        ax1f2.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
        ax1f2.set_title('3D Histogram of new deathes based on temperature in ' + textCombobox,fontsize = 14)
        ax1f2.set_xlabel("Number of deathes",fontsize = 12)
        ax1f2.set_ylabel("Tempreture(C)",fontsize = 12)
          
    
        ################## setting for figures
        self.setting_for_figures()
        ##################
        
    # next page with temp
    def show_plot_next_page_scatter_temp(self):
        
        global pageNumber,tempCountryDate,new_case
        # pageNumber = 2
        self.remove_figures()
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.835,bottom=0.155,left=0.11,right=0.9,hspace=0.5,wspace=0.2)
        
        # get data according to time
        new_case = self.GetDatetime(textCombobox,'new_cases')
        tempCountryDate = ReadingData.temp_cal(textCombobox, dateFrom, dateTo)
        
         # Input signal
        # newCases = ReadingData.detial_list(df,text,new_case)
        # fig = plt.figure(figsize=(10,3))
        ax1f1 = fig.add_subplot(121)
        ax1f1.scatter(tempCountryDate,new_case)
        ax1f1.set_title('New cases based on Temp ' + textCombobox,fontsize = 14)
        ax1f1.set_xlabel('Tempreture(C)',fontsize = 12)
        ax1f1.set_ylabel('New cases',fontsize = 12)
        print('show_plot_next_page_temp pressed')
        
         # To generate some test data
        x = new_case
        y = tempCountryDate
        
        # fig = plt.figure() #create a canvas, tell matplotlib it's 3d
        ax1f2 = fig.add_subplot(122, projection='3d')
        
        xRange = max(new_case)
        yRange = max(tempCountryDate)
        print(yRange)
        hist, xedges, yedges = np.histogram2d(x, y, bins=(10,10), range = [[0,xRange],[0,yRange]]) # you can change your bins, and the range on which to take data
        # hist is a 7X7 matrix, with the populations for each of the subspace parts.
        xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])
        
        
        xpos = xpos.flatten()*1./2
        ypos = ypos.flatten()*1./2
        zpos = np.zeros_like (xpos)
        
        dx = xedges [1] - xedges [0]
        dy = yedges [1] - yedges [0]
        dz = hist.flatten()
        
        cmap = plt.get_cmap('jet') # Get desired colormap - you can change this!
        max_height = np.max(dz)   # get range of colorbars so we can normalize
        min_height = np.min(dz)
        # scale each z to [0,1], and get their rgb values
        rgba = [cmap((k-min_height)/max_height) for k in dz] 
        
        ax1f2.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
        ax1f2.set_title('3D Histogram of new cases based on temperature in ' + textCombobox,fontsize = 14)
        ax1f2.set_xlabel("Number of cases",fontsize = 12)
        ax1f2.set_ylabel("Tempreture(C)",fontsize = 12)
        # ax1f1.savefig("Your_title_goes_here")
        # plt.show()   
    
        ################## setting for figures
        self.setting_for_figures()
        ##################
    # get which shifted time is selected
    def get_shift_com(self):
        textComShift = self.ui.com_shift.currentText()
        pageNumberShift = self.ui.com_shift.findText(textComShift, QtCore.Qt.MatchFixedString)
        shift = 0
        if pageNumberShift == 1:
            shift = 7
        elif pageNumberShift == 2:
            shift = 14
        elif pageNumberShift == 3:
            shift = 21
        elif pageNumberShift == 4:
            shift = 30
        return shift
    
    def show_plot_scatter_Compare(self):
        
        global pageNumber,new_death,new_case
        pageNumber = 3
        
        self.remove_figures()
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.835,bottom=0.155,left=0.105,right=0.9,hspace=0.5,wspace=0.2)
        
        # get data according to time
        new_death = self.GetDatetime(textCombobox,'new_deaths')
        new_death = Calculation.remove_nan_withZero(new_death)
        new_case = self.GetDatetime(textCombobox,'new_cases')
        
        new_case,new_death = ReadingData.shift_value(new_case,new_death,self.get_shift_com())
     
         # Input signal
        # newCases = ReadingData.detial_list(df,text,new_case)
        # fig = plt.figure(figsize=(10,3))
        ax1f1 = fig.add_subplot(121)
        ax1f1.scatter(new_case,new_death,color = 'red')
        ax1f1.set_title('New deathes based on New case ' + textCombobox,fontsize = 14)
        ax1f1.set_xlabel('New cases',fontsize = 12)
        ax1f1.set_ylabel('New deathes',fontsize = 12)
        
         # To generate some test data
        x = new_death
        y = new_case
        
        # fig = plt.figure() #create a canvas, tell matplotlib it's 3d
        ax1f2 = fig.add_subplot(122, projection='3d')
        
        xRange = max(new_death)
        yRange = max(new_case)
        print(yRange)
        hist, xedges, yedges = np.histogram2d(x, y, bins=(10,10), range = [[0,xRange],[0,yRange]]) # you can change your bins, and the range on which to take data
        # hist is a 7X7 matrix, with the populations for each of the subspace parts.
        xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])
        
        
        xpos = xpos.flatten()*1./2
        ypos = ypos.flatten()*1./2
        zpos = np.zeros_like (xpos)
        
        dx = xedges [1] - xedges [0]
        dy = yedges [1] - yedges [0]
        dz = hist.flatten()
        
        cmap = plt.get_cmap('jet') # Get desired colormap - you can change this!
        max_height = np.max(dz)   # get range of colorbars so we can normalize
        min_height = np.min(dz)
        # scale each z to [0,1], and get their rgb values
        rgba = [cmap((k-min_height)/max_height) for k in dz] 
        
        ax1f2.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
        ax1f2.set_title('3D Histogram of new deathes based on new cases in ' + textCombobox,fontsize = 14)
        ax1f2.set_xlabel("Number of deathes",fontsize = 12)
        ax1f2.set_ylabel("Number of cases",fontsize = 12)
          
    
        ################## setting for figures
        self.setting_for_figures()
        ##################
    def setting_for_figures(self):
        global b_Canvas
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self.ui.mplwindow, coordinates=True)
        self.ui.verticalLayout.addWidget(self.toolbar)
        b_Canvas = True
    # set info in below process
    def set_info_new_case(self):
        
        SetInfo.set_info_new_case(self, df, textCombobox, new_case)
    def set_info_new_deathes(self):
        
        SetInfo.set_info_new_deathes(self, df, textCombobox, new_death)
        
        
    def set_info_compare_new_deathes_new_cases(self):
        SetInfo.set_info_compare_new_deathes_new_cases(self, df, textCombobox, new_case, new_death)
        
    def set_info_compare_temp_new_cases(self):
        global new_case,tempCountryDate
        SetInfo.set_info_compare_temp_new_cases(self, df, textCombobox, new_case, tempCountryDate)
        
    def set_info_compare_temp_new_deathes(self):
        global new_death,tempCountryDate
        SetInfo.set_info_compare_temp_new_deathes(self, df, textCombobox, new_death, tempCountryDate)
        
    # plot new deaths for each country according to date  
    def show_plot_next_page_death_reg(self):
        global b_Canvas, new_death, pageNumber
        self.remove_figures()
            
        pageNumber = 2
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(hspace = 0.6)
        
        # get data according to time
        new_death = self.GetDatetime(textCombobox,'new_deaths')
        new_death = Calculation.remove_nan_withZero(new_death)
        
        self.get_valu_slider()
        
        
         # Input signal
        # newCases = ReadingData.detial_list(df,text,new_case)
        ax1f1 = fig.add_subplot(311)
        
        if self.ui.ch_marker.isChecked():
            
            
            textstr = self.calculate_date_new_death()
            
            # print(textstr)
            
            ax1f1.plot(new_death,color = 'red',marker='o',markerfacecolor='green',markeredgecolor = 'blue' ,markersize=3)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            ax1f1.text(0.01, 0.95, textstr, transform=ax1f1.transAxes, fontsize=14,
                        verticalalignment='top', bbox=props)    #
            
            
            # if x_data == 0:
            # fig.canvas.callbacks.connect('button_release_event', self.onrelease)
            fig.canvas.callbacks.connect('button_press_event', self.callback_death)
            

        else:
            ax1f1.plot(new_death,color = 'red')
        # ax1f1.plot(new_death,color = 'red')
        ax1f1.set_title('Number of death ' + textCombobox,fontsize = 14)
        ax1f1.set_xlabel('Days',fontsize = 12)
        ax1f1.set_ylabel('death',fontsize = 12)
        
         # FFT Abs   
        ax1f2 = fig.add_subplot(312)
        binsNum = self.ui.binSlider.value()
        # rangeCal = Calculation.cal_range(newCases,500)
        # (mu, sigma) = norm.fit(newCases)
        # y = mlab.normpdf( 100, mu, sigma)
        # mu, sigma = norm.fit(newCases)
        # best_fit_line = norm.pdf(binsNum, mu, sigma)
        
        ax1f2.hist(new_death, bins = binsNum, color = "red")
        # ax1f2.plot(binsNum, best_fit_line)
        ax1f2.set_title('Histogram of number of death in ' + textCombobox,fontsize = 14)
        ax1f2.set_xlabel("Number of deths", fontsize=12)
        ax1f2.set_ylabel("Days", fontsize=12)
        # ax1f2.axis(xmin=-pi/2, xmax=pi/2)
        
        # parameter for other figure
       
         # FFT Abs   
        fftNum = 512
        w, Hh = signal.freqz(new_death, 1, whole=True, worN=fftNum)  # to get entire frequency domain        
         # FFT Abs 
        halfFFtCal = int(fftNum/2)
        wPI = w-pi
        halfFFT = wPI[halfFFtCal:]
        yhalf = abs(fft.fftshift(Hh))
        yHalfFFT = yhalf[halfFFtCal:]
        ax1f3 = fig.add_subplot(313)
        ax1f3.plot(halfFFT, yHalfFFT, color = "red")
        ax1f3.set_title('FFT Graph of new cases for each day in ' + textCombobox, fontsize=14)
        # ax1f3.set_xlabel("Frequency", fontsize=12)
        # ax1f3.set_ylabel(r"$|H(\omega)| $", fontsize=14)
        ax1f3.axis(xmin=0, xmax=pi/2)
        
        ################## setting for figures
        self.setting_for_figures()
        
        b_Canvas = True   
       
    # remove the figures if exist
    def remove_figures(self):
        global b_Canva
        if b_Canvas == True:
            
            self.rm_mpl()
            
    def bins_value(self,Value):
        self.ui.binSlider.setVisible(Value)
        self.ui.label_3.setVisible(Value)
        self.ui.txt_slider_value.setVisible(Value)
            
    ############################################## Image part ############################################
    def image_button_push(self):   
        global menuCheck, pageNumberImage
        self.ui.gp_signal.setVisible(False)
        
        # if pageNumberImage == 0:
        self.ui.gp_tresh.setVisible(False)
        self.ui.gp_edgedetection.setVisible(False)
        self.ui.gp_filter.setVisible(False)
        self.ui.gp_morphology.setVisible(False)
        self.ui.gp_compare_image.setVisible(False)
            
        self.ui.gp_image.setVisible(True)
        self.remove_figures()
        menuCheck = 2
        self.fill_comboBox_image_method(['Select Method'])
        
        
    
    def com_image_selectionchange(self):
        global textComMethodImage, pageNumberImage
        textComMethodImage = self.ui.com_image.currentText()
        pageNumberImage = self.ui.com_image.findText(textComMethodImage, QtCore.Qt.MatchFixedString)
        
        print(pageNumberImage)
        if pageNumberImage == 1:
            
            self.his_show_plot()
            self.setvisible_group_box(pageNumberImage)
        
            
        elif pageNumberImage == 2:
            self.show_plot_threshold()
            self.setvisible_group_box(pageNumberImage)
            
        elif pageNumberImage == 3:
            self.show_plot_threshold_slider()
            self.setvisible_group_box(pageNumberImage)
            
        elif pageNumberImage == 4:
            self.show_plot_canny()
            self.setvisible_group_box(pageNumberImage)
        # print(pageNumber)
        elif pageNumberImage == 5:
            # print(pageNumber)
            self.show_plot_Median()
            self.setvisible_group_box(pageNumberImage)
            
        elif pageNumberImage == 6:
            # print(pageNumber)
            self.morphology_part_call()
            self.setvisible_group_box(pageNumberImage)
            
        elif pageNumberImage == 7:
            # print(pageNumber)
            self.compare_part_call()
            self.setvisible_group_box(pageNumberImage)
        
    def fill_comboBox_image_method(self,listMethod):
        self.ui.com_image.clear() 
        # self.ui.comboBox.addItems(['Select Country'])
        self.ui.com_image.addItems(listMethod)    
        
 
    def load_image(self):
         global imageOriginal, imageHelth
         filename = QFileDialog.getOpenFileName(self, 'Open', "", "Case(*.png)")[0]
         if filename != '':
             
             imageOriginal = cv2.imread(filename,0)
             imageHelth = cv2.imread('normal.png',0)
             self.show_images()
             self.set_info_val()
             self.fill_comboBox_image_method(methodToAnalysImage)
         
         
    # show load image and healt person
    def show_images(self):
        print('show_images')
        global pageNumberImage
        # pageNumberImage = 1
        self.remove_figures()
        self.ui.textBrowser.setVisible(False)
        
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(hspace = 0.5)
        
        
        ax1f1 = fig.add_subplot(121)
        ax1f1.imshow(cv2.cvtColor(imageOriginal, cv2.COLOR_BGR2RGB))
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        # row,col= imageOriginal.shape
        # ax1f1.set_xlabel(str(row))
        # ax1f1.set_ylabel(str(col))
     
        ax1f2 = fig.add_subplot(122)
        ax1f2.imshow(cv2.cvtColor(imageHelth, cv2.COLOR_BGR2RGB))
        ax1f2.set_title('Healthy person CT scan image')
        ax1f2.axis("off")
        
        
        self.setting_for_figures()
        
    def his_show_plot(self):
        
  
        
        print('show_hist_eq')
        global pageNumberImage
        # pageNumberImage = 2
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.895,bottom=0.095,left=0.16,right=0.855,hspace=0.2,wspace=0.2)
        
                         
        
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(cv2.cvtColor(imageOriginal, cv2.COLOR_BGR2RGB))
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        # row,col= imageOriginal.shape
        # ax1f1.set_xlabel(str(row))
        # ax1f1.set_ylabel(str(col))
     
        ax1f2 = fig.add_subplot(222)
        ax1f2.hist(imageOriginal.ravel(),256,[0,256])
        ax1f2.set_title('Histogram of Covid-19 patient')
       
        ax1f3 = fig.add_subplot(223)
        dst = cv2.equalizeHist(imageOriginal)
        ax1f3.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
        ax1f3.set_title('Covid-19 patient Histogram Equalization')
        ax1f3.axis("off")
        
        ax1f4 = fig.add_subplot(224)
        ax1f4.hist(dst.ravel(),256,[0,256])
        ax1f4.set_title('Equalization Histogram of Covid-19 patient')
        
        # ax1f2.axis("off")
        self.setting_for_figures()
        
   
    
    def show_plot_threshold(self) :
        print('show_plot_threshold')
        global pageNumberImage
        # pageNumberImage = 3
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(cv2.cvtColor(imageOriginal, cv2.COLOR_BGR2RGB))
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        
        ret,threshOutsu = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ax1f2 = fig.add_subplot(222)
        ax1f2.imshow(cv2.cvtColor(threshOutsu, cv2.COLOR_BGR2RGB))
        ax1f2.set_title('Outsu Threshold Covid-19 patient')
        ax1f2.axis("off")
        
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(cv2.cvtColor(imageHelth, cv2.COLOR_BGR2RGB))
        ax1f3.set_title('Normal person CT scan image')
        ax1f3.axis("off")
        
        ret2,threshOutsuHealth = cv2.threshold(imageHelth,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ax1f4 = fig.add_subplot(224)
        ax1f4.imshow(cv2.cvtColor(threshOutsuHealth, cv2.COLOR_BGR2RGB))
        ax1f4.set_title('Outsu Threshold normal person')
        ax1f4.axis("off")
        
        self.setting_for_figures()
        
    def show_plot_threshold_slider(self)   :
        print('show_plot_threshold')
        global ch_THRESH_BINARY, ch_THRESH_TRUNC, ch_THRESH_TOZERO
        global pageNumberImage
        # pageNumberImage = 4
        
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.9,bottom=0.075,left=0.04,right=0.965,hspace=0.2,wspace=0.2)
        
       
        ax1f8 = fig.add_subplot(241)
        ax1f8.imshow(imageOriginal, 'gray')
        ax1f8.set_title('covid-19 patient CT scan')
        ax1f8.axis("off")
        
        ax1f4 = fig.add_subplot(242)
        ax1f4.hist(imageOriginal.ravel(),256,[0,256])
        ax1f4.set_title('Histogram of Covid-19 patient')
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,ch_THRESH_BINARY,255,cv2.THRESH_BINARY)
        ax1f1 = fig.add_subplot(243)
        ax1f1.imshow(THRESH_BINARY, 'gray')
        ax1f1.set_title('THRESH_BINARY for Covid-19 patient')
        ax1f1.axis("off")
        
        ax1f5 = fig.add_subplot(244)
        ax1f5.hist(THRESH_BINARY.ravel(),256,[0,256])
        ax1f5.set_title('Histogram of THRESH_BINARY ')
        
        
        ret,THRESH_TRUNC = cv2.threshold(imageOriginal,ch_THRESH_TRUNC,255,cv2.THRESH_TRUNC)
        ax1f2 = fig.add_subplot(245)
        ax1f2.imshow(THRESH_TRUNC, 'gray')
        ax1f2.set_title('THRESH_TRUNC for Covid-19 patient')
        ax1f2.axis("off")
        
        ax1f6 = fig.add_subplot(246)
        ax1f6.hist(THRESH_TRUNC.ravel(),256,[0,256])
        ax1f6.set_title('Histogram of THRESH_TRUNC ')
        
        ret,THRESH_TOZERO = cv2.threshold(imageOriginal,ch_THRESH_TOZERO,255,cv2.THRESH_TOZERO)
        ax1f3 = fig.add_subplot(247)
        ax1f3.imshow(THRESH_TOZERO, 'gray')
        ax1f3.set_title('THRESH_TOZERO for Covid-19 patient')
        ax1f3.axis("off")
        
        ax1f7 = fig.add_subplot(248)
        ax1f7.hist(THRESH_TOZERO.ravel(),256,[0,256])
        ax1f7.set_title('Histogram of THRESH_TOZERO')
        
        self.setting_for_figures()
    
    def get_valu_slider_tresh(self):
        
        # print('Bins number: ' + str(self.ui.binSlider.value()))
        strBinNumber = 'Threshold value: ' + str(self.ui.slider_threshold.value())
        self.ui.tx_tresh_value.setText(strBinNumber)
        
    def process_image_tresh(self):
        global ch_THRESH_BINARY,  ch_THRESH_TRUNC, ch_THRESH_TOZERO
        
        boolBinary = self.ui.ch_THRESH_BINARY.isChecked()
        boolTrunc = self.ui.ch_THRESH_TRUNC.isChecked()
        boolTozero = self.ui.ch_THRESH_TOZERO.isChecked()
        
        if boolBinary and not boolTrunc and not boolTozero:
            ch_THRESH_BINARY =  int(self.ui.slider_threshold.value())
        
        elif boolTrunc and not boolBinary and not boolTozero:
            ch_THRESH_TRUNC = int(self.ui.slider_threshold.value())
            
        elif boolTozero and not boolBinary and not boolTrunc :
            ch_THRESH_TOZERO = int(self.ui.slider_threshold.value())
            
        elif boolBinary and boolTrunc and not boolTozero:
            ch_THRESH_BINARY =  int(self.ui.slider_threshold.value())
            ch_THRESH_TRUNC = int(self.ui.slider_threshold.value())
            
        elif boolBinary and not boolTrunc and boolTozero:
            ch_THRESH_BINARY =  int(self.ui.slider_threshold.value())
            ch_THRESH_TOZERO = int(self.ui.slider_threshold.value())
            
        elif boolTrunc and boolTozero and not boolBinary:
            ch_THRESH_TRUNC = int(self.ui.slider_threshold.value())
            ch_THRESH_TOZERO = int(self.ui.slider_threshold.value())
            
        elif boolTrunc and boolTozero and boolBinary:
            ch_THRESH_BINARY =  int(self.ui.slider_threshold.value())
            ch_THRESH_TRUNC = int(self.ui.slider_threshold.value())
            ch_THRESH_TOZERO = int(self.ui.slider_threshold.value())   
            
        self.show_plot_threshold_slider()
        
        print('process image is clicked')
    def com_edge_selectionchange(self):
        # global textComMethodEdge, pageNumberEdge
        textComMethodEdge = self.ui.com_edge.currentText()
        pageNumberEdge = self.ui.com_edge.findText(textComMethodEdge, QtCore.Qt.MatchFixedString)
        
        if pageNumberEdge == 0:
            
            self.show_plot_canny()
        elif pageNumberEdge == 1:
            print('edge prewitt')
            self.show_plot_prewitt()
            
        elif pageNumberEdge == 2:
            print('sobel prewitt')
            self.show_plot_sobel()
        
    def set_text_edge(self,text):
        
        self.ui.txt_edge_binary.setText(str(text) + ' For Binary image')
        self.ui.txt_ede_method.setText(str(text) + ' for original image')
        
    def show_plot_canny(self):
        print('show_plot_canny')
        global threshBinary, cannyThreshOne, cannyThreshTwo
        global pageNumberImage, outsuCanny
        # pageNumberImage = 5
       
        self.ui.gp_canny.setVisible(True)
        
        self.set_text_edge('Canny')
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        # fig.subplots_adjust(vspace = 0.5)
         
        outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.ui.txt_outsu.setText('Otsu Threshold value:' + str(outsuVal))
        outsuCanny = outsuVal
        
        if threshBinary == 0:
            self.ui.slider_thresh_canny.setValue(int(outsuVal))
            threshBinary = outsuVal
            # self.ui.slider_threshold.setValue(threshBinary)
       
            
            
         
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(imageOriginal, 'gray')
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,threshBinary,255,cv2.THRESH_BINARY)
        ax1f2 = fig.add_subplot(222)
        ax1f2.imshow(cv2.cvtColor(THRESH_BINARY, cv2.COLOR_BGR2RGB))
        ax1f2.set_title('Threshold binary Covid-19 patient')
        ax1f2.axis("off")
        
        edges = cv2.Canny(THRESH_BINARY,cannyThreshOne,cannyThreshTwo)
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(edges, 'gray')
        ax1f3.set_title('Canny with binary image')
        ax1f3.axis("off")
        
        edges = cv2.Canny(imageOriginal,cannyThreshOne,cannyThreshTwo)
        ret2,threshOutsuHealth = cv2.threshold(edges,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ax1f4 = fig.add_subplot(224)
        ax1f4.imshow(cv2.cvtColor(threshOutsuHealth, cv2.COLOR_BGR2RGB))
        ax1f4.set_title('Canny with Covid-19 patient CT image')
        ax1f4.axis("off")    
        
        
        
        self.setting_for_figures()
        
    def show_plot_prewitt(self):
        print('show_plot_canny')
        global threshBinary, cannyThreshOne, cannyThreshTwo
        global pageNumberImage, outsuCanny
        # pageNumberImage = 5
        # self.ui.gp_tresh.setVisible(False)
        # self.ui.gp_edgedetection.setVisible(True)
        self.ui.gp_canny.setVisible(False)
        # self.set_text_edge('Prewitt')
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        # fig.subplots_adjust(vspace = 0.5)
         
        #prewitt
        kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        img_prewittx = cv2.filter2D(imageOriginal, -1, kernelx)
        img_prewitty = cv2.filter2D(imageOriginal, -1, kernely)
        imgPrewitt = img_prewittx + img_prewitty
         
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(imageOriginal, 'gray')
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        
        ax1f2 = fig.add_subplot(222)
        ax1f2.imshow(img_prewittx, 'gray')
        ax1f2.set_title('Prewitt gradiant X for Covid-19 patient')
        ax1f2.axis("off")
        
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(img_prewitty, 'gray')
        ax1f3.set_title('Prewitt gradiant Y for Covid-19 patient')
        ax1f3.axis("off")
        
        
        ax1f4 = fig.add_subplot(224)
        ax1f4.imshow(imgPrewitt, 'gray')
        ax1f4.set_title('Prewitt for Covid-19 patient')
        ax1f4.axis("off")    
        
        
        
        self.setting_for_figures()
        
    def show_plot_sobel(self):
        print('show_plot_canny')
        global threshBinary, cannyThreshOne, cannyThreshTwo
        global pageNumberImage, outsuCanny
        # pageNumberImage = 5
        # self.ui.gp_tresh.setVisible(False)
        # self.ui.gp_edgedetection.setVisible(True)
        self.ui.gp_canny.setVisible(False)
        # self.set_text_edge('Prewitt')
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        # fig.subplots_adjust(vspace = 0.5)
         
        #sobel
        img_sobelx = cv2.Sobel(imageOriginal,cv2.CV_8U,1,0,ksize=3)
        img_sobely = cv2.Sobel(imageOriginal,cv2.CV_8U,0,1,ksize=3)
        abs_grad_x = cv2.convertScaleAbs(img_sobelx)
        abs_grad_y = cv2.convertScaleAbs(img_sobely)
        img_sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
         
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(imageOriginal, 'gray')
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        
        ax1f2 = fig.add_subplot(222)
        ax1f2.imshow(img_sobelx, 'gray')
        ax1f2.set_title('Sobel gradiant X for Covid-19 patient')
        ax1f2.axis("off")
        
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(img_sobely, 'gray')
        ax1f3.set_title('Sobel gradiant Y for Covid-19 patient')
        ax1f3.axis("off")
        
        
        ax1f4 = fig.add_subplot(224)
        ax1f4.imshow(img_sobel, 'gray')
        ax1f4.set_title('Sobel Covid-19 CT patient')
        ax1f4.axis("off")    
        
        
        
        self.setting_for_figures()
        
    def com_filter_selectionchange(self):
        global pageNumberFilter
        textComMethodFilter = self.ui.com_filter.currentText()
        pageNumberFilter = self.ui.com_filter.findText(textComMethodFilter, QtCore.Qt.MatchFixedString)
        
        if pageNumberFilter == 0:
            
            self.show_plot_Median()
        elif pageNumberFilter == 1:
            self.show_plot_Guassian()
            
        elif pageNumberFilter == 2:
            self.show_plot_Averaging()
            
        elif pageNumberFilter == 3:
            self.show_plot_Laplacian()
    
    ####### Morphology #######################
    # Morpholigy combo box 
    def morphology_part_call(self):
        
        # self.show_plot_erosion()
        self.fill_comboBox_morphology(morphologyListName)
        
    def com_morphology_selectionchange(self):
        global pageNumberMorph
        textComMethodMorph = self.ui.com_morphology.currentText()
        pageNumberMorph = self.ui.com_morphology.findText(textComMethodMorph, QtCore.Qt.MatchFixedString)
        print('pageNumberMorph' + str(pageNumberMorph))
        if pageNumberMorph == 0:
            self.show_plot_erosion()
            
        elif pageNumberMorph == 1:
            self.show_plot_dilation()
            
        elif pageNumberMorph == 2:
            self.show_plot_opening()
            
        elif pageNumberMorph == 3:
            self.show_plot_closing()
    
    def fill_comboBox_morphology(self,listMethod):
        self.ui.com_morphology.clear() 
        # self.ui.comboBox.addItems(['Select Country'])
        self.ui.com_morphology.addItems(listMethod)  
        
    def get_valu_slider_thresh_morph(self):
        
        # print('Bins number: ' + str(self.ui.binSlider.value()))
        strBinNumber = 'Threshold Value: ' + str(self.ui.slider_thresh_morph.value())
        self.ui.txt_tresh_morph.setText(strBinNumber)
    def process_image_morph(self):
        global pageNumberMorph
        
        if pageNumberMorph == 0:
            
            self.show_plot_erosion()
        elif pageNumberMorph == 1:
            self.show_plot_dilation()
            
        elif pageNumberMorph == 2:
            self.show_plot_opening()
            
        elif pageNumberMorph == 3:
            self.show_plot_closing()
    
    def show_plot_erosion(self):
        print('show_plot_erosion')
        global threshBinaryErosion
        global pageNumberMorph, outsuErosion
        # pageNumberImage = 5
        
        self.ui.sp_morph_iter.setVisible(True)
        
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(hspace = 0.5)
         
        
        
        # get the value of threshold
        if threshBinaryErosion == 0:
            outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.ui.txt_tresh_morph.setText('Threshold Value:' + str(int(outsuVal)))
            outsuErosion = outsuVal
            self.ui.txt_otsu_morph.setText('Otsu Value: '+ str(int(outsuVal)))
            self.ui.slider_thresh_morph.setValue(int(outsuVal))
            threshBinaryErosion = outsuVal
        else:
            threshBinaryErosion = self.ui.slider_thresh_morph.value()
            
        # getting value of kernel and iter
        valueSpKernelMorph = self.ui.sp_morph_kernel.value() 
        valueSpItMorph = self.ui.sp_morph_iter.value()
        kernel = np.ones((valueSpKernelMorph,valueSpKernelMorph),np.uint8)
        ######
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,threshBinaryErosion,255,cv2.THRESH_BINARY)
        ax1f2 = fig.add_subplot(121)
        ax1f2.imshow(THRESH_BINARY, 'gray')
        ax1f2.set_title('Threshold binary Covid-19 patient')
        ax1f2.axis("off")
        
        erosion = cv2.erode(THRESH_BINARY,kernel,iterations = valueSpItMorph)
        ax1f3 = fig.add_subplot(122)
        ax1f3.imshow(erosion, 'gray')
        ax1f3.set_title('Erosion with binary image')
        ax1f3.axis("off")
       
        
        self.setting_for_figures()
        
    def show_plot_dilation(self):
        print('show_plot_deliation')
        global outsuErosion
        global pageNumberMorph, outsuErosion
        self.ui.sp_morph_iter.setVisible(True)
        # pageNumberImage = 5
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(hspace = 0.5)
         
     
        # get the value of threshold
        
        threshBinaryErosion = self.ui.slider_thresh_morph.value()
            
        # getting value of kernel and iter
        valueSpKernelMorph = self.ui.sp_morph_kernel.value() 
        valueSpItMorph = self.ui.sp_morph_iter.value()
        kernel = np.ones((valueSpKernelMorph,valueSpKernelMorph),np.uint8)
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,threshBinaryErosion,255,cv2.THRESH_BINARY)
        ax1f2 = fig.add_subplot(121)
        ax1f2.imshow(THRESH_BINARY, 'gray')
        ax1f2.set_title('Threshold binary Covid-19 patient')
        ax1f2.axis("off")
        
        dilation = cv2.dilate(THRESH_BINARY,kernel,iterations = valueSpItMorph)
        ax1f3 = fig.add_subplot(122)
        ax1f3.imshow(dilation, 'gray')
        ax1f3.set_title('Dilation with binary image')
        ax1f3.axis("off")
       
        
        self.setting_for_figures()
        
    def show_plot_opening(self):
        print('show_plot_opening')
        global threshBinaryErosion
        global pageNumberMorph, outsuErosion
        self.ui.sp_morph_iter.setVisible(False)
        
        # pageNumberImage = 5
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(hspace = 0.5)
         
        # outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # self.ui.txt_tresh_morph.setText('Threshold Value:' + str(int(outsuVal)))
        # outsuErosion = outsuVal
        
        # get the value of threshold
        
        threshBinaryErosion = self.ui.slider_thresh_morph.value()
            
        # getting value of kernel and iter
        valueSpKernelMorph = self.ui.sp_morph_kernel.value() 
        # valueSpItMorph = self.ui.sp_morph_iter.value()
        kernel = np.ones((valueSpKernelMorph,valueSpKernelMorph),np.uint8)
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,threshBinaryErosion,255,cv2.THRESH_BINARY)
        ax1f2 = fig.add_subplot(121)
        ax1f2.imshow(THRESH_BINARY, 'gray')
        ax1f2.set_title('Threshold binary Covid-19 patient')
        ax1f2.axis("off")
        
        opening = cv2.morphologyEx(THRESH_BINARY, cv2.MORPH_OPEN, kernel)
        ax1f3 = fig.add_subplot(122)
        ax1f3.imshow(opening, 'gray')
        ax1f3.set_title('Opening with binary image')
        ax1f3.axis("off")
       
        
        self.setting_for_figures()
        
    def show_plot_closing(self):
        print('show_plot_closing')
        global threshBinaryErosion
        global pageNumberMorph, outsuErosion
        self.ui.sp_morph_iter.setVisible(False)
        
        # pageNumberImage = 5
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(hspace = 0.5)
         
        # outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # self.ui.txt_tresh_morph.setText('Threshold Value:' + str(int(outsuVal)))
        # outsuErosion = outsuVal
        
        # get the value of threshold
        
        threshBinaryErosion = self.ui.slider_thresh_morph.value()
            
        # getting value of kernel and iter
        valueSpKernelMorph = self.ui.sp_morph_kernel.value() 
        kernel = np.ones((valueSpKernelMorph,valueSpKernelMorph),np.uint8)
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,threshBinaryErosion,255,cv2.THRESH_BINARY)
        ax1f2 = fig.add_subplot(121)
        ax1f2.imshow(THRESH_BINARY, 'gray')
        ax1f2.set_title('Threshold binary Covid-19 patient')
        ax1f2.axis("off")
        
        closing = cv2.morphologyEx(THRESH_BINARY, cv2.MORPH_CLOSE, kernel)
        ax1f3 = fig.add_subplot(122)
        ax1f3.imshow(closing, 'gray')
        ax1f3.set_title('Closing with binary image')
        ax1f3.axis("off")
       
        
        self.setting_for_figures()
    ### End Morphology ##########################
    
    #### Compare part ###########################
    
    def compare_part_call(self):
        
        # self.show_plot_erosion()
        self.show_plot_opening_compare_automat()
        print('compare_part_call')
        
  
        
    def get_valu_slider_thresh_compare(self):
        
        # print('Bins number: ' + str(self.ui.binSlider.value()))
        strBinNumber = 'Threshold Value: ' + str(self.ui.slider_tresh_compare.value())
        self.ui.txt_tresh_compare.setText(strBinNumber)
        
    def com_compare_type_selectionchange(self):
        
        global pageNumberCompareType
        textComMethodCompareType = self.ui.com_compare_type.currentText()
        pageNumberCompareType = self.ui.com_compare_type.findText(textComMethodCompareType, QtCore.Qt.MatchFixedString)
        print('pageNumberMorph' + str(pageNumberCompareType))
        if pageNumberCompareType == 0:
            
            self.ui.gp_compare_manual.setVisible(False)
            self.show_plot_opening_compare_automat()
            
        elif pageNumberCompareType == 1:
            self.ui.gp_compare_manual.setVisible(True)
            self.show_plot_opening_compare()
       
            
    def process_image_compare(self):
        global pageNumberMorph
        self.show_plot_opening_compare()
        
    
    def show_plot_opening_compare(self):
        print('show_plot_opening')
        global threshBinaryCompareCovid, valueSpKernelCompareCovid, threshBinaryCompareHealth,valueSpKernelCompareHealth
        global pageNumberMorph, outsuErosion,imageHelth
        # self.ui.sp_morph_iter.setVisible(False)
        
        # pageNumberImage = 5
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        fig.subplots_adjust(top=0.905,bottom=0.06,left=0.11,right=0.9,hspace=0.2,wspace=0.2)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
         
        # get the value of threshold
        
        if self.ui.rd_covid_compare.isChecked() and threshBinaryCompareCovid == 0:
            outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.ui.txt_otsu_compare.setText('Otsu value: ' + str(int(outsuVal)))
            threshBinaryCompareCovid = outsuVal
            self.ui.slider_tresh_compare.setValue(int(outsuVal))
            valueSpKernelCompareCovid = 31
            self.ui.sp_kernel_compare.setValue(valueSpKernelCompareCovid)
            
        elif self.ui.rd_covid_compare.isChecked():
            threshBinaryCompareCovid = self.ui.slider_tresh_compare.value()
            valueSpKernelCompareCovid = self.ui.sp_kernel_compare.value()
       
            
        # getting value of kernel and iter
       
        kernel = np.ones((valueSpKernelCompareCovid,valueSpKernelCompareCovid),np.uint8)
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,threshBinaryCompareCovid,255,cv2.THRESH_BINARY)
        ax1f2 = fig.add_subplot(231)
        ax1f2.imshow(THRESH_BINARY, 'gray')
        ax1f2.set_title('Threshold binary Covid-19 patient')
        ax1f2.axis("off")
        
        
        opening = cv2.morphologyEx(THRESH_BINARY, cv2.MORPH_OPEN, kernel)
        labelsCovidInfo = (255-opening)
        labelsCovidInfo = measure.label(labelsCovidInfo)
        labelsCovid = measure.label(opening)
        cmap = plt.cm.gnuplot
        ax1f3 = fig.add_subplot(232)
        ax1f3.imshow(labelsCovid,cmap)
        ax1f3.set_title('Opening method for Covid patient')
        ax1f3.axis("off")
        
        resultCovid = THRESH_BINARY - opening
        ax1f3 = fig.add_subplot(233)
        ax1f3.imshow(resultCovid, 'gray')
        ax1f3.set_title('Subtract binary image from opening for Covid patient')
        ax1f3.axis("off")
        
        #### health part
        
        if threshBinaryCompareHealth == 0:
            outsuVal,thresh6 = cv2.threshold(imageHelth,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            threshBinaryCompareHealth = outsuVal
            valueSpKernelCompareHealth = 17
            self.ui.sp_kernel_compare.setValue(valueSpKernelCompareHealth)
            
        elif self.ui.rd_health_compare.isChecked():
            threshBinaryCompareHealth = self.ui.slider_tresh_compare.value()
            valueSpKernelCompareHealth = self.ui.sp_kernel_compare.value()
        
        kernel = np.ones((valueSpKernelCompareHealth,valueSpKernelCompareHealth),np.uint8)
        
        ret,THRESH_BINARY = cv2.threshold(imageHelth,threshBinaryCompareHealth,255,cv2.THRESH_BINARY)
        ax1f3 = fig.add_subplot(234)
        ax1f3.imshow(THRESH_BINARY, 'gray')
        ax1f3.set_title('Threshold binary healthy person')
        ax1f3.axis("off")
        
        
        opening = cv2.morphologyEx(THRESH_BINARY, cv2.MORPH_OPEN, kernel)
        labelsHealthInfo = (255-opening)
        labelsHealthInfo = measure.label(labelsHealthInfo)
        labelsHealth = measure.label(opening)
        cmap = plt.cm.gnuplot
        ax1f3 = fig.add_subplot(235)
        ax1f3.imshow(labelsHealth,cmap)
        ax1f3.set_title('Opening method for healthy person')
        ax1f3.axis("off")
        
        resultHealth = THRESH_BINARY - opening
        ax1f3 = fig.add_subplot(236)
        ax1f3.imshow(resultHealth, 'gray')
        ax1f3.set_title('Subtract binary image from opening for healthy person')
        ax1f3.axis("off")
       
        
        self.setting_for_figures()
        
        ### set info
        self.set_info_compare(resultCovid, resultHealth,labelsCovidInfo,labelsHealthInfo)
        
    def show_plot_opening_compare_automat(self):
        print('show_plot_opening')
        
        # self.ui.sp_morph_iter.setVisible(False)
        
        # pageNumberImage = 5
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
         
        # get the value of threshold
        
        
        outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        
        # getting value of kernel and iter
       
        kernelCovid = np.ones((31,31),np.uint8)
        
        ret,THRESH_BINARY = cv2.threshold(imageOriginal,outsuVal,255,cv2.THRESH_BINARY)
        ax1f2 = fig.add_subplot(221)
        ax1f2.imshow(THRESH_BINARY, 'gray')
        ax1f2.set_title('Threshold binary Covid-19 patient')
        ax1f2.axis("off")
        
        
        opening = cv2.morphologyEx(THRESH_BINARY, cv2.MORPH_OPEN, kernelCovid)
        labelsCovidInfo = (255-opening)
        labelsCovidInfo = measure.label(labelsCovidInfo)
        resultCovid = THRESH_BINARY - opening
        ax1f3 = fig.add_subplot(222)
        ax1f3.imshow(resultCovid, 'gray')
        ax1f3.set_title('Subtract binary image from opening for Covid patient')
        ax1f3.axis("off")
        
        #### health part
        
        
        outsuVal,thresh6 = cv2.threshold(imageHelth,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        kernelHealth = np.ones((17,17),np.uint8)
        
        ret,THRESH_BINARY = cv2.threshold(imageHelth,outsuVal,255,cv2.THRESH_BINARY)
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(THRESH_BINARY, 'gray')
        ax1f3.set_title('Threshold binary healthy person')
        ax1f3.axis("off")
        
        
        opening = cv2.morphologyEx(THRESH_BINARY, cv2.MORPH_OPEN, kernelHealth)
        labelsHealthInfo = (255-opening)
        labelsHealthInfo = measure.label(labelsHealthInfo)
        resultHealth = THRESH_BINARY - opening
        ax1f3 = fig.add_subplot(224)
        ax1f3.imshow(resultHealth, 'gray')
        ax1f3.set_title('Subtract binary image from opening for healthy person')
        ax1f3.axis("off")
       
        
        self.setting_for_figures()
        
        ### set info
        self.set_info_compare(resultCovid, resultHealth, labelsCovidInfo, labelsHealthInfo )
        
    def rd_covid_compare_check(self):
        global threshBinaryCompareCovid, valueSpKernelCompareCovid
        if self.ui.rd_covid_compare.isChecked() and threshBinaryCompareCovid == 0:
            
            outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.ui.txt_otsu_compare.setText('Otsu value: ' + str(int(outsuVal)))
            threshBinaryCompareCovid = outsuVal
            self.ui.slider_tresh_compare.setValue(int(outsuVal))
            
        elif self.ui.rd_covid_compare.isChecked():
            outsuVal,thresh6 = cv2.threshold(imageOriginal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.ui.txt_otsu_compare.setText('Otsu value: ' + str(int(outsuVal)))
            self.ui.slider_tresh_compare.setValue(int(threshBinaryCompareCovid))
            self.ui.sp_kernel_compare.setValue(valueSpKernelCompareCovid)
            
    def rd_health_compare_check(self):
        
        global threshBinaryCompareHealth, valueSpKernelCompareHealth
        if self.ui.rd_health_compare.isChecked() and threshBinaryCompareHealth == 0 :
            outsuVal,thresh6 = cv2.threshold(imageHelth,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.ui.txt_otsu_compare.setText('Otsu value: ' + str(int(outsuVal))) 
            self.ui.slider_tresh_compare.setValue(int(outsuVal))
            self.ui.sp_kernel_compare.setValue(3)
            
        elif self.ui.rd_health_compare.isChecked():
            outsuVal,thresh6 = cv2.threshold(imageHelth,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.ui.txt_otsu_compare.setText('Otsu value: ' + str(int(outsuVal))) 
            self.ui.slider_tresh_compare.setValue(int(threshBinaryCompareHealth))
            self.ui.sp_kernel_compare.setValue(valueSpKernelCompareHealth)
            
    def set_info_compare(self,imageCovid, imageHealth,labelsCovid,lablesHealth):
        
        propsCovid = measure.regionprops(labelsCovid)
        areaCovid = []
        for prop in propsCovid:
            areaCovid.append(prop.area) 
        
        propsHealth = measure.regionprops(lablesHealth)
        areaHealth = []
        for prop in propsHealth:
            areaHealth.append(prop.area) 
        
        resultHealthPixel = 0
        if len(areaHealth)>3:
            resultHealthPixel = (max(areaHealth))
            areaHealth.remove(resultHealthPixel)
            resultHealthPixel = resultHealthPixel + max(areaHealth)
        
        print(areaCovid)
        resultCovidPixel = 0
        if len(areaCovid)>3:
            resultCovidPixel = (max(areaCovid))
            areaCovid.remove(resultCovidPixel)
            resultCovidPixel = resultCovidPixel + max(areaCovid)
        elif len(areaCovid)<=3:
            resultCovidPixel = (max(areaCovid))
            
        whiteCovid = Calculation.count_white(imageCovid)
        whiteHealth = Calculation.count_white(imageHealth)
        
        rowCovid, colCovid = imageCovid.shape
        rowHealth, colHealth = imageHealth.shape
        
        # sizeCovid = rowCovid*colCovid
        # sizeHealthd = rowHealth*colHealth
        percentRatioCovid = round((whiteCovid/resultCovidPixel) *100,2)
        percentRatioHealth = round((whiteHealth/resultHealthPixel) *100,2)
        percentageTotal = round((percentRatioCovid/percentRatioHealth) *10,2)
        
        print(percentageTotal)
        self.ui.txt_normal_compare.setText(str(percentRatioHealth) + ' %')
        self.ui.txt_covid_compare.setText(str(percentRatioCovid) + ' %')
        # self.ui.txt_percentage_compare.setText('Percentage of disease: ' + str(percentageTotal))
        
        print(areaCovid)
        print(areaHealth)
        print(resultHealthPixel)
        
    ##### End Compare ###########################
    
    def process_image_filter(self):
        global pageNumberFilter,valueSpinBox
        valueSpinBox = self.ui.spinBox.value() 
        if pageNumberFilter == 0:
            
            self.show_plot_Median()
        elif pageNumberFilter == 1:
            self.show_plot_Guassian()
            
        elif pageNumberFilter == 2:
            self.show_plot_Averaging()
            
        elif pageNumberFilter == 3:
            self.show_plot_Laplacian()
            
            
    def show_plot_Median(self):
        print('show_plot_canny')
        global pageNumberFilter,valueSpinBox
        # pageNumberImage = 5
        self.ui.gp_tresh.setVisible(False)
        self.ui.gp_edgedetection.setVisible(False)
        # self.ui.gp_canny.setVisible(False)
        self.ui.gp_filter.setVisible(True)
        # self.set_text_edge('Prewitt')
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(top=0.895,bottom=0.095,left=0.16,right=0.855,hspace=0.2,wspace=0.2)
         
        #sobel
        
        medianImage	= cv2.medianBlur(imageOriginal, ksize=valueSpinBox)
        
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(imageOriginal, 'gray')
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        ax1f2 = fig.add_subplot(222)
        ax1f2.hist(imageOriginal.ravel(),256,[0,256])
        ax1f2.set_title('Histogram of Covid-19 patient')
        
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(medianImage, 'gray')
        ax1f3.set_title('Median Image for Covid-19 patient')
        ax1f3.axis("off")
        
        ax1f4 = fig.add_subplot(224)
        ax1f4.hist(medianImage.ravel(),256,[0,256])
        ax1f4.set_title('Histogram of Median Image')
        
        
        self.setting_for_figures()
        
    def show_plot_Guassian(self):
        print('show_plot_canny')
        global pageNumberFilter,valueSpinBox
        # pageNumberImage = 5
        self.ui.gp_tresh.setVisible(False)
        self.ui.gp_edgedetection.setVisible(False)
        # self.ui.gp_canny.setVisible(False)
        self.ui.gp_filter.setVisible(True)
        # self.set_text_edge('Prewitt')
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(top=0.895,bottom=0.095,left=0.16,right=0.855,hspace=0.2,wspace=0.2)
         
        #sobel
        
        medianImage	= cv2.GaussianBlur(imageOriginal,(valueSpinBox,valueSpinBox),0 )
        
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(imageOriginal, 'gray')
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        ax1f2 = fig.add_subplot(222)
        ax1f2.hist(imageOriginal.ravel(),256,[0,256])
        ax1f2.set_title('Histogram of Covid-19 patient')
        
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(medianImage, 'gray')
        ax1f3.set_title('Gaussian Image for Covid-19 patient')
        ax1f3.axis("off")
        
        ax1f4 = fig.add_subplot(224)
        ax1f4.hist(medianImage.ravel(),256,[0,256])
        ax1f4.set_title('Histogram of Gaussian Image')
        
        
        self.setting_for_figures()
        
    def show_plot_Averaging(self):
        print('show_plot_canny')
        global pageNumberFilter,valueSpinBox
        # pageNumberImage = 5
        self.ui.gp_tresh.setVisible(False)
        self.ui.gp_edgedetection.setVisible(False)
        # self.ui.gp_canny.setVisible(False)
        self.ui.gp_filter.setVisible(True)
        # self.set_text_edge('Prewitt')
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(top=0.895,bottom=0.095,left=0.16,right=0.855,hspace=0.2,wspace=0.2)
         
        #sobel
        
        medianImage	= cv2.blur(imageOriginal,(valueSpinBox,valueSpinBox))
        
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(imageOriginal, 'gray')
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        ax1f2 = fig.add_subplot(222)
        ax1f2.hist(imageOriginal.ravel(),256,[0,256])
        ax1f2.set_title('Histogram of Covid-19 patient')
        
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(medianImage, 'gray')
        ax1f3.set_title('Averaging Image for Covid-19 patient')
        ax1f3.axis("off")
        
        ax1f4 = fig.add_subplot(224)
        ax1f4.hist(medianImage.ravel(),256,[0,256])
        ax1f4.set_title('Histogram of Averaging Image')
        
        
        self.setting_for_figures()
        
    def show_plot_Laplacian(self):
        print('show_plot_canny')
        global pageNumberFilter,valueSpinBox
        # pageNumberImage = 5
        self.ui.gp_tresh.setVisible(False)
        self.ui.gp_edgedetection.setVisible(False)
        # self.ui.gp_canny.setVisible(False)
        self.ui.gp_filter.setVisible(True)
        # self.set_text_edge('Prewitt')
        
        self.remove_figures()
        
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ui.verticalLayout.addWidget(self.canvas)
        # fig.subplots_adjust(top=0.92,bottom=0.065,left=0.25,right=0.75,hspace=0.2,wspace=0.2)
        fig.subplots_adjust(top=0.895,bottom=0.095,left=0.16,right=0.855,hspace=0.2,wspace=0.2)
         
        #sobel
        medianImage = cv2.Laplacian(imageOriginal, cv2.CV_8U, ksize=valueSpinBox)
        medianImage = cv2.convertScaleAbs(medianImage)
        
        
        ax1f1 = fig.add_subplot(221)
        ax1f1.imshow(imageOriginal, 'gray')
        ax1f1.set_title('Covid-19 patient CT scan image')
        ax1f1.axis("off")
        
        ax1f2 = fig.add_subplot(222)
        ax1f2.hist(imageOriginal.ravel(),256,[0,256])
        ax1f2.set_title('Histogram of Covid-19 patient')
        
        ax1f3 = fig.add_subplot(223)
        ax1f3.imshow(medianImage, 'gray')
        ax1f3.set_title('Laplacian Image for Covid-19 patient')
        ax1f3.axis("off")
        
        ax1f4 = fig.add_subplot(224)
        ax1f4.hist(medianImage.ravel(),256,[0,256])
        ax1f4.set_title('Histogram of Laplacian Image')
        
        
        self.setting_for_figures()
        
    def get_valu_slider_canny_outsuthresh(self):
        
        # print('Bins number: ' + str(self.ui.binSlider.value()))
        strBinNumber = 'Threshold value: ' + str(self.ui.slider_thresh_canny.value())
        self.ui.txt_tresh_canny.setText(strBinNumber)
        
    def get_valu_slider_canny_thresh1(self):
        
        # print('Bins number: ' + str(self.ui.binSlider.value()))
        strBinNumber = 'Threshold value one: ' + str(self.ui.slider_tresh1.value())
        self.ui.txt_canny_tresh1.setText(strBinNumber)
        
    def get_valu_slider_canny_thresh2(self):
        
        # print('Bins number: ' + str(self.ui.binSlider.value()))
        strBinNumber = 'Threshold value two: ' + str(self.ui.slider_thresh2.value())
        self.ui.txt_canny_tresh2.setText(strBinNumber)
        
    def process_image_canny(self):
        global threshBinary, cannyThreshOne, cannyThreshTwo
        
        threshBinary =  int(self.ui.slider_thresh_canny.value())
        cannyThreshOne = int(self.ui.slider_tresh1.value())
        cannyThreshTwo = int(self.ui.slider_thresh2.value())
        
        self.show_plot_canny()
        
        
        print('process image is clicked')
        
    # show and hid the group box
    def setvisible_group_box(self,pageNumberImage):
        
        if pageNumberImage == 1:
            self.ui.gp_compare_image.setVisible(False)
            self.ui.gp_tresh.setVisible(False)
            self.ui.gp_gp_edgedetection.setVisible(False)
            self.ui.gp_filter.setVisible(False)
            self.ui.gp_morphology.setVisible(False)
        
            
        elif pageNumberImage == 2:
            self.ui.gp_compare_image.setVisible(False)
            self.ui.gp_tresh.setVisible(False)
            self.ui.gp_edgedetection.setVisible(False)
            self.ui.gp_filter.setVisible(False)
            self.ui.gp_morphology.setVisible(False)
            
        elif pageNumberImage == 3:
            self.ui.gp_compare_image.setVisible(False)
            self.ui.gp_edgedetection.setVisible(False)
            self.ui.gp_filter.setVisible(False)
            self.ui.gp_morphology.setVisible(False)
            self.ui.gp_tresh.setVisible(True)
            
        elif pageNumberImage == 4:
            self.ui.gp_compare_image.setVisible(False)
            self.ui.gp_tresh.setVisible(False)
            self.ui.gp_filter.setVisible(False)
            self.ui.gp_morphology.setVisible(False)
            self.ui.gp_edgedetection.setVisible(True)
            
        # print(pageNumber)
        elif pageNumberImage == 5:
            self.ui.gp_compare_image.setVisible(False)
            self.ui.gp_tresh.setVisible(False)
            self.ui.gp_edgedetection.setVisible(False)
            self.ui.gp_morphology.setVisible(False)
            self.ui.gp_filter.setVisible(True)
            
        elif pageNumberImage == 6:
            self.ui.gp_compare_image.setVisible(False)
            self.ui.gp_tresh.setVisible(False)
            self.ui.gp_edgedetection.setVisible(False)
            self.ui.gp_filter.setVisible(False)
            self.ui.gp_morphology.setVisible(True)
            
        elif pageNumberImage == 7:
            
            self.ui.gp_tresh.setVisible(False)
            self.ui.gp_edgedetection.setVisible(False)
            self.ui.gp_filter.setVisible(False)
            self.ui.gp_morphology.setVisible(False)
            self.ui.gp_compare_manual.setVisible(False)
            self.ui.gp_compare_image.setVisible(True)
    
    def set_info_val(self):
        row, col = imageOriginal.shape
        self.ui.txt_size.setText('Size covid image: ' + str(row) + '*' + str(col))
    ############################################## Image part end ########################################
    def closeEvent(self,event):
        QApplication.quit()
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

