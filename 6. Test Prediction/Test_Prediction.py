# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 21:45:34 2019

@author: AMAN
"""

import numpy as np 
import pandas as pd

test_feature=pd.read_csv('Billing_Data_Test_vf.csv')
Predicted_metric=pd.read_csv('Predicted_values_2015.csv')
Predicted_metric.columns
Predicted_metric.drop('Monthly SMA MTD % to Quota.1',axis=1,inplace=True)

store_metric_master.columns

## Rename columns
Predicted_metric.rename(columns={'Store_id':'Plant'},inplace=True)

# Date transform
Predicted_metric['FISCAL_YEAR_PERIOD']=Predicted_metric['Date'].apply(lambda x: pd.to_numeric(str(x)[-4:]+'0'+str(x)[-7:-5]))


# Merge with  metric
test_feature=pd.merge(test_feature,Predicted_metric,on=['Plant','FISCAL_YEAR_PERIOD'],how='left')

# Merge with foot traffic
store_foot=pd.read_csv('Store_footTraffic.csv')
test_feature=pd.merge(test_feature,store_foot,on=['Plant','FISCAL_YEAR_PERIOD'],how='left')

# Customer Merge
cust=pd.read_csv('Customer_ND.csv') #### Duplicates in Customer data removed in Excel
cust.drop('Unnamed: 0',axis=1,inplace=True)
test_feature=pd.merge(test_feature,cust,on=['Sold_To_Party'],how='left')
test_feature.fillna('Missing',inplace=True)

## Store characteristics merge
store_character=pd.read_csv('Store_charateristics_vf.csv')
store_character.columns
store_character.drop('Store Zip',axis=1,inplace=True)
store_character.drop('Opening Date',axis=1,inplace=True)
test_feature=pd.merge(test_feature,store_character,on=['Plant'],how='left')
test_feature.fillna('Missing',inplace=True)

########### Creating dummy variables for categorical data

test_feature.columns

# Sale Category
test_feature['Category'].value_counts(dropna=False)
pd.get_dummies(test_feature['Category'],prefix='Sale_Category')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Category'],prefix='Sale_Category')],axis=1)

# Customer Cluster
test_feature['Cluster'].value_counts(dropna=False)
pd.get_dummies(test_feature['Cluster'],prefix='Cust_Cluster')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Cluster'],prefix='Cust_Cluster')],axis=1)

# Customer Premier_Deal
test_feature['Premier_Dealer__c'].value_counts(dropna=False)
pd.get_dummies(test_feature['Premier_Dealer__c'],prefix='Cust_Premier_Deal')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Premier_Dealer__c'],prefix='Cust_Premier_Deal')],axis=1)

# Customer Market_Package
test_feature['Marketing Package'].value_counts(dropna=False)
pd.get_dummies(test_feature['Marketing Package'],prefix='Cust_Market_Package')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Marketing Package'],prefix='Cust_Market_Package')],axis=1)

# Store Trade Area Size
test_feature['Trade_Area_Size']=test_feature['Trade Area Size '].apply(lambda x: "Small Market" if x=="Small Market" or x=="small Market" else x)
test_feature['Trade_Area_Size'].value_counts(dropna=False) 
pd.get_dummies(test_feature['Trade_Area_Size'],prefix='Store_TAS')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Trade_Area_Size'],prefix='Store_TAS')],axis=1)

# Store Size
test_feature['Store Size'].value_counts(dropna=False) 
pd.get_dummies(test_feature['Store Size'],prefix='Store_Size')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Store Size'],prefix='Store_Size')],axis=1)

# Store Type
test_feature['Store Type'].value_counts(dropna=False) 
pd.get_dummies(test_feature['Store Type'],prefix='Store_Type')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Store Type'],prefix='Store_Type')],axis=1)

# Does Store Have a Fleet Delivery Truck?
pd.get_dummies(test_feature['Does Store Have a Fleet Delivery Truck?'],prefix='Fleet')
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Does Store Have a Fleet Delivery Truck?'],prefix='Fleet')],axis=1)

# Month
test_feature['FISCAL_YEAR_PERIOD'].apply(lambda x: pd.to_numeric(str(x)[-2:]))
test_feature['Sale_Month']=test_feature['FISCAL_YEAR_PERIOD'].apply(lambda x: str(x)[-2:])
test_feature['Sale_Month'].replace(['01','02','03','04','05','06','07','08','09','10','11','12'],
                 ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                 ,inplace=True)
test_feature=pd.concat([test_feature,pd.get_dummies(test_feature['Sale_Month'],prefix='Sale_Month')],axis=1)


test_feature.columns
x_test=test_feature.copy()
y_test_true=x_test.pop('Sales')

x_test1=x_test[['Monthly Avg Tkt YoY Growth',
       'Monthly Mktg Adopt', 'Monthly Parts & Supplies MTD % to Quota',
       'Monthly Phonecalls', 'Monthly SMA MTD % to Quota',
       'Monthly Store Account MTD % to Quota', 'Monthly VOC',
       'Foottraffic', 'Sale_Category_#',
       'Sale_Category_Building Automation',
       "Sale_Category_Com'l Unit Controls", 'Sale_Category_Controls',
       'Sale_Category_Heating Products', 'Sale_Category_IAQ',
       'Sale_Category_Mini-Split Controls', 'Sale_Category_Mini-Splits',
       'Sale_Category_Other', 'Sale_Category_Package Rooftops',
       'Sale_Category_Parts & Supplies', 'Sale_Category_Res Cooling',
       'Sale_Category_Res Heating', 'Sale_Category_Solar',
       'Sale_Category_Splits', 'Sale_Category_Unit Controls',
       'Sale_Category_VRF Accessories', 'Sale_Category_VRF Controls',
       'Sale_Category_VRF Indoor', 'Sale_Category_VRF Outdoor',
       'Cust_Cluster_Key', 'Cust_Cluster_Missing', 'Cust_Cluster_Priority',
       'Cust_Cluster_Standard', 'Cust_Premier_Deal_Missing',
       'Cust_Premier_Deal_No', 'Cust_Premier_Deal_Yes',
       'Cust_Market_Package_Best', 'Cust_Market_Package_Better',
       'Cust_Market_Package_Good', 'Cust_Market_Package_Missing',
       'Cust_Market_Package_None','Store_TAS_Large Market',
       'Store_TAS_Medium Market', 'Store_TAS_Missing',
       'Store_TAS_Small Market', 'Store_Size_Group 1 < $2.75M',
       'Store_Size_Group 2 > $2.75M', 'Store_Size_Group 3 > $10M',
       'Store_Size_Missing', 'Store_Type_Missing', 'Store_Type_New',
       'Store_Type_Relocation', 'Store_Type_Remodel', 'Fleet_Missing',
       'Fleet_N', 'Fleet_Y','Sale_Month_Apr', 'Sale_Month_Aug',
       'Sale_Month_Dec', 'Sale_Month_Feb', 'Sale_Month_Jan', 'Sale_Month_Jul',
       'Sale_Month_Jun', 'Sale_Month_Mar', 'Sale_Month_May', 'Sale_Month_Nov',
       'Sale_Month_Oct', 'Sale_Month_Sep']]

#'Sale_Category_Solar' 'Sale_Category_VRF Controls'\n
# 'Sale_Category_VRF Indoor' 'Sale_Category_VRF Outdoor'\n 
# 'Cust_Cluster_Missing' 'Cust_Premier_Deal_Missing'\n 
# 'Cust_Market_Package_Missing' 'Store_Size_Missing' 'Fleet_Missing'\n
# 'Sale_Month_Apr' 'Sale_Month_Feb' 'Sale_Month_Jan' 'Sale_Month_Jun'\n
# 'Sale_Month_Mar' 'Sale_Month_May'
 
x_test['Sale_Category_Solar']=np.nan 
x_test['Sale_Category_VRF Controls']=np.nan
x_test['Sale_Category_VRF Indoor']=np.nan
x_test['Sale_Category_VRF Outdoor']=np.nan
x_test['Cust_Cluster_Missing']=np.nan
x_test['Cust_Premier_Deal_Missing']=np.nan
x_test['Cust_Market_Package_Missing']=np.nan
x_test['Store_Size_Missing']=np.nan
x_test['Fleet_Missing']=np.nan
x_test['Sale_Month_Apr']=np.nan
x_test['Sale_Month_Feb']=np.nan
x_test['Sale_Month_Jan']=np.nan
x_test['Sale_Month_Jun']=np.nan
x_test['Sale_Month_Mar']=np.nan
x_test['Sale_Month_May']=np.nan
x_test.fillna(0,inplace=True)

x_test1=x_test[['Monthly Avg Tkt YoY Growth',
       'Monthly Mktg Adopt', 'Monthly Parts & Supplies MTD % to Quota',
       'Monthly Phonecalls', 'Monthly SMA MTD % to Quota',
       'Monthly Store Account MTD % to Quota', 'Monthly VOC',
       'Foottraffic', 'Sale_Category_#',
       'Sale_Category_Building Automation',
       "Sale_Category_Com'l Unit Controls", 'Sale_Category_Controls',
       'Sale_Category_Heating Products', 'Sale_Category_IAQ',
       'Sale_Category_Mini-Split Controls', 'Sale_Category_Mini-Splits',
       'Sale_Category_Other', 'Sale_Category_Package Rooftops',
       'Sale_Category_Parts & Supplies', 'Sale_Category_Res Cooling',
       'Sale_Category_Res Heating', 'Sale_Category_Solar',
       'Sale_Category_Splits', 'Sale_Category_Unit Controls',
       'Sale_Category_VRF Accessories', 'Sale_Category_VRF Controls',
       'Sale_Category_VRF Indoor', 'Sale_Category_VRF Outdoor',
       'Cust_Cluster_Key', 'Cust_Cluster_Missing', 'Cust_Cluster_Priority',
       'Cust_Cluster_Standard', 'Cust_Premier_Deal_Missing',
       'Cust_Premier_Deal_No', 'Cust_Premier_Deal_Yes',
       'Cust_Market_Package_Best', 'Cust_Market_Package_Better',
       'Cust_Market_Package_Good', 'Cust_Market_Package_Missing',
       'Cust_Market_Package_None','Store_TAS_Large Market',
       'Store_TAS_Medium Market', 'Store_TAS_Missing',
       'Store_TAS_Small Market', 'Store_Size_Group 1 < $2.75M',
       'Store_Size_Group 2 > $2.75M', 'Store_Size_Group 3 > $10M',
       'Store_Size_Missing', 'Store_Type_Missing', 'Store_Type_New',
       'Store_Type_Relocation', 'Store_Type_Remodel', 'Fleet_Missing',
       'Fleet_N', 'Fleet_Y','Sale_Month_Apr', 'Sale_Month_Aug',
       'Sale_Month_Dec', 'Sale_Month_Feb', 'Sale_Month_Jan', 'Sale_Month_Jul',
       'Sale_Month_Jun', 'Sale_Month_Mar', 'Sale_Month_May', 'Sale_Month_Nov',
       'Sale_Month_Oct', 'Sale_Month_Sep']]

y_test_predict=model1.predict(x_test1)
test=pd.concat([x_test,pd.Series(y_test_predict)],axis=1)
test.columns
test=test[['Plant','Sold_To_Party',
                            'FISCAL_YEAR_PERIOD',
                                      'Category',
                                               0]]

test.rename(columns={0:'Sale_Prediction'},inplace=True)
test.to_csv('Billing_Data_Test_Predictions.csv')
