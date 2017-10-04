# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 13:59:37 2017

@author: CKAN
"""

import pandas as pd
from ops.socios import buildFeatureFrame, checkAnswer, loadTables
import feather

#List of random variables in Bayesian network
bn_n = ["monthly_income", "water_access", "roof_material", "wall_material", "cb_size", "floor_area", "geyser_nr"]

def features2000(year):
    #Define socio-demographic search terms corresponding to BN nodes - valid for surveys from 2000 onwards
    searchlist = ['earn per month', 'watersource', 'GeyserNumber', 'GeyserBroken', 'roof', 'wall', 'main switch', 'floor area']
    
    #Get data and questions from socio-demographic survey responses
    data = buildFeatureFrame(searchlist, year)
    featureframe = data[0]
    questions = data[1]
    
    featureframe['geyser_nr'] = featureframe['115'] - featureframe['131'] #geyser_nr = GeyserNumber - GeyserBroken
    featureframe.drop(['115','131'], axis=1, inplace=True) #remove superfluous geyser columns
    featureframe.columns = ['AnswerID'] + bn_n #rename columns to BN node names
    
    #Convert columns into datatypes that match BN node variables    
    income_bins = [0, 1800, 3200, 7800, 11600, 19116, 24500, 65600, 500000]
    income_labels = ['R0-R1799','R1800-R3199','R3200-R7799','R7800-R11599','R11600-R19115','R19116-R24499','R24500-R65499','+R65500']
#    floorarea_bins = []
#    floorarea_labels = []

    featureframe.monthly_income = pd.cut(featureframe.monthly_income, bins = income_bins, labels = income_labels, right=False, include_lowest=True)
#    featureframe.floor_area = pd.cut(featureframe.floor_area, bins = floorarea_bins, labels = floorarea_labels)
    featureframe.water_access = featureframe.water_access.astype(int)
    featureframe.roof_material = featureframe.roof_material.astype(int)
    featureframe.wall_material = featureframe.wall_material.astype(int)
    featureframe.cb_size = featureframe.cb_size.astype(int)
    featureframe.geyser_nr = featureframe.geyser_nr.astype(int)
    
    return featureframe

testanswercheck = checkAnswer(915, 'iron')

# NEED TO ASSOCIATE ANSWERID WITH PROFILEID

#mydata = featureFrame(features, 2011)[0]
#mydata = mydata.drop(['AnswerID','95'], axis=1)
#cols = ['Hi','Wa','Rm','Wm','Te']
#mydata.columns = cols

#playing with profiles
kW = feather.read_dataframe('E:\\git\\DLR_DB\\profiles\\raw\\2009\\2009-8\\2009-8_kW.feather')
kWh = kW.groupby(['UoM','RecorderID','ProfileID']).resample('1H', on='Datefield').sum()
kWd = kW.groupby(['UoM','RecorderID','ProfileID']).resample('1D', on='Datefield').sum()
kWm = kW.groupby(['UoM','RecorderID','ProfileID']).resample('1M', on='Datefield').sum()

recorder_ids = kW.RecorderID.cat.categories.tolist()

