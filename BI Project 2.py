#!/usr/bin/env python
# coding: utf-8

# In[136]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
color = sns.color_palette()


# In[5]:


pwd


# In[12]:


data = pd.read_csv('Ecommerce - UK Retailer.csv',encoding= 'unicode_escape')
data.head(10)


# #  Data Cleaning

# In[15]:


data.isnull().sum()


# In[16]:


data.describe()


# In[17]:


data.info()


# In[18]:


data.shape


# 3. Remove duplicate rows

# In[19]:


data.drop_duplicates()


# 4. Remove rows which have negative values in Quantity column 
# 

# In[29]:


data_new = data[(data['Quantity'] >= 0)] # Removing '-ve' values from the Quantity column.
data_new


# Treating Outliers 

# In[27]:


plt.subplots(figsize=(12,10))
sns.boxplot(data_new.UnitPrice)

plt.xlabel('Quantity')
plt.title('Unit Price')
plt.grid()
plt.show()
# Verifying 'Outliers' , Found 1 Negative Value 


# In[30]:


fine_data = data_new[(data_new['UnitPrice'] >= 0)]
fine_data.head(2) # Price Can't Be in the '-ve'.


# In[31]:


fine_data.shape


# In[33]:


fine_data.isnull().sum()


# --  Check for missing values in all columns and replace them with the appropriate metric(Mean/Median/Mode) 
# 

# In[39]:


fine_data.Description.fillna(fine_data.Description.mode()[0],inplace = True)


# In[41]:


fine_data.isnull().sum() # Hence all the Missing values from Description are nill..


# In[49]:


fine_data.CustomerID.fillna(fine_data.CustomerID.median(),inplace = True)


# In[50]:


fine_data.isnull().sum() #Hence all the Missing values from CustomerID are nill..


# Add the columns - Month, Day and Hour for the invoice 

# In[62]:


fine_data['InvoiceDate'] = fine_data['InvoiceDate'].astype('datetime64[ns]')
fine_data['Year'] = fine_data.InvoiceDate.dt.year
fine_data['Month'] = fine_data.InvoiceDate.dt.month
fine_data['year_month']=fine_data.InvoiceDate.map(lambda x: 100*x.year +x.month)
fine_data['Day']=(fine_data.InvoiceDate.dt.dayofweek)+1 # +1 to make Monday=1.....until Sunday=7
fine_data['Hour'] = fine_data.InvoiceDate.dt.hour
fine_data['Revenue'] = fine_data['Quantity'] * fine_data['UnitPrice']
fine_data.head()


#   How many orders made by the customers? 
# 

# In[74]:


orders_cus = pd.Index(fine_data['Quantity'])
print(f"The Total Number of orders made by the Customers = {orders_cus.value_counts().sum()}")


#     TOP 5 customers with higher number of orders

# In[106]:


total_order = fine_data.groupby(by=['CustomerID','Country'],as_index = False)['InvoiceNo'].count()
total_order


# In[107]:


total_order.sort_values(by ='InvoiceNo',ascending = False).head()


# How much money spent by the customers? 

# In[116]:


money_spent = fine_data.groupby(by=['CustomerID','Country'],as_index = False)['Revenue'].sum()
money_spent


# 4. TOP 5 customers with highest money spent

# In[131]:


money_spent.sort_values(by='Revenue',ascending = False).head()


# 5. How many orders per month?

# In[143]:


graph = fine_data.groupby('InvoiceNo')['year_month'].unique().value_counts().sort_index().plot(kind='bar',color=color[0],figsize=(20,6))
graph.set_xlabel('Month',fontsize=15)
graph.set_ylabel('Number of Orders',fontsize=15)
graph.set_title('Number of orders for different Months (1st Dec 2010 - 9th Dec 2011)',fontsize=20)
graph.set_xticklabels(('Dec_10','Jan_11','Feb_11','Mar_11','Apr_11','May_11','Jun_11','July_11','Aug_11','Sep_11','Oct_11','Nov_11','Dec_11'), rotation='horizontal', fontsize=13)
plt.show()


# 6. How many orders per day?

# In[147]:


day_orders = fine_data.groupby(by = 'InvoiceNo')['Day'].unique().value_counts().sort_index().plot(kind = 'bar',color=color[0],figsize=(20,8))
day_orders.set_xlabel('Day',fontsize = 15)
day_orders.set_ylabel('Number of orders per day',fontsize = 15)
day_orders.set_title('Number of Orders per day',fontsize = 19)
day_orders.set_xticklabels(('Mon','Tue','Wed','Thurs','Friday','Sun'),rotation='horizontal',fontsize=15)
plt.show()


