#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import urllib.parse
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
from itertools import groupby
print('Imports Finished')

url = 'https://www.milesfaster.co.uk/london-postcodes-list.htm'
    
page = requests.get(url)
postcode_soup = bs(page.text, 'html.parser')
post_code_data = postcode_soup.find_all('td')
master_list = []
for line in post_code_data:
    post_code_raw = line.text
    post_code = post_code_raw.strip()
    master_list.append(post_code)
master_list = list(filter(None, master_list))
post_code_list = master_list[::2]
name_list = master_list[1::2]
df = pd.DataFrame({'Postcode': post_code_list, 'Area': name_list})
df1 = df['Postcode']

df1.to_csv('/Users/matthewbeale/Documents/Python/postcode.csv', index = False) 


# In[4]:


tiny_post_code_list = ['SE1']
final_url_list = []
#Scraping the number of webpages we need to scrape
for postcode in post_code_list:
    time.sleep(2)
    lpc = postcode.lower()
    first_url = f'https://www.zoopla.co.uk/to-rent/property/{lpc}/?page_size=100&price_frequency=per_month&q={postcode}&radius=0&results_sort=lowest_price&search_source=refine&view_type=list&pn=1'
    print(postcode)
    #print(first_url)
    page = requests.get(first_url)
    soup = bs(page.text, 'html.parser')
    data = soup.find_all('a',{'aria-disabled':'false'} )
    num_list = []
    for item in data:
        if item.text.strip() == 'Next >':
            continue
        elif item.text.strip() == None:
            continue
        elif item.text.strip() == '...':
            continue
        else:
            num_list.append(int(item.text.strip()))
    max_num = max(num_list)
    if max(num_list) == 1:
        final_num_list = [1]
    else:
        final_num_list = list(range(1, max_num+1))
    for i in final_num_list:
        url = f'https://www.zoopla.co.uk/to-rent/property/{lpc}/?page_size=100&price_frequency=per_month&q={postcode}&radius=0&results_sort=lowest_price&search_source=refine&view_type=list&pn={str(i)}'
        #print(url)
        final_url_list.append(url)
print('Finished')

    


# In[ ]:


#Checking postcodes
for url in final_url_list:
    print(url.split('/')[5])


# In[5]:


import requests
import urllib.parse
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
from itertools import groupby
#Creating and generating all the URL's necessary to scrape the data
url_list = []
id_list = [] #done
total_cost_per_month_list = [] #done
type_of_rental_list = [] #done
number_of_bedrooms_list = [] #done
post_code_list_df = [] #done
date_listed_list = [] #done
number_of_bathrooms_list = [] #done
number_of_living_rooms_list = [] #done
first_public_transport_distance_list = [] #done
first_public_transport_list = [] #done
second_public_transport_distance_list = [] #done
second_public_transport_list = [] #done
#can all be done within the dataframe
cost_per_bedroom_list = [] #done
bathrooms_to_bedrooms_ratio_list = [] #done
bedroom_to_living_room_ratio_list = [] #done
#extra stuff for latitude longitude and stations
address_list = []
def split_condition(x):
    return x in {''}
def pd_max_options(rows, columns):
    pd.set_option('display.max_rows', rows)
    pd.set_option('display.max_columns', columns)
def df_where(df_name, column_name, value):
    return df_name.loc[df_name[column_name]==value]
