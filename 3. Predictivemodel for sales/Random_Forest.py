# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 21:37:32 2019

@author: AMAN
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score

Bill_Train=pd.read_csv('Train_2013_2014_WD.csv')
Bill_copy=Bill_Train.copy()
Bill_copy.columns


y=Bill_copy.pop('Sales')
y[y!=0]
x=Bill_copy[['Monthly Avg Tkt YoY Growth',
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

model1=RandomForestRegressor(n_estimators=200,
                             oob_score=True,
                             n_jobs=-1,
                             random_state=50,
                             max_features="auto",
                             min_samples_leaf=50)

model1.fit(x,y)

model1.score(x,y)

r2_score(y,model1.oob_prediction_)

explained_variance_score(y,model1.oob_prediction_)

feature=pd.Series(model1.feature_importances_,index=x.columns)

feature.sort_values(ascending=False,inplace=True)

feature.plot(kind='barh')
