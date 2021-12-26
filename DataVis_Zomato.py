#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing libraries and packages
import numpy as num
import pandas as pds
import matplotlib.pyplot as mpl
import seaborn as sbn


# In[2]:


#DATASET
#loading the dataset
zom_og=pds.read_csv("zomato.csv")
zom_og.head() 


# In[3]:


#summary of the data 
zom_og.info() 


# In[4]:


#DATA CLEANING
#deleting unwanted columns such as dishliked,url,phone
zom_new=zom_og.drop(['url','dish_liked','phone'],axis=1)

#removing the duplicate values
zom_new.duplicated().sum()
zom_new.drop_duplicates(inplace=True)

#removing the nan and null values from our data
zom_new.isnull().sum()
zom_new.dropna(how='any',inplace=True)
zom_new.info() 


# In[5]:


#checking the columns left
zom_new.columns


# In[6]:


#changing the column names
zom_new = zom_new.rename(columns={'approx_cost(for two people)':'cost','listed_in(type)':'type',
                                  'listed_in(city)':'city'})
zom_new.columns


# In[7]:


#changing the datatype for cost
zom_new['cost'] = zom_new['cost'].astype(str) #Changing the cost to string
zom_new['cost'] = zom_new['cost'].apply(lambda x: x.replace(',','.')) #Using lambda function to replace ',' from cost
zom_new['cost'] = zom_new['cost'].astype(float) # Changing the cost to Float
zom_new.info()


# In[8]:


#displaying and checking the rate column of data
zom_new['rate'].unique()


# In[9]:


#removing '/5' from rates
zom_new = zom_new.loc[zom_new.rate !='NEW']
zom_new = zom_new.loc[zom_new.rate !='-'].reset_index(drop=True)
remove_slash = lambda x: x.replace('/5', '') if type(x) == num.str else x
zom_new.rate = zom_new.rate.apply(remove_slash).str.strip().astype('float')
zom_new['rate'].head()


# In[10]:


# Adjusting the column names
zom_new.name = zom_new.name.apply(lambda x:x.title())
zom_new.online_order.replace(('Yes','No'),(True, False),inplace=True)
zom_new.book_table.replace(('Yes','No'),(True, False),inplace=True)
zom_new.cost.unique()


# In[11]:


#Encoding the input Variables
def Encode(zom_new):
    for column in zom_new.columns[~zom_new.columns.isin(['rate', 'cost', 'votes'])]:
        zom_new[column] = zom_new[column].factorize()[0]
    return zom_new

zom_en = Encode(zom_new.copy())


# In[12]:


#correlation matrix for variables
corr = zom_en.corr(method='kendall')
mpl.figure(figsize=(12,8))
sbn.heatmap(corr, annot=True)
mpl.title('Correlation matrix',fontsize=18)
mpl.savefig("correlation.png")
zom_en.columns


# In[14]:


#Data visualization part
fig = mpl.figure(figsize=(20,8))
loc = sbn.countplot(x="location",data=zom_og, palette = "Set1")
loc.set_xticklabels(loc.get_xticklabels(), rotation=90, ha="right")
mpl.ylabel("Frequency",size=12)
mpl.xlabel("Location",size=12)
mpl.title('No. of restaurants in a Location',fontsize = 18,pad=20)
mpl.savefig("No. of restaurants in a Location.png")


# In[15]:


fig = mpl.figure(figsize=(12,8))
rest = sbn.countplot(x="rest_type",data=zom_og, palette = "Set1")
rest.set_xticklabels(rest.get_xticklabels(), rotation=90, ha="right")
mpl.ylabel("Frequency",size=12)
mpl.xlabel("Restaurant type",size=12)
mpl.title('Type of restaurant',fontsize = 18 ,pad=20)
mpl.savefig('Type of restaurant.png')


# In[16]:


mpl.figure(figsize=(12,8))
chains=zom_og['name'].value_counts()[:20]
sbn.barplot(x=chains,y=chains.index,palette='Set1')
mpl.title("Famous restaurant chains in Bangalore",fontsize=18,pad=20)
mpl.xlabel("No. of Outlets",size=12)
mpl.savefig('Famous restaurant chains in Bangalore.png')