# 7. How many orders per hour?

# In[152]:


#order_hour = fine_data.groupby(by='InvoiceNo')['Hour'].unique().value_counts().sort_index().plot(kind='bar',color=color[0],figsize=(20,8))
order_hour = fine_data.groupby('InvoiceNo')['Hour'].unique().value_counts().iloc[:-1].sort_index().plot(kind='bar',color=color[0],figsize=(15,6))
order_hour.set_xlabel('Hour',fontsize=13)
order_hour.set_ylabel('Number of Orders',fontsize=13)
order_hour.set_title('Number of Hours',fontsize=13)
order_hour.set_xticklabels(range(6,21), rotation='horizontal', fontsize=13)
plt.show()


#     8. How many orders for each country?

# In[159]:


country_orders = fine_data.groupby(by = 'Country')['InvoiceNo'].count().sort_values()
del country_orders['United Kingdom']

plt.subplots(figsize=(20,10))
country_orders.plot(kind = 'barh',fontsize=16,color=color[0])
plt.xlabel('Number of orders',fontsize=14)
plt.ylabel('Country',fontsize=14)
plt.title('Number of Orders for different Countries',fontsize=14)
plt.show()


# In[171]:


country_orders = fine_data.groupby('Country')['InvoiceNo'].count().sort_values()
#del group_country_orders['United Kingdom']

# number of unique customers in each country (with UK)
plt.subplots(figsize=(15,8))
country_orders.plot(kind='barh', fontsize=14, color=color[0])
plt.xlabel('Number of Orders', fontsize=14)
plt.ylabel('Country', fontsize=14)
plt.title('Number of Orders for different Countries', fontsize=14)
plt.show()


# 10. How much money spent by each country?

# In[175]:


Money_spent = fine_data.groupby('Country')['Revenue'].sum().sort_values()
del Money_spent['United Kingdom']

plt.subplots(figsize=(20,8))
Money_spent.plot(kind='barh',fontsize=12,color=color[0])
plt.xlabel('Money Spent(Dollar)',fontsize = 14)
plt.ylabel('Country',fontsize=14)
plt.title('Money Spent by different Countries',fontsize=14)
plt.show()


# In[176]:


Money_spent = fine_data.groupby('Country')['Revenue'].sum().sort_values()
#del group_country_amount_spent['United Kingdom']

# plot total money spent by each country (without UK)
plt.subplots(figsize=(15,8))
Money_spent.plot(kind='barh', fontsize=12, color=color[0])
plt.xlabel('Money Spent (Dollar)', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.title('Money Spent by different Countries', fontsize=12)
plt.show()


# In[179]:


# Box Plot
plt.subplots(figsize=(10,8))
sns.boxplot(fine_data.UnitPrice)

plt.xlabel('Unit Price')
plt.ylabel('Unit Price')
plt.show()


# In[187]:


# Histogram for numerical Data Distribution
plt.hist(fine_data['Hour'],color='black',bins = int(100/2))
plt.xlabel('Hour')
plt.ylabel('Revenue USD($)')
plt.show()


# In[188]:


# Distribution Plot – All Numeric Variables
plt.subplots(figsize=(10,8))
sns.distplot(fine_data.Quantity[fine_data.Quantity < 50], label='Unit Price').legend()

plt.xlabel('Unit Price')
plt.ylabel('Distribution')
plt.title('Price Distribution')
plt.show()


# D. Aggregation for all numerical Columns 
# 

# In[189]:


fine_data.describe()


# E. Unique Values across all columns 

# In[190]:


pd.unique(fine_data[['Country','Description','StockCode','Country']].values.ravel())


# G. Correlation – Heatmap - All Numeric Variables

# In[191]:


# Heat Map
sns.heatmap(fine_data.corr())
plt.show()


# In[192]:


#Bar Plot 
result=fine_data.groupby('Month').sum()
month=range(1,13)
plt.bar(month,result['Revenue'])
plt.xticks(month)
plt.xlabel('month in number')
plt.ylabel('Revenue USD($)')
plt.show()


# J. Pair plot - All Numeric Variables 

# In[193]:


sns.pairplot(fine_data,vars=["Quantity","UnitPrice","Revenue","Month","Day"])
plt.show()


#     K.Line chart to show the trend of data

# In[196]:


plt.plot(fine_data['Day'],fine_data['Revenue'])
plt.xlabel('Day')
plt.ylabel('Revenue')
plt.show()


# In[198]:


# skewness 
fine_data.skew(axis=0,skipna=True)


# In[197]:


fine_data.skew(axis=1,skipna=True)

