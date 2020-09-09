import pandas as pd
import numpy as np
import datetime

import os.path

import xml.etree.ElementTree as etree

def build_df():
    df = pd.DataFrame()
    for i in range(4,137028):
        dict_new = root[i].attrib
        df = df.append(dict_new, ignore_index=True)
    return df    

def wrangle_xml():
    
    if os.path.isfile('./xml.csv'):
        df = pd.read_csv('xml.csv')
    
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