station_df = pd.read_csv('/Users/matthewbeale/Downloads/London stations.csv')
station_df['Zone'] = station_df['Zone'].astype(str).str[0]
debug_url_list = ['https://www.zoopla.co.uk/to-rent/property/n8/?page_size=100&price_frequency=per_month&q=N8&radius=0&results_sort=lowest_price&search_source=refine&view_type=list&pn=1']        
#print(url_list)
for url in final_url_list:
    print(url)
    #Scraping Price
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    data = soup.find_all('p', {'data-testid':'listing-price'})
    for item in data:
        item = item.text
        if item == 'POA':
            #print(item)
            total_cost_per_month_list.append(None)
        else:
            item = item[1:]
            item = item[:-4]
            item = item.strip()
            item = item.replace(',', '')
            item = int(item)
            total_cost_per_month_list.append(item)
        post_code_list_df.append(url.split('/')[5])
    #print(len(total_cost_per_month_list))
    #print(total_cost_per_month_list)
    #Scraping type of rental and number of bedrooms
    data = soup.find_all('h2', {'data-testid':'listing-title'})
    for item in data:
        text = item.text
        text = text.strip()
        #print(text)
        if 'Parking/garage' in text:
            listing_type = 'Parking Garage'
            num_bedrooms = None
        elif 'Room to rent' in text:
            listing_type = 'Room to Rent'
            num_bedrooms = 1
        elif 'Studio to rent' in text:
            listing_type = 'Studio'
            num_bedrooms = 1
        elif 'end terrace' in text:
            listing_type = 'Semi-Detached House'
            num_bedrooms = int(text.split(' ')[0])
        elif 'Block of flats' in text:
            listing_type = 'Property'
            num_bedrooms = 99999
            #Remember to remove Block of Flats type at the end
        elif 'flat' in text:
            listing_type = 'Flat'
            num_bedrooms = int(text.split(' ')[0])
        elif 'semi-detached house' in text:
            listing_type = 'Semi-Detached House'
            num_bedrooms = int(text.split(' ')[0])
        elif 'Semi-detached house' in text:
            listing_type = 'Semi-Detached House'
            num_bedrooms = None
        elif 'detached house' in text:
            listing_type = 'Detached House'
            num_bedrooms = int(text.split(' ')[0])
        elif 'Detached house' in text:
            listing_type = 'Detached House'
            num_bedrooms = None
        elif 'terraced' in text:
            listing_type = 'Terraced House'
            num_bedrooms = int(text.split(' ')[0])
        elif 'Terraced house' in text:
            listing_type = 'Terraced House'
            num_bedrooms = None
        elif 'maisonette' in text:
            listing_type = 'Maisonette'
            num_bedrooms = int(text.split(' ')[0])
        elif 'Maisonette' in text:
            listing_type = 'Maisonette'
            num_bedrooms = None
        elif 'shared accommodation' in text:
            listing_type = 'Room to Rent'
            num_bedrooms = 1
        elif 'Land to Rent' in text:
            listing_type = 'Land'
            num_bedrooms = 99999
            #Remember to Remove Land to Rent type at the end
        elif 'mews house' in text:
            listing_type = 'Terraced House'
            num_bedrooms = int(text.split(' ')[0])
        elif 'penthouse' in text:
            listing_type = 'Flat'
            num_bedrooms = int(text.split(' ')[0])
        elif 'bungalow' in text:
            listing_type = 'Bungalow'
            num_bedrooms = int(text.split(' ')[0])
        elif 'cottage' in text:
            listing_type = 'Detached House'
            num_bedrooms = int(text.split(' ')[0])
        elif 'town house' in text:
            listing_type = 'Townhouse'
            num_bedrooms = int(text.split(' ')[0])
        elif 'Town house' in text:
            listing_type = 'Townhouse'
            num_bedrooms = None
        elif 'barn conversion' in text:
            listing_type = 'Barn Conversion'
            num_bedrooms = int(text.split(' ')[0])
        else:
            #print(text)
            listing_type = 'Property'
            try:
                num_bedrooms = int(text.split(' ')[0])
            except ValueError:
                num_bedrooms = 0
        type_of_rental_list.append(listing_type)
        number_of_bedrooms_list.append(num_bedrooms)
    #print(type_of_rental_list)
    #print(len(type_of_rental_list))
    #Scraping an ID                                                                               Come back here 
    data = soup.find_all('div', {'id': lambda L: L and L.startswith('listing')})
    #print(data[0])
    for item in data:
        text = str(item).split(r'"')[1].split('_')[1]
        id_list.append(text)
