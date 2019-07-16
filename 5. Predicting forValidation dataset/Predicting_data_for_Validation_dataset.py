# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 20:37:31 2019

@author: AMAN
"""

import numpy as np 
import pandas as pd

validation_feature=pd.read_csv('Billing_Data_Validation_vf.csv')
Predicted_metric=pd.read_csv('Predicted_values_2015.csv')
Predicted_metric.columns
Predicted_metric.drop('Monthly SMA MTD % to Quota.1',axis=1,inplace=True)

store_metric_master.columns

## Rename columns
Predicted_metric.rename(columns={'Store_id':'Plant'},inplace=True)

# Date transform
Predicted_metric['FISCAL_YEAR_PERIOD']=Predicted_metric['Date'].apply(lambda x: pd.to_numeric(str(x)[-4:]+'0'+str(x)[-7:-5]))


# Merge with  metric
validation_feature=pd.merge(validation_feature,Predicted_metric,on=['Plant','FISCAL_YEAR_PERIOD'],how='left')

# Merge with foot traffic
store_foot=pd.read_csv('Store_footTraffic.csv')
validation_feature=pd.merge(validation_feature,store_foot,on=['Plant','FISCAL_YEAR_PERIOD'],how='left')

# Customer Merge
cust=pd.read_csv('Customer_ND.csv') #### Duplicates in Customer data removed in Excel
cust.drop('Unnamed: 0',axis=1,inplace=True)
validation_feature=pd.merge(validation_feature,cust,on=['Sold_To_Party'],how='left')
validation_feature.fillna('Missing',inplace=True)

## Store characteristics merge
store_character=pd.read_csv('Store_charateristics_vf.csv')
store_character.columns
store_character.drop('Store Zip',axis=1,inplace=True)
store_character.drop('Opening Date',axis=1,inplace=True)
validation_feature=pd.merge(validation_feature,store_character,on=['Plant'],how='left')
validation_feature.fillna('Missing',inplace=True)

########### Creating dummy variables for categorical data

validation_feature.columns

# Sale Category
validation_feature['Category'].value_counts(dropna=False)
pd.get_dummies(validation_feature['Category'],prefix='Sale_Category')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Category'],prefix='Sale_Category')],axis=1)

# Customer Cluster
validation_feature['Cluster'].value_counts(dropna=False)
pd.get_dummies(validation_feature['Cluster'],prefix='Cust_Cluster')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Cluster'],prefix='Cust_Cluster')],axis=1)

# Customer Premier_Deal
validation_feature['Premier_Dealer__c'].value_counts(dropna=False)
pd.get_dummies(validation_feature['Premier_Dealer__c'],prefix='Cust_Premier_Deal')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Premier_Dealer__c'],prefix='Cust_Premier_Deal')],axis=1)

# Customer Market_Package
validation_feature['Marketing Package'].value_counts(dropna=False)
pd.get_dummies(validation_feature['Marketing Package'],prefix='Cust_Market_Package')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Marketing Package'],prefix='Cust_Market_Package')],axis=1)

# Store Trade Area Size
validation_feature['Trade_Area_Size']=validation_feature['Trade Area Size '].apply(lambda x: "Small Market" if x=="Small Market" or x=="small Market" else x)
validation_feature['Trade_Area_Size'].value_counts(dropna=False) 
pd.get_dummies(validation_feature['Trade_Area_Size'],prefix='Store_TAS')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Trade_Area_Size'],prefix='Store_TAS')],axis=1)

# Store Size
validation_feature['Store Size'].value_counts(dropna=False) 
pd.get_dummies(validation_feature['Store Size'],prefix='Store_Size')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Store Size'],prefix='Store_Size')],axis=1)

# Store Type
validation_feature['Store Type'].value_counts(dropna=False) 
pd.get_dummies(validation_feature['Store Type'],prefix='Store_Type')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Store Type'],prefix='Store_Type')],axis=1)

# Does Store Have a Fleet Delivery Truck?
pd.get_dummies(validation_feature['Does Store Have a Fleet Delivery Truck?'],prefix='Fleet')
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Does Store Have a Fleet Delivery Truck?'],prefix='Fleet')],axis=1)

# Month
validation_feature['FISCAL_YEAR_PERIOD'].apply(lambda x: pd.to_numeric(str(x)[-2:]))
validation_feature['Sale_Month']=validation_feature['FISCAL_YEAR_PERIOD'].apply(lambda x: str(x)[-2:])
validation_feature['Sale_Month'].replace(['01','02','03','04','05','06','07','08','09','10','11','12'],
                 ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                 ,inplace=True)
validation_feature=pd.concat([validation_feature,pd.get_dummies(validation_feature['Sale_Month'],prefix='Sale_Month')],axis=1)


validation_feature.columns

'Cust_Cluster_Missing','Cust_Premier_Deal_Missing','Cust_Market_Package_Missing','Store_TAS_Missing',
'Store_Size_Missing', 'Store_Type_Missing','Fleet_Missing',

validation_feature['Cust_Cluster_Missing']=np.nan
validation_feature['Cust_Premier_Deal_Missing']=np.nan
validation_feature['Cust_Market_Package_Missing']=np.nan
validation_feature['Store_TAS_Missing']=np.nan
validation_feature['Store_Size_Missing']=np.nan
validation_feature['Store_Type_Missing']=np.nan
validation_feature['Fleet_Missing']=np.nan





validation_feature.fillna(0,inplace=True)

validation_feature.to_csv('Validation_2015.csv')
x_val=validation_feature.copy()
y_val_true=x_val.pop('Sales')

x_val['Sale_Category_Solar']=np.nan
x_val['Sale_Category_VRF Controls']=np.nan
x_val['Sale_Category_VRF Indoor']=np.nan
x_val['Sale_Category_VRF Outdoor']=np.nan
x_val['Sale_Month_Aug']=np.nan
x_val['Sale_Month_Dec']=np.nan
x_val['Sale_Month_Jul']=np.nan
x_val['Sale_Month_Nov']=np.nan
x_val['Sale_Month_Oct']=np.nan
x_val['Sale_Month_Sep']=np.nan
x_val.fillna(0,inplace=True)




x_val1=x_val[['Monthly Avg Tkt YoY Growth',
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


y_val_predict=model1.predict(x_val1)
validation=pd.concat([x_val,y_val_true,pd.Series(y_val_predict)],axis=1)
validation.columns
validation=validation[['Plant','Sold_To_Party',
                            'FISCAL_YEAR_PERIOD',
                                      'Category','Sales',
                                               0]]

validation.rename(columns={0:'Prediction'},inplace=True)
validation.to_csv('Billing_Data_Validation_Predictions.csv')

#'Monthly WC MTD % to Quota',