import pandas as pd
import numpy as np
import datetime

import os.path

import xml.etree.ElementTree as etree

def build_df():
    """this function creates an empty dataframe and then builds a dataframe
    from every relevant row in the xml file and then saves as csv"""

    """ This function takes a very long time to run, see `wrangle_xml()` function
    which checks to see if there is a csv before running this function """
    df = pd.DataFrame()
    for i in range(4,137028):
        dict_new = root[i].attrib
        df = df.append(dict_new, ignore_index=True)

    return df    

def wrangle_xml():
    """ this function checks to see if there is an existing csv
    if not runs build_df function""" 

    if os.path.isfile('./xml.csv'):
        df = pd.read_csv('xml.csv')

        df = df.drop(columns="Unnamed: 0")
    else:
   
        tree = etree.parse("export.xml")
    
        root = tree.getroot()
    
        df = build_df()
    
        df.to_csv('xml.csv')
    
    return df

def validate_data_sets():
    """looking into the xml data frame"""
    df = pd.DataFrame(root[4].attrib, index=[0])
    
    print(root[5].attrib['type'])
    
    ## check to see if attribute is step counter
    i = 4
    l = []
    while i < 67920:
        if root[i].attrib['type'] == 'HKQuantityTypeIdentifierStepCount':
            l.append[i]
        else:
            print(i)
            break
            i += 1
            
    root[67919].attrib
    
    m = []
    i = 67919
    while i < 1_000_000:
        if root[i].attrib['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
            m.append(i)
        else:
            print(f'{i} is false and break')
            break
        i += 1
        
    root[135827].attrib
    
    k = []
    i = 135827
    while i < 1_000_000:
        if root[i].attrib['type'] == 'HKQuantityTypeIdentifierFlightsClimbed':
            k.append(i)
        else:
            print(f'{i} is false and break')
            break
        i += 1
        
    root[137028].attrib
    
    j = []
    i = 0
    type_list = []
    while i < 1_000_000:
        if root[i].attrib['type'] in type_list:
            j.append(i)
        else:
            type_list.append(root[i].attrib['type'])
        i +=1
    
    type_list
    
    return type_list

def preprocessing_xml(df):
    """ function for processing dataframe into datetime format """
    
    # remove timezone from the column
    df['endDate'] = df.endDate.str.replace("-0500", "")
    df['startDate'] = df.startDate.str.replace("-0500", "")
    df['creationDate'] = df.creationDate.str.replace("-0500", "")
    
    # change the column into datetime
    df['endDate'] = pd.to_datetime(df.endDate)
    df['startDate'] = pd.to_datetime(df.startDate)
    df['creationDate'] = pd.to_datetime(df.creationDate) 
    
    
    # set index as creation date
    df = df.set_index('startDate')
    
    #reset index
    df = df.reset_index()
    
    return df


def make_df_by_resample(df, column):
    """Makes a resampled by day series for each of the date columns in xml df"""
    series = df.set_index(column).resample("D").value.sum()
    return series


def create_validate_xml_df():
    """This function will create a df to validate the three datetime columns from xml file as compared to the export.csv 
    from the pedometer application"""

    ### read in xml data
    df = wrangle_xml()
    
    ### segment xml data for steps only into new df
    df_steps = df[df.type == 'HKQuantityTypeIdentifierStepCount']
    
    ### preprocess df_steps
    df_steps = preprocessing_xml(df_steps)
    
    ### reset index on df_steps
    df_steps.reset_index(inplace=True)
    
    ### create `creationDate`, `startDate` and `endDate` resample series for merge
    create = make_df_by_resample(df_steps, "creationDate")
    end =  make_df_by_resample(df_steps, "endDate")
    start =  make_df_by_resample(df_steps, "startDate")
    
    ### create validate df from pedometer csv file
    df_validate = pd.read_csv("Export.csv")
    
    ### set datetime index for df_validate
    df_validate['Date'] = pd.to_datetime(df_validate.Date)
    
    ### merge all series with validate df
    df_validate = (df_validate.merge(start, left_on='Date', right_on='startDate')
    .rename(columns={"value": 'start_value'})
    .merge(create, left_on='Date', right_on='creationDate')
    .rename(columns={"value": 'create_value'})
    .merge(end, left_on='Date', right_on='endDate')
    .rename(columns={"value": 'end_value'})
    )
    
    return df_validate