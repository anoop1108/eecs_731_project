
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:41:56 2020

@author: gracemcmonagle
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans

filepath = '/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/data/owid-covid-data.csv'
rawData = pd.read_csv(filepath, delimiter = ',')
rawData_nan0 = rawData.fillna(0)

filepath2 = '/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/data/OxCGRT_latest.csv'
df = pd.read_csv(filepath2, delimiter = ',')

filepath3 ='/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/data/coronanet_release_allvars.csv'
policies = pd.read_csv(filepath3, delimiter = ',')


#%% calculate average new number of cases in each country
countries = rawData.iso_code.unique()
avgCaseGrowth = {}
for country in countries:
    is_country = rawData['iso_code'] == country
    avgCG = rawData[is_country].new_cases_per_million.mean()
    avgCaseGrowth[country] = avgCG


caseGrowth = pd.DataFrame.from_dict(avgCaseGrowth, orient='index').rename(columns={0:'caseGrowth'})
caseGrowth.to_csv('/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/src/caseGrowth.csv',index=True)
#could add population
#%% Calculate avg stringency index for each country
avgStringIndex = {}
for country in countries:
    is_country = df['CountryCode'] == country
    avgSI = df[is_country].StringencyIndex.mean()
    avgStringIndex[country] = avgSI
    
stringIndex = pd.DataFrame.from_dict(avgStringIndex, orient='index').rename(columns={0:'stringIndex'})
stringIndex.to_csv('/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/src/avgStringIndex.csv',index=True)
#%% calculate #days into pandemic schools closed
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
c1_flag = df['C1_Flag'] == 1
scClosing = df[c1_flag]

daysBefSClose = {}
for country in countries:
    is_country = scClosing['CountryCode'] == country
    if len(scClosing[is_country]) == 0:
        days = float('NaN')
    else:
        days = (scClosing[is_country]['Date'].iloc[0] - datetime.strptime('01012020', '%m%d%Y')).days
    daysBefSClose[country] = days
    
daysSClose = pd.DataFrame.from_dict(daysBefSClose, orient = 'index').rename(columns = {0: 'DaysBeforeSClose'})

#%% number of policies by country
policyCount = {}
for country in countries:
    is_country = policies['ISO_A3'] == country
    count = len(policies[is_country].record_id.unique())
    policyCount[country] = count
    
policyCountdf = pd.DataFrame.from_dict(policyCount, orient = 'index').rename(columns = {0 : 'PolicyCount'})
policyCountdf.to_csv('/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/src/policyCounts.csv',index=True)
#%% 
full = pd.concat([caseGrowth, stringIndex, daysSClose], axis = 1).dropna()
ax1 = full.plot.scatter(x='stringIndex',
                      y='caseGrowth',
                      c='DarkBlue')

ax2 = full.plot.scatter(x='DaysBeforeSClose',
                      y='caseGrowth',
                      c='DarkBlue')


#%%
clt = AgglomerativeClustering(linkage = 'complete', affinity = 'euclidean', n_clusters = 5)
model = clt.fit(full)
labels = list(model.labels_)
#full['Country'] = full.index
country_with_cluster = full
country_with_cluster['cluster'] = labels

country_with_cluster.to_csv('/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/src/clusterAgg.csv',index=True)

#%%
clt2 = KMeans(n_clusters=5, random_state = 42)
model2 = clt2.fit(full)
labels2 = list(model2.labels_)
country_with_cluster2 = full
country_with_cluster2['cluster'] = labels2

country_with_cluster2.to_csv('/Users/gracemcmonagle/Desktop/School/Fall 2020/EECS 731/Group Project/src/clusterKMeans.csv',index=True)