# In[17]:


sbn.countplot(zom_new['online_order'])
fig = mpl.gcf()
fig.set_size_inches(12,12)
mpl.title('onlinedelivery or not',fontsize=18)
mpl.savefig("online.png")


# In[18]:


sbn.countplot(zom_new['book_table'])
fig = mpl.gcf()
fig.set_size_inches(12,12)
mpl.savefig("Book_Table.png")
mpl.title('Booking Table in a Restaurant (allowed or not)',fontsize=18)


# In[19]:


mpl.rcParams['figure.figsize'] = (12, 9)
Y = pds.crosstab(zom_new['rate'], zom_new['book_table'])
Y.div(Y.sum(1).astype(float), axis = 0).plot(kind = 'bar', stacked = True,color=['blue','red'])
mpl.title('table booking vs rate',fontsize = 18)
mpl.legend(loc="upper right")
mpl.savefig("Table_Booking_Rate.png")
mpl.show()


# In[20]:


sbn.countplot(zom_new['city'])
sbn.countplot(zom_new['city']).set_xticklabels(sbn.countplot(zom_new['city']).get_xticklabels(), rotation=90, ha="right")
fig = mpl.gcf()
fig.set_size_inches(12,12)
mpl.savefig("Location.png")
mpl.title('Location',fontsize=18)


# In[21]:


loc_plt=pds.crosstab(zom_new['rate'],zom_new['city'])
loc_plt.plot(kind='bar',stacked=True);
mpl.title('Location - Rating',fontsize=18)
mpl.ylabel('Location',fontsize=12)
mpl.xlabel('Rating',fontsize=12)
mpl.xticks(fontsize=8)
mpl.yticks(fontsize=8);
mpl.legend().remove();
mpl.savefig("Location Rating.png")


# In[22]:


sbn.countplot(zom_new['rest_type'])
sbn.countplot(zom_new['rest_type']).set_xticklabels(sbn.countplot(zom_new['rest_type']).get_xticklabels(), rotation=90, ha="right")
fig = mpl.gcf()
fig.set_size_inches(12,12)
mpl.savefig("Restaurant Type.png")
mpl.title('Restaurant Type',fontsize=18)


# In[23]:


loc_plt=pds.crosstab(zom_new['rate'],zom_new['rest_type'])
loc_plt.plot(kind='bar',stacked=True);
mpl.title('Rest. type - Rating',fontsize=18)
mpl.ylabel('Rest. type',fontsize=12)
mpl.xlabel('Rating',fontsize=12)
mpl.xticks(fontsize=10)
mpl.yticks(fontsize=10);
mpl.legend().remove();
mpl.savefig('Rest Type-Rating.png')


# In[24]:


sbn.countplot(zom_new['type'])
sbn.countplot(zom_new['type']).set_xticklabels(sbn.countplot(zom_new['type']).get_xticklabels(), rotation=90, ha="right")
fig = mpl.gcf()
fig.set_size_inches(12,12)
mpl.title('Type of Service',fontsize=18)
mpl.savefig('Type of Service.png')


# In[25]:


type_plt=pds.crosstab(zom_new['rate'],zom_new['type'])
type_plt.plot(kind='bar',stacked=True);
mpl.title('Type and Rating',fontsize=18)
mpl.ylabel('Type',fontsize=12)
mpl.xlabel('Rating',fontsize=12)
mpl.xticks(fontsize=10)
mpl.yticks(fontsize=10);
mpl.savefig('Type and Rating.png')


# In[26]:


sbn.countplot(zom_new['cost'])
sbn.countplot(zom_new['cost']).set_xticklabels(sbn.countplot(zom_new['cost']).get_xticklabels(), rotation=90, ha="right")
fig = mpl.gcf()
fig.set_size_inches(12,12)
mpl.title('Cost(Restaurant)',fontsize=18)
mpl.savefig('Cost(Restaurant).png')