#     print(len(id_list))
#     print(id_list)
    data = soup.find_all('li')
    for item in data:
        text = item.text
        if 'Listed on' in text:
            a = text.split(' ')
            a = a[2:]
            a[0] = a[0][:-2]
            a = '-'.join(a)
            a = datetime.strptime(a, '%d-%b-%Y').date()
            date_listed_list.append(a)
        else:
            continue
    #print(date_listed_list)
    #print(len(date_listed_list))
    nl = []
    for item in data:
        text = item.text
        nl.append(text)
    #print(nl)
    nl = nl[11:]
    #print(nl)
    #print(nl)
    grouper = groupby(nl, key=split_condition)
    res = dict(enumerate((list(j) for i, j in grouper if not i), 1))
    text_list = []
    for item in res.values():
        if len(item[-1]) <6:
            continue
        elif ' '.join(item).count('Listed') > 1:
            init = ' '.join(item)
            st_splt = (init.split('Listed'))[:-1]
            for item in st_splt:
                desc = item
                text_list.append(desc)
        else:
            desc = ' '.join(item) 
            text_list.append(desc)
    #Getting number of bathrooms
   # print('\n Values FROM RES \n')
    print(len(text_list))
    for item in text_list:
        if 'Bathrooms' in item:
            a = item.split('Bathrooms')
            number_of_bathrooms_list.append(int(a[1][0]))
        else:
            number_of_bathrooms_list.append(None)
    #Getting number of living rooms
    for item in text_list:
        if 'Living rooms' in item:
            a = item.split('Living rooms')
            number_of_living_rooms_list.append(int(a[1][0]))
        else:
            number_of_living_rooms_list.append(None)
    for item in text_list:
        if 'mile' in item:
            #finding first distance
            #print(item)
            a = item.split('mile')
            d1 = a[0].strip().split(' ')[-1]
            first_public_transport_distance_list.append(float(d1))
            #finding first station/public transport hub
            s1 = a[1]
            if s1[0] == 's':
                s1 = s1[1:].strip()
                s1 = s1.split(' ')[:-1]
                s1 = ' '.join(s1)
                first_public_transport_list.append(s1)
            else:
                s1 = s1.strip()
                s1 = s1.split(' ')[:-1]
                s1 = ' '.join(s1)
                first_public_transport_list.append(s1)
            #finding second distance
            #print(a)
            d2 = a[1].strip().split(' ')[-1]
            second_public_transport_distance_list.append(float(d2))
            #finding second public transport hub
            #print(a)
            s2 = a[2].strip()
            if s2[0] == 's':
                b = s2[1:].strip()
        #print(s2)
            else:
                b = s2.strip()
            #print(b)
            if 'Student' in b:
                second_station = b.split('Student')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Available Now' in b:
                second_station = b.split('Available Now')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Viewing' in b:
                    second_station = b.split('Viewing')[0].strip().replace('&', 'and')
                    second_public_transport_list.append(second_station)
            elif 'Period Property' in b:
                second_station = b.split('Period Property')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Balcony' in b:
                    second_station = b.split('Balcony')[0].strip().replace('&', 'and')
                    second_public_transport_list.append(second_station)
            elif 'Leisure Facilities' in b:
                second_station = b.split('Leisure Facilities')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif '24hr Security' in b:
                second_station = b.split('24hr')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Penthouse' in b:
                second_station = b.split('Penthouse')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Close to Train Station' in b:
                second_station = b.split('Close to Train Station')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Short Let' in b:
                second_station = b.split('Short Let')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            else:
                second_station = b.split('Listed')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)         
        else:
            first_public_transport_list.append(None)
            second_public_transport_list.append(None)
            first_public_transport_distance_list.append(None)
            second_public_transport_distance_list.append(None)
    print(f'{url} PARSED')
    print('Length of lists:')
    print('Total Cost')
    print(len(total_cost_per_month_list))
    #print((total_cost_per_month_list))
    print('Rental type')
    print(len(type_of_rental_list))
    #print((type_of_rental_list))    
    print('Num bedrooms')
    print(len(number_of_bedrooms_list))
    #print((number_of_bedrooms_list))
    print('postcode')
    print(len(post_code_list_df))
    #print((post_code_list_df))    
    print('date listed')
    print(len(date_listed_list))
    #print((date_listed_list))
    print('number bathrooms')
    print(len(number_of_bathrooms_list))
   # print((number_of_bathrooms_list))
    print('living rooms')
    print(len(number_of_living_rooms_list))
    #print((number_of_living_rooms_list))
    print('first pt dist')
    print(len(first_public_transport_distance_list))
    #print((first_public_transport_distance_list))
    print('first pt')
    print(len(first_public_transport_list))
    #print((first_public_transport_list))
    print('second pt dist')
    print(len(second_public_transport_distance_list))
    #print((second_public_transport_distance_list))
    print('second pt')
    print(len(second_public_transport_list))
    #print((second_public_transport_list))
