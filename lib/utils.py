import os
import sys
import numpy as np
import pandas as pd
import openpyxl

def five_question_columns_cleaner(df):
    counter = 0
    for it,column in reversed(list(enumerate(df.columns))):
        if 'Unnamed' in column:
            counter += 1
        else:
            if counter != 0:
                df_temporal = df.iloc[:,it:int(counter+it+1)]
                try:
                    df_temporal_transformed = df_temporal.fillna('')
                    df_f = df_temporal_transformed.apply(lambda x: ''.join(x.dropna()), axis=1)
                except:
                    df_temporal_transformed = df_temporal.fillna(0)
                    df_f = df_temporal_transformed.apply(np.sum, axis=1)
                df = df.drop(df.columns[it+1:it+counter+1],axis=1)
                df[df.columns[it]] = df_f.values
                #print(df.columns[it:int(counter+it+1)])       
            counter = 0
    return df
def df_describe_missing(df):
    # first create missing indicator for features with missing data
    df_missing = df.copy()
    for col in df_missing.columns:
        missing = df_missing[col].isnull()
        num_missing = np.sum(missing)
        
        if num_missing > 0:  
            print('created missing indicator for: {}'.format(col))
            df_missing['{}_ismissing'.format(col)] = missing
    # then based on the indicator, plot the histogram of missing values
    ismissing_cols = [col for col in df_missing.columns if 'ismissing' in col]
    df_missing['num_missing'] = df_missing[ismissing_cols].sum(axis=1)
    print(df_missing['num_missing'].value_counts())
    df_missing['num_missing'].value_counts().reset_index().sort_values(by='index').plot.bar(x='index', y='num_missing')

    return df_missing