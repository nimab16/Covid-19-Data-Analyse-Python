# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 17:27:28 2021

@author: Nima
"""
import pandas
import datetime
from calculation import Calculation


class ReadingData():
    
    def name_of_country(readingData):
        listOfCountrie = []
        
        countryName = 'st'
        nameListCountry = readingData['location'].tolist()
        for i in range(0,len(nameListCountry)):
            
            
            if str(nameListCountry[i]) != countryName :
                countryName  = nameListCountry[i]
                # print(countryName)
                listOfCountrie.append(countryName)
        return listOfCountrie
    
    #############################################
    def detial_list(df,countryName, detailName):
        
        listDate = []
        datel = df[detailName].tolist()
        locationL = df['location'].tolist()
        
        for k in range(0,len(datel)):
            if str(locationL[k]) == countryName:
                # print(datel[k])
                listDate.append(datel[k])
        return listDate

    ########################################################
    def get_dat_according_time(df, countryName, dataType, timeFrom, timeTo):
        
        datel = df['date'].tolist()
        locationL = df['location'].tolist()
        indexFrom = 0
        indexTo = 1
        
        for k in range(0,len(locationL)):
            if locationL[k] == countryName and datel[k] == timeFrom:
                        # print(datel[k])
                    print(k)
                    indexFrom = k
            elif locationL[k] == countryName and datel[k] == timeTo:
                        # print(datel[k])
                    # print(k)
                    indexTo = k
        
        datResultList = df[dataType].tolist()[indexFrom:indexTo]
        out_list = [abs(s) for s in datResultList]
        return out_list

###### calculating the temp ##################################################
    def create_time_list(dateIn,dateOut):
        dayStart = '2020-01-01'
        dayEnd = '2020-12-28'
        start = datetime.datetime.strptime(dayStart, "%Y-%m-%d")
        end = datetime.datetime.strptime(dayEnd,  "%Y-%m-%d")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
        
        timeList = []
        for i in range(0,len(date_generated)) :
            re = date_generated[i].strftime("%Y-%m-%d")
            if re == dateIn or re == dateOut:
                timeList.append(i)
            # timeList.append(date.strftime("%Y-%m-%d"))
        # print(timeList)
        return timeList 


    def temp_cal(countryName,dateIn,dateOut):
        
        nameCoun = countryName + '.csv'
        df = pandas.read_csv(nameCoun)
        # print(df.head())
        # df.astype({'NAME': 'str'}).dtypes
        # name = df['NAME'].tolist()
        stations = df['STATION'].tolist()
        # date = df['DATE'].tolist()
        # print(date[0:362])
        stations.append('end')
        temp = df['TAVG'].tolist()
        tempAvg = []
        tempAvg.append(temp[0])
        tempResult = []
        # dateRelate = []
        dateList = ReadingData.create_time_list(dateIn,dateOut)
        
        
        valueOfLenDay = 362
        for i in range(1,len(stations)):
            
            if stations[i-1] == stations[i] and str(temp[i]) != 'nan' :
                tempAvg.append(temp[i])
            
            else:
                sizeTemp = len(tempAvg)
                
                if sizeTemp > 355:
                   
                    diffS = valueOfLenDay - sizeTemp
                    for l in range(0,diffS):
                        tempAvg.append(tempAvg[-1])
                        
                    tempResult.append(tempAvg)
                    if stations[i] != 'end':
                        # print(tempResult)
                        tempAvg = []
                        tempAvg.append(temp[i])
                        
                else:
                    tempAvg = []
               
          
        # print(len(tempResult))    
    
        result = [0]*valueOfLenDay
        averageTempList = []
        for tempe in tempResult:
            result = [sum(pair) for pair in zip(result, tempe)]
        
        
        for tempDay in result:
            averageTemp = tempDay/len(tempResult)
            averageTempList.append(averageTemp)
        
        
        # print(averageTempList)
        return averageTempList[dateList[0]:dateList[1]]
    
    ###################################################################
    def get_dat_according_time_compare(df, countryName, dataType, timeFrom, timeTo):
        
        datel = df['date'].tolist()
        locationL = df['location'].tolist()
        indexFrom = -1
        indexTo = 1
        checkFirst = True
        
        for k in range(0,len(locationL)):
            if locationL[k] == countryName and datel[k] == timeFrom:
                        # print(datel[k])
                    print(k)
                    indexFrom = k
            elif locationL[k] == countryName and datel[k] == timeTo:
                        # print(datel[k])
                    # print(k)
                    indexTo = k
            elif locationL[k] == countryName and checkFirst:
                
                    indexFrom = k
                    checkFirst = False
            
            
        
            
        datResultList = df[dataType].tolist()[indexFrom:indexTo]
        out_list = [abs(s) for s in datResultList]
        return out_list
    
    def create_equal_list(df,firstCountry, secondCountry,detail,dateFrom,dateTo) :   
    
     
        firstCountry = Calculation.remove_nan_withZero(ReadingData.get_dat_according_time_compare(df,firstCountry,detail,dateFrom,dateTo))
        secondCountry = Calculation.remove_nan_withZero(ReadingData.get_dat_according_time_compare(df,secondCountry,detail,dateFrom,dateTo))
        
        if len(firstCountry) > len(secondCountry):
            diffLen = len(firstCountry)-len(secondCountry)
            for i in range(0,diffLen):
                secondCountry.insert(0, 0)
                
        elif len(secondCountry) > len(firstCountry):
            diffLen = len(secondCountry)-len(firstCountry)
            for i in range(0,diffLen):
                firstCountry.insert(0, 0)
                
        return firstCountry,secondCountry

    def shift_value(new_case,new_death,shift):
     print('shift_value') 
     endNewCase = len(new_case) - shift
     
     new_caseR = new_case[0:endNewCase]
     new_deathR = new_death[shift:]
     
     return new_caseR, new_deathR
     
     

    