df = pd.DataFrame({'ID':id_list,
                  'Total Cost per Month': total_cost_per_month_list,
                  'Rental Type':type_of_rental_list,
                  'Number of Bedrooms': number_of_bedrooms_list,
                  'Postcode': post_code_list_df,
                  'Date Listed': date_listed_list,
                  'Number of Bathrooms': number_of_bathrooms_list,
                  'Number of Living Rooms': number_of_living_rooms_list,
                  'Distance to First Public Transport Hub (Miles)': first_public_transport_distance_list,
                  'First Public Transport Hub Name': first_public_transport_list,
                  'Distance to Second Public Transport Hub (Miles)': second_public_transport_distance_list,
                  'Second Public Transport Hub Name': second_public_transport_list})
df.to_csv('/Users/matthewbeale/Documents/Python/rental_csv.csv', index = False)    
df['Cost per Bedroom'] = df['Total Cost per Month']/df['Number of Bedrooms']
df['Bedrooms to Bathrooms Ratio'] = df['Number of Bedrooms']/df['Number of Bathrooms']
df['Bedrooms to Living Rooms Ratio'] = df['Number of Bedrooms']/df['Number of Living Rooms']
pd_max_options(500,500)
df = pd.merge(left=df, right=station_df, how = 'left', left_on = 'First Public Transport Hub Name',
         right_on = 'Station')
df = df.drop(['Station', 'OS X', 'OS Y', 'Latitude', 'Longitude', 'Postcode_y'], axis=1)
failed_station_df = df[df['Zone'].isna()]
failed_station_df = pd.merge(left=failed_station_df, right = station_df, how = 'left',
                             left_on = 'Second Public Transport Hub Name',
                             right_on = 'Station')
failed_station_df = failed_station_df.drop(['Station', 'OS X', 'OS Y', 'Latitude', 'Longitude', 'Zone_x', 'Postcode'], axis=1)
failed_station_df = failed_station_df.rename(columns={'Postcode_x':'Postcode', 'Zone_y':'Zone'})
df = df.rename(columns={'Postcode_x':'Postcode'})
pd_max_options(500,20)
df = pd.concat([df, failed_station_df])
df = df.drop_duplicates(subset = 'ID', keep='last').sort_values(by=['Total Cost per Month'])
df = df.reset_index(drop=True)
df
            
    





    
    


# In[7]:


df


# In[8]:


df.to_csv('/Users/matthewbeale/Documents/Python/Rent Price Analysis/Rental_DF_DEC22_EXAMPLE.csv', index=False)


# ##
# Debugging script

# In[108]:


import requests
import urllib.parse
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
from itertools import groupby
#Creating and generating all the URL's necessary to scrape the data
url_list = []
id_list = [] #done
total_cost_per_month_list = [] #done
type_of_rental_list = [] #done
number_of_bedrooms_list = [] #done
post_code_list_df = [] #done
date_listed_list = [] #done
number_of_bathrooms_list = [] #done
number_of_living_rooms_list = [] #done
first_public_transport_distance_list = [] #done
first_public_transport_list = [] #done
second_public_transport_distance_list = [] #done
second_public_transport_list = [] #done
#can all be done within the dataframe
cost_per_bedroom_list = [] #done
bathrooms_to_bedrooms_ratio_list = [] #done
bedroom_to_living_room_ratio_list = [] #done
#extra stuff for latitude longitude and stations
address_list = []
def split_condition(x):
    return x in {''}
def pd_max_options(rows, columns):
    pd.set_option('display.max_rows', rows)
    pd.set_option('display.max_columns', columns)
