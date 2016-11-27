#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 19:29:52 2016

@author: montassar
"""

import urllib
import json
import requests
import numpy as np
import geocoder


radius=10000  
def dataCleaningSolution(cityName,minPrice,maxPrice,daysNumber,interest,roomsNumber,currency):
    g = geocoder.google(cityName)

    cityLat=g.latlng[0]
    cityLng=g.latlng[1]
    placesNumber=10
    
    urlAirbnb='https://api.airbnb.com/v2/search_results?'
    valuesAirbnb ={'client_id':'Your_Client_ID',
             'currency':currency,
             'locale':'en-US',
             'user_lat':cityLat,
             'user_lng':cityLng,
             'location':cityName,
             'min_bedrooms':roomsNumber,
             '_limit':'10',
             'guests':'1',
             '_format':'for_search_results_with_minimal_pricing',
             'price_min':minPrice,  
             'price_max':maxPrice,
             'sort':'1'}
    dataAirbnb= urllib.urlencode(valuesAirbnb)
    r = requests.get(urlAirbnb,dataAirbnb)
    Airbnbdata=json.loads(r.content)
    Final=np.zeros((len(Airbnbdata['search_results']), 6))
    houses={}
    for  i in range(len(Airbnbdata['search_results'])):  
        Price=Airbnbdata['search_results'][i]['pricing_quote']['rate']['amount']
        Houselat=Airbnbdata['search_results'][i]['listing']['lat']
        Houselng=Airbnbdata['search_results'][i]['listing']['lng']
        Houseid=Airbnbdata['search_results'][i]['listing']['id']
        Final[i]=[Houseid,Houselat,Houselng,Price,0,0]
        houses[str(i)]={'id':Houseid,'lat':Houselat,'lng':Houselng,'amount':Price}
    cityLoc=str(cityLat)+','+str(cityLng)
    urlLocations='https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    valuesLocations={
             'key': 'Your_key',
             'location':cityLoc,
             'radius':radius,
             'rankby':'prominence',
             'type':interest
             }
    dataLocations= urllib.urlencode(valuesLocations)
    r = requests.get(urlLocations,dataLocations)
    Locationsdata=json.loads(r.content) 
    places={}
    for  j in range(len(Airbnbdata['search_results'])):  
        cityLat=Final[j][1]
        cityLng=Final[j][2]
        value=0
        for  i in range(placesNumber):     
            poiLat=Locationsdata['results'][i]['geometry']['location']['lat']
            poiLng=Locationsdata['results'][i]['geometry']['location']['lng']
            poiName=Locationsdata['results'][i]['name']    
            if (j==0):
                places[str(i)]={'name':poiName,'lat':poiLat,'lng':poiLng}
            valuesUber ={'start_latitude':cityLat,
                     'start_longitude':cityLng,
                     'end_latitude':poiLat,
                     'end_longitude':poiLng,
                     'server_token':'aSlAqRieU4ctPGVZOdkOaE2bVSVpUiJhdzTI0YR8'}
            
            urlUber = 'https://api.uber.com/v1/estimates/price?'
            dataUber = urllib.urlencode(valuesUber)
            r = requests.get(urlUber,dataUber)
            Uberdata=json.loads(r.content)
            uberMaxPrice=Uberdata['prices'][0]['high_estimate']
            uberMinPrice=Uberdata['prices'][0]['low_estimate']
            value+=(uberMaxPrice+uberMinPrice)/2
        Final[j][4]=value
        Final[j][5]=value*2+daysNumber*Final[j][3]
        print (j)
        with open('places_shopping_LA.json', 'w') as outfile:
            json.dump(places, outfile)
        with open('houses_LA.json', 'w') as outfile:
            json.dump(houses, outfile)
                
    return Final

matr=dataCleaningSolution('Los Angeles',5,1500,5,'food',1,'USD')