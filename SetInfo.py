# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:00:29 2021

@author: Nima
"""
from readingdata import ReadingData
import numpy as np
from PyQt5.QtWidgets import QTableWidgetItem
class SetInfo():
    
    def set_info_new_deathes(self,df,textCombobox,new_death):
        print('set info set')
        SetInfo.covariance_matrix_cisibility(self,False)
        population = int(ReadingData.detial_list(df, textCombobox, 'population')[0])
        self.ui.txt_population.setText('Population: '+str(population))
        
        maxForDay = str(int(max(new_death)))
        self.ui.txt_max_case.setText('max new death in day: ' + maxForDay)
        
        indexMax = new_death.index(int(maxForDay))
        dateMax = ReadingData.detial_list(df, textCombobox, 'date')[indexMax]
        # dateMax = dateMax.
        self.ui.txt_date_max.setText('Date of max new death: ' + str(dateMax))
        
        variance = round(np.var(new_death),2)
        self.ui.txt_variance_new_cases.setText('Variance new deathes: ' + str(variance) )
        
        stdNew = round(np.std(new_death),2)
        self.ui.txt_std_new_case.setText('Std new deathes: ' + str(stdNew))
        
        meanNew = round(np.mean(new_death),2)
        self.ui.txt_mean_new_case.setText('Mean new deathes: ' + str(meanNew))
        
        self.ui.txt_co.setVisible(False)
        self.ui.txt_covariance.setVisible(False)
        # self.ui.txt_conclusion.setText('txt_conclusion')
        
    def set_info_new_case(self,df,textCombobox,new_case):
        print('set info set')
        population = int(ReadingData.detial_list(df, textCombobox, 'population')[0])
        self.ui.txt_population.setText('Population: '+str(population))
        SetInfo.covariance_matrix_cisibility(self,False)
        
        maxForDay = str(int(max(new_case)))
        self.ui.txt_max_case.setText('max new case in day: ' + maxForDay)
        
        indexMax = new_case.index(int(maxForDay))
        dateMax = ReadingData.detial_list(df, textCombobox, 'date')[indexMax]
        # dateMax = dateMax.
        self.ui.txt_date_max.setText('Date of max new case: ' + str(dateMax))
        
        variance = round(np.var(new_case),2)
        self.ui.txt_variance_new_cases.setText('Variance new cases: ' + str(variance) )
        
        stdNew = round(np.std(new_case),2)
        self.ui.txt_std_new_case.setText('Std new cases: ' + str(stdNew))
        
        meanNew = round(np.mean(new_case),2)
        self.ui.txt_mean_new_case.setText('Mean new cases: ' + str(meanNew))
        
        self.ui.txt_co.setVisible(False)
        self.ui.txt_covariance.setVisible(False)
        # self.ui.txt_conclusion.setText('txt_conclusion')
        
    def set_info_compare_new_deathes_new_cases(self,df,textCombobox,new_case,new_death):
        print('set info set')
        self.ui.txt_co.setVisible(True)
        self.ui.txt_covariance.setVisible(True)
        SetInfo.covariance_matrix_cisibility(self,True)
        
        population = int(ReadingData.detial_list(df, textCombobox, 'population')[0])
        self.ui.txt_population.setText('Population: '+str(population))
        
        maxForDay = str(int(max(new_case)))
        self.ui.txt_max_case.setText('max new case in day: ' + maxForDay)
        
        indexMax = new_case.index(int(maxForDay))
        dateMax = ReadingData.detial_list(df, textCombobox, 'date')[indexMax]
        # dateMax = dateMax.
        self.ui.txt_date_max.setText('Date of max new case: ' + str(dateMax))
        
        maxForDayDeath = str(int(max(new_death)))
        self.ui.txt_variance_new_cases.setText('max new death in day: ' + maxForDayDeath )
        
        indexMaxDe = new_death.index(int(maxForDayDeath))
        dateMaxDe = ReadingData.detial_list(df, textCombobox, 'date')[indexMaxDe]
        self.ui.txt_std_new_case.setText('Date of max new death: ' + str(dateMaxDe))
        
        # self.ui.txt_mean_new_case.setVisible(False)
        covDatat = np.cov(new_case,new_death)
        coCoeif = np.corrcoef(new_case,new_death)
        
        self.ui.txt_co.setText('Correlation coefficient: ' + str(np.round(coCoeif[1][0],3)))
        
      
        self.ui.txt_co_00.setText(str(np.round(covDatat[0][0],3)))
        self.ui.txt_co_01.setText(str(np.round(covDatat[0][1],3)))
        self.ui.txt_co_10.setText(str(np.round(covDatat[1][0],3)))
        self.ui.txt_co_11.setText(str(np.round(covDatat[1][1],3)))
        
    def set_info_compare_temp_new_cases(self,df,textCombobox,new_case,tempCountryDate):
        print('set info set')
        self.ui.txt_co.setVisible(True)
        self.ui.txt_covariance.setVisible(True)
        SetInfo.covariance_matrix_cisibility(self,True)
        
        population = int(ReadingData.detial_list(df, textCombobox, 'population')[0])
        self.ui.txt_population.setText('Population: '+str(population))
        
        print(max(new_case))
        maxForDay = str(int(max(new_case)))
        self.ui.txt_max_case.setText('max new case in day: ' + maxForDay)
        
        indexMax = new_case.index(int(maxForDay))
        dateMax = ReadingData.detial_list(df, textCombobox, 'date')[indexMax]
        # dateMax = dateMax.
        self.ui.txt_date_max.setText('Date of max new case: ' + str(dateMax))
        
        maxForDayDeath = str(int(max(tempCountryDate)))
        self.ui.txt_variance_new_cases.setText('max temp: ' + maxForDayDeath )
        
        # indexMaxDe = tempCountryDate.index(int(maxForDayDeath))
        # dateMaxDe = ReadingData.detial_list(df, textCombobox, 'date')[indexMaxDe]
        # self.ui.txt_std_new_case.setText('Date of max temp: ' + str(dateMaxDe))
        
        # self.ui.txt_mean_new_case.setVisible(False)
        covDatat = np.cov(new_case,tempCountryDate)
        coCoeif = np.corrcoef(new_case,tempCountryDate)
        
        self.ui.txt_co.setText('Correlation coefficient: ' + str(np.round(coCoeif[1][0],3)))
        
      
        self.ui.txt_co_00.setText(str(np.round(covDatat[0][0],3)))
        self.ui.txt_co_01.setText(str(np.round(covDatat[0][1],3)))
        self.ui.txt_co_10.setText(str(np.round(covDatat[1][0],3)))
        self.ui.txt_co_11.setText(str(np.round(covDatat[1][1],3)))
        
       
    def set_info_compare_temp_new_deathes(self,df,textCombobox,new_death,tempCountryDate):
        print('set info set')
        self.ui.txt_co.setVisible(True)
        self.ui.txt_covariance.setVisible(True)
        SetInfo.covariance_matrix_cisibility(self,True)
        
        population = int(ReadingData.detial_list(df, textCombobox, 'population')[0])
        self.ui.txt_population.setText('Population: '+str(population))
        
        maxForDay = str(int(max(new_death)))
        self.ui.txt_max_case.setText('max new case in day: ' + maxForDay)
        
        indexMax = new_death.index(int(maxForDay))
        dateMax = ReadingData.detial_list(df, textCombobox, 'date')[indexMax]
        # dateMax = dateMax.
        self.ui.txt_date_max.setText('Date of max new death: ' + str(dateMax))
        
        maxForDayDeath = str(int(max(tempCountryDate)))
        self.ui.txt_variance_new_cases.setText('max temp: ' + maxForDayDeath )
        
        # indexMaxDe = tempCountryDate.index(int(maxForDayDeath))
        # dateMaxDe = ReadingData.detial_list(df, textCombobox, 'date')[indexMaxDe]
        # self.ui.txt_std_new_case.setText('Date of max temp: ' + str(dateMaxDe))
        
        # self.ui.txt_mean_new_case.setVisible(False)
        covDatat = np.cov(new_death,tempCountryDate)
        coCoeif = np.corrcoef(new_death,tempCountryDate)
        
        self.ui.txt_co.setText('Correlation coefficient: ' + str(np.round(coCoeif[1][0],3)))
        
        
        self.ui.txt_co_00.setText(str(np.round(covDatat[0][0],3)))
        self.ui.txt_co_01.setText(str(np.round(covDatat[0][1],3)))
        self.ui.txt_co_10.setText(str(np.round(covDatat[1][0],3)))
        self.ui.txt_co_11.setText(str(np.round(covDatat[1][1],3)))
        
    def set_info_compare_two_countries_new_cases(self,df,firstCountyName,secondCountryName,
                                                 first_country_new_cases,second_country_new_cases):
        print('set info set')
        self.ui.txt_co.setVisible(True)
        self.ui.txt_covariance.setVisible(True)
        SetInfo.covariance_matrix_cisibility(self,True)
        
        populationFirst = int(ReadingData.detial_list(df, firstCountyName, 'population')[0])
        self.ui.txt_population.setText(firstCountyName + ' Population: '+str(populationFirst))
        
        populationSecond = int(ReadingData.detial_list(df, secondCountryName, 'population')[0])
        self.ui.txt_max_case.setText(secondCountryName + ' Population: '+str(populationSecond))
        
        maxForDayFirst = str(int(max(first_country_new_cases)))
        
        indexMaxFirst = first_country_new_cases.index(int(maxForDayFirst))
        dateMaxF = ReadingData.detial_list(df, firstCountyName, 'date')[indexMaxFirst]
        # dateMax = dateMax.
        self.ui.txt_date_max.setText(firstCountyName + ' date of max new cases: ' )
        
        maxForDaySecond = str(int(max(second_country_new_cases)))
        
        indexMaxSec = second_country_new_cases.index(int(maxForDaySecond))
        dateMaxS = ReadingData.detial_list(df, secondCountryName, 'date')[indexMaxSec]
        # dateMax = dateMax.
        self.ui.txt_variance_new_cases.setText(str(dateMaxF) )
        
       
        
        # indexMaxDe = tempCountryDate.index(int(maxForDayDeath))
        # dateMaxDe = ReadingData.detial_list(df, textCombobox, 'date')[indexMaxDe]
        self.ui.txt_std_new_case.setText(secondCountryName + ' date of max new cases: ')
        self.ui.txt_mean_new_case.setText(str(dateMaxS))
        
        covDatat = np.cov(first_country_new_cases,second_country_new_cases)
        coCoeif = np.corrcoef(first_country_new_cases,second_country_new_cases)
        
        self.ui.txt_co.setText('Correlation coefficient: ' + str(np.round(coCoeif[1][0],3)))
        
        
        self.ui.txt_co_00.setText(str(np.round(covDatat[0][0],3)))
        self.ui.txt_co_01.setText(str(np.round(covDatat[0][1],3)))
        self.ui.txt_co_10.setText(str(np.round(covDatat[1][0],3)))
        self.ui.txt_co_11.setText(str(np.round(covDatat[1][1],3)))
        
    def set_info_compare_two_countries_new_death(self,df,firstCountyName,secondCountryName,
                                                 first_country_new_death,second_country_new_death):
        print('set info set')
        self.ui.txt_co.setVisible(True)
        self.ui.txt_covariance.setVisible(True)
        SetInfo.covariance_matrix_cisibility(self,True)
        
        populationFirst = int(ReadingData.detial_list(df, firstCountyName, 'population')[0])
        self.ui.txt_population.setText(firstCountyName + ' Population: '+str(populationFirst))
        
        populationSecond = int(ReadingData.detial_list(df, secondCountryName, 'population')[0])
        self.ui.txt_max_case.setText(secondCountryName + ' Population: '+str(populationSecond))
        
        maxForDayFirst = str(int(max(first_country_new_death)))
        
        indexMaxFirst = first_country_new_death.index(int(maxForDayFirst))
        dateMaxF = ReadingData.detial_list(df, firstCountyName, 'date')[indexMaxFirst]
        # dateMax = dateMax.
        self.ui.txt_date_max.setText(firstCountyName + ' date of max new deaths: ' )
        
        maxForDaySecond = str(int(max(second_country_new_death)))
        
        indexMaxSec = second_country_new_death.index(int(maxForDaySecond))
        dateMaxS = ReadingData.detial_list(df, secondCountryName, 'date')[indexMaxSec]
        # dateMax = dateMax.
        self.ui.txt_variance_new_cases.setText(str(dateMaxF) )
        
       
        
        # indexMaxDe = tempCountryDate.index(int(maxForDayDeath))
        # dateMaxDe = ReadingData.detial_list(df, textCombobox, 'date')[indexMaxDe]
        self.ui.txt_std_new_case.setText(secondCountryName + ' date of max new deaths: ')
        self.ui.txt_mean_new_case.setText(str(dateMaxS))
        
        covDatat = np.cov(first_country_new_death,second_country_new_death)
        coCoeif = np.corrcoef(first_country_new_death,second_country_new_death)
        
        self.ui.txt_co.setText('Correlation coefficient: ' + str(np.round(coCoeif[1][0],3)))
        
        
        self.ui.txt_co_00.setText(str(np.round(covDatat[0][0],3)))
        self.ui.txt_co_01.setText(str(np.round(covDatat[0][1],3)))
        self.ui.txt_co_10.setText(str(np.round(covDatat[1][0],3)))
        self.ui.txt_co_11.setText(str(np.round(covDatat[1][1],3)))
           
    def covariance_matrix_cisibility(self,value):
        self.ui.txt_co_00.setVisible(value)
        self.ui.txt_co_01.setVisible(value)
        self.ui.txt_co_10.setVisible(value)
        self.ui.txt_co_11.setVisible(value)
        self.ui.txt_covariance.setVisible(value)
        
        
        # meanNew = round(np.mean(new_death),2)
        # self.ui.txt_mean_new_case.setText('Mean new deathes: ' + str(meanNew))
        
        # self.ui.txt_co.setVisible(False)
        # self.ui.txt_covariance.setVisible(False)
        # self.ui.txt_conclusion.setText('txt_conclusion')