def df_where(df_name, column_name, value):
    return df_name.loc[df_name[column_name]==value]
station_df = pd.read_csv('/Users/matthewbeale/Downloads/London stations.csv')
station_df['Zone'] = station_df['Zone'].astype(str).str[0]
debug_url_list = ['https://www.zoopla.co.uk/to-rent/property/nw3/?page_size=100&price_frequency=per_month&q=NW3&radius=0&results_sort=lowest_price&search_source=refine&view_type=list&pn=3']        
#print(url_list)
for url in debug_url_list:
    print(url)
    #Scraping Price
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    data = soup.find_all('p', {'data-testid':'listing-price'})
    for item in data:
        item = item.text
        if item == 'POA':
            #print(item)
            total_cost_per_month_list.append(None)
        else:
            item = item[1:]
            item = item[:-4]
            item = item.strip()
            item = item.replace(',', '')
            item = int(item)
            total_cost_per_month_list.append(item)
        post_code_list_df.append(url.split('/')[5])
    #print(len(total_cost_per_month_list))
    #print(total_cost_per_month_list)
    #Scraping type of rental and number of bedrooms
    data = soup.find_all('h2', {'data-testid':'listing-title'})
    for item in data:
        text = item.text
        text = text.strip()
        #print(text)
        if 'Parking/garage' in text:
            listing_type = 'Parking Garage'
            num_bedrooms = None
        elif 'Room to rent' in text:
            listing_type = 'Room to Rent'
            num_bedrooms = 1
        elif 'Studio to rent' in text:
            listing_type = 'Studio'
            num_bedrooms = 1
        elif 'end terrace' in text:
            listing_type = 'Semi-Detached House'
            num_bedrooms = int(text.strip()[0])
        elif 'Block of flats' in text:
            listing_type = 'Property'
            num_bedrooms = 99999
            #Remember to remove Block of Flats type at the end
        elif 'flat' in text:
            listing_type = 'Flat'
            num_bedrooms = int(text.strip()[0])
        elif 'semi-detached house' in text:
            listing_type = 'Semi-Detached House'
            num_bedrooms = int(text.strip()[0])
        elif 'Semi-detached house' in text:
            listing_type = 'Semi-Detached House'
            num_bedrooms = None
        elif 'detached house' in text:
            listing_type = 'Detached House'
            num_bedrooms = int(text.strip()[0])
        elif 'Detached house' in text:
            listing_type = 'Detached House'
            num_bedrooms = None
        elif 'terraced' in text:
            listing_type = 'Terraced House'
            num_bedrooms = int(text.strip()[0])
        elif 'Terraced house' in text:
            listing_type = 'Terraced House'
            num_bedrooms = None
        elif 'maisonette' in text:
            listing_type = 'Maisonette'
            num_bedrooms = int(text.strip()[0])
        elif 'Maisonette' in text:
            listing_type = 'Maisonette'
            num_bedrooms = None
        elif 'shared accommodation' in text:
            listing_type = 'Room to Rent'
            num_bedrooms = 1
        elif 'Land to Rent' in text:
            listing_type = 'Land'
            num_bedrooms = 99999
            #Remember to Remove Land to Rent type at the end
        elif 'mews house' in text:
            listing_type = 'Terraced House'
            num_bedrooms = int(text.strip()[0])
        elif 'penthouse' in text:
            listing_type = 'Flat'
            num_bedrooms = int(text.strip()[0])
        elif 'bungalow' in text:
            listing_type = 'Bungalow'
            num_bedrooms = int(text.strip()[0])
        elif 'cottage' in text:
            listing_type = 'Detached House'
            num_bedrooms - int(text.strip()[0])
        elif 'town house' in text:
            listing_type = 'Townhouse'
            num_bedrooms = int(text.strip()[0])
        elif 'Town house' in text:
            listing_type = 'Townhouse'
            num_bedrooms = None
        elif 'barn conversion' in text:
            listing_type = 'Barn Conversion'
            num_bedrooms = int(text.strip()[0])
        else:
            #print(text)
            listing_type = 'Property'
            try:
                num_bedrooms = int(text.strip()[0])
            except ValueError:
                num_bedrooms = 0
        type_of_rental_list.append(listing_type)
        number_of_bedrooms_list.append(num_bedrooms)
    #print(type_of_rental_list)
    #print(len(type_of_rental_list))
    #Scraping an ID                                                                               Come back here 
    data = soup.find_all('div', {'id': lambda L: L and L.startswith('listing')})
    #print(data[0])
    for item in data:
        text = str(item).split(r'"')[1].split('_')[1]
        id_list.append(text)
