#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install lxml')
get_ipython().system('pip install geopy')
import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

#!conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 


from IPython.display import display_html
import pandas as pd
import numpy as np
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors

print('Folium installed')
print('Libraries imported.')


# In[2]:


source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup=BeautifulSoup(source,'lxml')
print(soup.title)
from IPython.display import display_html
tab = str(soup.table)
display_html(tab,raw=True)


# In[3]:


dfs = pd.read_html(tab)
df=dfs[0]
df.head()


# # Data preprocessing and cleaning

# In[20]:


# Dropping the rows where Borough is 'Not assigned'
df1 = df[df.Borough != 'Not assigned']

# Combining the neighbourhoods with same Postalcode
df2 = df1.groupby(['Postal Code','Borough'], sort=False).agg(', '.join)
df2.reset_index(inplace=True)

# Replacing the name of the neighbourhoods which are 'Not assigned' with names of Borough
df2['Neighborhood'] = np.where(df2['Neighborhood'] == 'Not assigned',df2['Borough'], df2['Neighborhood'])

df2


# In[8]:


# Shape of data frame
df2.shape


# # Importing the csv file conatining the latitudes and longitudes for various neighbourhoods in Canada

# In[21]:


lat_lon = pd.read_csv('https://cocl.us/Geospatial_data')
lat_lon.head()


# # Merging the two tables for getting the Latitudes and Longitudes for various neighbourhoods in Canada

# In[22]:


df3 = pd.merge(df2,lat_lon)
df3.head()


# # The notebook from here includes the Clustering and the plotting of the neighbourhoods of Canada which contain Toronto in their Borough

# ## Getting all the rows from the data frame which contains Toronto in their Borough.

# In[23]:


df4 = df3[df3['Borough'].str.contains('Toronto',regex=False)]
df4


# # Visualizing all the Neighbourhoods of the above data frame using Folium

# In[25]:


map_toronto = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

for lat,lng,borough,neighbourhood in zip(df4['Latitude'],df4['Longitude'],df4['Borough'],df4['Neighborhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
    [lat,lng],
    radius=5,
    popup=label,
    color='blue',
    fill=True,
    fill_color='#3186cc',
    fill_opacity=0.7,
    parse_html=False).add_to(map_toronto)
map_toronto


# In[ ]:




