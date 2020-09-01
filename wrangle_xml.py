import pandas as pd

import xml.etree.ElementTree as etree

def build_df(df):
    df = pd.DataFrame()
    for i in range(4,137028):
        dict_new = root[i].attrib
        df = df.append(dict_new, ignore_index=True)
    return df    

def wrangle_xml():
    
   
    tree = etree.parse("export.xml")
    
    root = tree.getroot()
    
    df = build_df(df)
    
    return df