#     print(len(id_list))
#     print(id_list)
    data = soup.find_all('li')
    for item in data:
        text = item.text
        if 'Listed on' in text:
            a = text.split(' ')
            a = a[2:]
            a[0] = a[0][:-2]
            a = '-'.join(a)
            a = datetime.strptime(a, '%d-%b-%Y').date()
            date_listed_list.append(a)
        else:
            continue
    #print(date_listed_list)
    #print(len(date_listed_list))
    nl = []
    for item in data:
        text = item.text
        nl.append(text)
    #print(nl)
    nl = nl[11:]
    #print(nl)
    #print(nl)
    grouper = groupby(nl, key=split_condition)
    res = dict(enumerate((list(j) for i, j in grouper if not i), 1))
    text_list = []
    print(res, '\n')
    for item in res.values():
        if len(item[-1]) <6:
            continue
        elif ' '.join(item).count('Listed') > 1:
            init = ' '.join(item)
            st_splt = (init.split('Listed'))[:-1]
            for item in st_splt:
                desc = item
                text_list.append(desc)
        else:
            desc = ' '.join(item) 
            text_list.append(desc)
    #Getting number of bathrooms
   # print('\n Values FROM RES \n')
    #print(len(text_list))
    for item in text_list:
        if 'Bathrooms' in item:
            a = item.split('Bathrooms')
            number_of_bathrooms_list.append(int(a[1][0]))
            print(item, '\n')
        else:
            number_of_bathrooms_list.append(None)
            print(item, '\n')
    #Getting number of living rooms
    for item in text_list:
        if 'Living rooms' in item:
            a = item.split('Living rooms')
            number_of_living_rooms_list.append(int(a[1][0]))
        else:
            number_of_living_rooms_list.append(None)
    for item in text_list:
        if 'mile' in item:
            #finding first distance
            #print(item)
            a = item.split('mile')
            d1 = a[0].strip().split(' ')[-1]
            first_public_transport_distance_list.append(float(d1))
            #finding first station/public transport hub
            s1 = a[1]
            if s1[0] == 's':
                s1 = s1[1:].strip()
                s1 = s1.split(' ')[:-1]
                s1 = ' '.join(s1)
                first_public_transport_list.append(s1)
            else:
                s1 = s1.strip()
                s1 = s1.split(' ')[:-1]
                s1 = ' '.join(s1)
                first_public_transport_list.append(s1)
            #finding second distance
            #print(a)
            d2 = a[1].strip().split(' ')[-1]
            second_public_transport_distance_list.append(float(d2))
            #finding second public transport hub
            #print(a)
            s2 = a[2].strip()
            if s2[0] == 's':
                b = s2[1:].strip()
        #print(s2)
            else:
                b = s2.strip()
            #print(b)
            if 'Student' in b:
                second_station = b.split('Student')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Available Now' in b:
                second_station = b.split('Available Now')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Viewing' in b:
                    second_station = b.split('Viewing')[0].strip().replace('&', 'and')
                    second_public_transport_list.append(second_station)
            elif 'Period Property' in b:
                second_station = b.split('Period Property')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Balcony' in b:
                    second_station = b.split('Balcony')[0].strip().replace('&', 'and')
                    second_public_transport_list.append(second_station)
            elif 'Leisure Facilities' in b:
                second_station = b.split('Leisure Facilities')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif '24hr Security' in b:
                second_station = b.split('24hr')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Penthouse' in b:
                second_station = b.split('Penthouse')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Close to Train Station' in b:
                second_station = b.split('Close to Train Station')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            elif 'Short Let' in b:
                second_station = b.split('Short Let')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)
            else:
                second_station = b.split('Listed')[0].strip().replace('&', 'and')
                second_public_transport_list.append(second_station)         
        else:
            first_public_transport_list.append(None)
            second_public_transport_list.append(None)
            first_public_transport_distance_list.append(None)
            second_public_transport_distance_list.append(None)
    print(f'{url} PARSED')
    print('Length of lists:')
    print('Total Cost')
    print(len(total_cost_per_month_list))
    #print((total_cost_per_month_list))
    print('Rental type')
    print(len(type_of_rental_list))
    #print((type_of_rental_list))    
    print('Num bedrooms')
    print(len(number_of_bedrooms_list))
    #print((number_of_bedrooms_list))
    print('postcode')
    print(len(post_code_list_df))
    #print((post_code_list_df))    
    print('date listed')
    print(len(date_listed_list))
    #print((date_listed_list))
    print('number bathrooms')
    print(len(number_of_bathrooms_list))
    print((number_of_bathrooms_list))
    print('living rooms')
    print(len(number_of_living_rooms_list))
    print((number_of_living_rooms_list))
    print('first pt dist')
    print(len(first_public_transport_distance_list))
    print((first_public_transport_distance_list))
    print('first pt')
    print(len(first_public_transport_list))
    print((first_public_transport_list))
    print('second pt dist')
    print(len(second_public_transport_distance_list))
    print((second_public_transport_distance_list))
    print('second pt')
    print(len(second_public_transport_list))
    print((second_public_transport_list))
