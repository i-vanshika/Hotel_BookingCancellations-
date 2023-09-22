#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[1]:


import pandas as pd 

import matplotlib.pyplot as plt 
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the Dataset

# In[2]:


df=pd.read_csv('hotel_booking.csv')


# # EDA and Data Cleaning

# In[3]:


df.head()


# In[4]:


df.tail()


# In[5]:


df.shape


# In[6]:


df.drop(['name','email','credit_card','phone-number'],axis=1,inplace=True) 


# In[7]:


df.head(10)


# In[8]:


df.shape

# we have removed all the personal detail of a customer because a hotel would never provide the personal details of a customer


# In[9]:


df.columns


# In[10]:


df.dtypes


# In[11]:


df.info()


#  We have to perform our analysis on reservation_status_date. Since it is present in object form so we will convert it into date and time .

# In[12]:


df['reservation_status_date']=pd.to_datetime(df['reservation_status_date'])  

# by using datetime function we will convert it into required format and save it into same column.


# In[13]:


df.info()

Object datatypes are nothing but categoriacal columns
# In[14]:


df.describe(include='object')  

# describe function is only for numerical values but by using the keyword include='object' we will get the summary statistics
# of all the object columns.


# In[15]:


for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# ## Checking Missing Values

# In[16]:


df.isnull().sum()  # this function returns the number of missing values in the dataset.

We can simply remove the the columns agent and company because they have too many missing values and difficult to handle. We will drop the missing values of country.
# In[17]:


df.drop(['company','agent'], axis=1, inplace=True)


# In[18]:


df.dropna(inplace=True)


# In[19]:


df.isnull().sum()

So,now all the missing values have been removed from the columns
# In[20]:


df.describe()  # returns the summary characteristics of the numerical columns

Try removing all the outliers for example the range of adr is (-6.38 to 5400) and in case of babies, ranges from ( 0 to 10) which is again an outlier. In this project we c=have assumed that there are no outliers.
# In[21]:


df['adr'].plot(kind='box')

As we can see all the values of adr(average daily rate) are all below 1000 and only one is above 5000. This is a very large oulier which needs to be removed, while rest are somewhat considerable.
# In[22]:


df= df[df['adr']<5000]


# In[23]:


df.describe()

Now , the maximum value of adr is 510. Hence, otlier has been removed
# # Data Analysis and Visualisations

# In[24]:


df['is_canceled'].value_counts()


# In[25]:


# calculating the percentage

canceled_percentage= df['is_canceled'].value_counts(normalize = True)
print(canceled_percentage)


# 62% reservations are not cancelled and 37% reservations are cancelled. Cancellation rate is much higher.

# In[65]:


plt.figure(figsize=(5,4))
plt.title('Reservaton Status Count')
plt.bar(['Not cancelled','Cancelled'],df['is_canceled'].value_counts(), edgecolor='k', width=0.7)
plt.show()

Cancelled count is more than half which is a major issue 
# In[64]:


plt.figure(figsize=(8,4))
ax1=sns.countplot(x='hotel', hue='is_canceled', data=df, palette='BuPu')
plt.title('Reservation in different hotels', size=20)
plt.xlabel('hotel')
plt.ylabel('No. of reservations')
plt.show()


# In[28]:


resort_hotel= df[df['hotel']=='Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)


# In[29]:


city_hotel= df[df['hotel']=='City Hotel']
city_hotel['is_canceled'].value_counts(normalize=True)


# In[30]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[32]:


plt.figure(figsize=(20,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize=30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label= 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label= 'City Hotel')
plt.legend(fontsize =20)
plt.show()

So, we can infer that the cancellation in resort hotels might be due to the high prices. Spikes indicate the high prices of resort hotel and city hotel during weekends. Price of city hotel is comapretivey less when compared to resort hotels for so,e days.
# In[61]:


# creating a column named month so that we can see during which month cancellation rate is higher.

df['month']= df['reservation_status_date'].dt.month   # returns months according to the dates of reservation
plt.figure(figsize=(13,5))
ax1=sns.countplot(x='month', hue='is_canceled', data=df, palette= 'summer_r')
plt.title('Reservation status per month', size=20)
plt.ylabel('number of reservations')
plt.show()

Cancellations are highest in the month of January and lowest in August and September
# In[47]:


plt.figure(figsize=(10,5))
plt.title('ADR per month', fontsize=20)
sns.barplot('month','adr',data=df[df['is_canceled']==1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# It proves that high prices is directly proportional to the high cancellation rates in hotels.

# In[48]:


cancelled_data = df[df['is_canceled']==1 ]
top_10_country= cancelled_data['country'].value_counts()[:10]


# In[53]:


plt.figure(figsize=(7,7))
plt.title('Top 10 Countries with Cancelled Reservations')
plt.pie(top_10_country, autopct = '%.2f',labels= top_10_country.index)
plt.show()


# Highest number of cancellations are in Portugal when compared to other countries.

# In[54]:


df['market_segment'].value_counts()


# In[55]:


# percentage
df['market_segment'].value_counts(normalize= True)


# In[56]:


cancelled_data['market_segment'].value_counts(normalize= True)


# Since majority of the reservations are taking place through online mode, so majority of the cancellations are also from the online mode.

# In[ ]:




