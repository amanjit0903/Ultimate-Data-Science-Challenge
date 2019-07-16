# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 23:58:28 2019

@author: AMAN
"""

import numpy as np 
import pandas as pd

# Store Metrics 2013 & 2014 import and merge 
store_metric_2013=pd.read_csv('Store_metric_2013.csv')
store_metric_2013.rename(columns={'Store_ID':'Plant'},inplace=True)
store_metric_2013.rename(columns={'TS_ID':'FISCAL_YEAR_PERIOD'},inplace=True)
store_metric_2013['FISCAL_YEAR_PERIOD'].replace([1,2,3,4,5,6,7,8,9,10,11,12],
                 [2013001,2013002,2013003,2013004,2013005,2013006,2013007,2013008,2013009,2013010,2013011,2013012]
                 ,inplace=True)

store_metric_2014=pd.read_csv('Store_metric_2014.csv')
store_metric_2014.rename(columns={'Store_ID':'Plant'},inplace=True)
store_metric_2014.rename(columns={'TS_ID':'FISCAL_YEAR_PERIOD'},inplace=True)
store_metric_2014['FISCAL_YEAR_PERIOD'].replace([1,2,3,4,5,6,7,8,9,10,11,12],
                 [2014001,2014002,2014003,2014004,2014005,2014006,2014007,2014008,2014009,2014010,2014011,2014012]
                 ,inplace=True)

store_metric_master=pd.concat([store_metric_2013,store_metric_2014])
store_metric_master.fillna(0,inplace=True) ## Replacing nulls with zeros

## Billing Train import and merge 
Bill_Train=pd.read_csv('Billing_Data_Train_vf.csv')
Bill_Train=pd.merge(Bill_Train,store_metric_master,on=['Plant','FISCAL_YEAR_PERIOD'],how='left')

## Customer import and merge
cust=pd.read_csv('Customer_ND.csv') #### Duplicates in Customer data removed in Excel
cust.drop('Unnamed: 0',axis=1,inplace=True)
Bill_Train=pd.merge(Bill_Train,cust,on=['Sold_To_Party'],how='left')
Bill_Train.fillna('Missing',inplace=True)

## Store Characteristics import and merge
store_character=pd.read_csv('Store_charateristics_vf.csv')
store_character.columns
store_character.drop('Store Zip',axis=1,inplace=True)
store_character.drop('Opening Date',axis=1,inplace=True)
Bill_Train=pd.merge(Bill_Train,store_character,on=['Plant'],how='left')
Bill_Train.fillna('Missing',inplace=True)

## Store Foot Traffic import and merge
store_foot=pd.read_csv('Store_footTraffic.csv')
Bill_Train=pd.merge(Bill_Train,store_foot,on=['Plant','FISCAL_YEAR_PERIOD'],how='left')
Bill_Train.columns
Bill_Train['Foottraffic'].value_counts(dropna=False)

Bill_Train.to_csv('Train_2013_2014.csv')


########### Creating dummy variables for categorical data

Bill_Train.columns

# Sale Category
Bill_Train['Category'].value_counts(dropna=False)
pd.get_dummies(Bill_Train['Category'],prefix='Sale_Category')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Category'],prefix='Sale_Category')],axis=1)

# Customer Cluster
Bill_Train['Cluster'].value_counts(dropna=False)
pd.get_dummies(Bill_Train['Cluster'],prefix='Cust_Cluster')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Cluster'],prefix='Cust_Cluster')],axis=1)

# Customer Premier_Deal
Bill_Train['Premier_Dealer__c'].value_counts(dropna=False)
pd.get_dummies(Bill_Train['Premier_Dealer__c'],prefix='Cust_Premier_Deal')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Premier_Dealer__c'],prefix='Cust_Premier_Deal')],axis=1)

# Customer Market_Package
Bill_Train['Marketing Package'].value_counts(dropna=False)
pd.get_dummies(Bill_Train['Marketing Package'],prefix='Cust_Market_Package')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Marketing Package'],prefix='Cust_Market_Package')],axis=1)

# Store Trade Area Size
Bill_Train['Trade_Area_Size'].value_counts(dropna=False) 
Bill_Train['Trade_Area_Size']=Bill_Train['Trade Area Size '].apply(lambda x: "Small Market" if x=="Small Market" or x=="small Market" else x)
pd.get_dummies(Bill_Train['Trade_Area_Size'],prefix='Store_TAS')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Trade_Area_Size'],prefix='Store_TAS')],axis=1)

# Store Size
Bill_Train['Store Size'].value_counts(dropna=False) 
pd.get_dummies(Bill_Train['Store Size'],prefix='Store_Size')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Store Size'],prefix='Store_Size')],axis=1)

# Store Type
Bill_Train['Store Type'].value_counts(dropna=False) 
pd.get_dummies(Bill_Train['Store Type'],prefix='Store_Type')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Store Type'],prefix='Store_Type')],axis=1)

# Does Store Have a Fleet Delivery Truck?
pd.get_dummies(Bill_Train['Does Store Have a Fleet Delivery Truck?'],prefix='Fleet')
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Does Store Have a Fleet Delivery Truck?'],prefix='Fleet')],axis=1)

# Month
Bill_Train['FISCAL_YEAR_PERIOD'].apply(lambda x: pd.to_numeric(str(x)[-2:]))
Bill_Train['Sale_Month']=Bill_Train['FISCAL_YEAR_PERIOD'].apply(lambda x: str(x)[-2:])
Bill_Train['Sale_Month'].replace(['01','02','03','04','05','06','07','08','09','10','11','12'],
                 ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                 ,inplace=True)
Bill_Train=pd.concat([Bill_Train,pd.get_dummies(Bill_Train['Sale_Month'],prefix='Sale_Month')],axis=1)

# Export Files
Bill_Train.to_csv('Train_2013_2014_WD.csv')