# df = pd.DataFrame({'ID':id_list,
#                   'Total Cost per Month': total_cost_per_month_list,
#                   'Rental Type':type_of_rental_list,
#                   'Number of Bedrooms': number_of_bedrooms_list,
#                   'Postcode': post_code_list_df,
#                   'Date Listed': date_listed_list,
#                   'Number of Bathrooms': number_of_bathrooms_list,
#                   'Number of Living Rooms': number_of_living_rooms_list,
#                   'Distance to First Public Transport Hub (Miles)': first_public_transport_distance_list,
#                   'First Public Transport Hub Name': first_public_transport_list,
#                   'Distance to Second Public Transport Hub (Miles)': second_public_transport_distance_list,
#                   'Second Public Transport Hub Name': second_public_transport_list})
# df.to_csv('/Users/matthewbeale/Documents/Python/rental_csv.csv', index = False)    
# df['Cost per Bedroom'] = df['Total Cost per Month']/df['Number of Bedrooms']
# df['Bedrooms to Bathrooms Ratio'] = df['Number of Bedrooms']/df['Number of Bathrooms']
# df['Bedrooms to Living Rooms Ratio'] = df['Number of Bedrooms']/df['Number of Living Rooms']
# pd_max_options(500,500)
# df = pd.merge(left=df, right=station_df, how = 'left', left_on = 'First Public Transport Hub Name',
#          right_on = 'Station')
# df = df.drop(['Station', 'OS X', 'OS Y', 'Latitude', 'Longitude', 'Postcode_y'], axis=1)
# failed_station_df = df[df['Zone'].isna()]
# failed_station_df = pd.merge(left=failed_station_df, right = station_df, how = 'left',
#                              left_on = 'Second Public Transport Hub Name',
#                              right_on = 'Station')
# failed_station_df = failed_station_df.drop(['Station', 'OS X', 'OS Y', 'Latitude', 'Longitude', 'Zone_x', 'Postcode'], axis=1)
# failed_station_df = failed_station_df.rename(columns={'Postcode_x':'Postcode', 'Zone_y':'Zone'})
# df = df.rename(columns={'Postcode_x':'Postcode'})
# pd_max_options(500,20)
# df = pd.concat([df, failed_station_df])
# df = df.drop_duplicates(subset = 'ID', keep='last').sort_values(by=['Total Cost per Month'])
# df = df.reset_index(drop=True)
# df
            
    





    
    


# In[397]:


#Manipulating Station CSV
station_df = pd.read_csv('/Users/matthewbeale/Downloads/London stations.csv')
station_df['Zone'] = station_df['Zone'].astype(str).str[0]
station_df

