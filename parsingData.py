#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 10:08:17 2016

@author: montassar
"""

import urllib
import json
import requests
import numpy as np
import geocoder
from sklearn import linear_model


radius=10000  
def ParsingUber(cityName,interest):
    g = geocoder.google(cityName)
    ubersHistory={}
    cityLat=g.latlng[0]
    cityLng=g.latlng[1]
    cityLoc=str(cityLat)+','+str(cityLng)
    urlLocations='https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    valuesLocations={
             'key': 'AIzaSyCeqGfv4Ve920GWngec1OiV2gALX_XdpUk',
             'location':cityLoc,
             'radius':radius,
             'rankby':'prominence',
             'type':interest
             }
    dataLocations= urllib.urlencode(valuesLocations)
    r = requests.get(urlLocations,dataLocations)
    Locationsdata=json.loads(r.content) 
    poiLat=Locationsdata['results'][1]['geometry']['location']['lat']
    poiLng=Locationsdata['results'][1]['geometry']['location']['lng']
    poiName=Locationsdata['results'][1]['name']  
    for i in range(2):     
        valuesUber ={'start_latitude':cityLat,
                 'start_longitude':cityLng,
                 'end_latitude':poiLat+i*0.001,
                 'end_longitude':poiLng+i*0.001,
                 'server_token':'aSlAqRieU4ctPGVZOdkOaE2bVSVpUiJhdzTI0YR8'}
        
        urlUber = 'https://api.uber.com/v1/estimates/price?'
        dataUber = urllib.urlencode(valuesUber)
        r = requests.get(urlUber,dataUber)
        ubersHistory[str(i)]=json.loads(r.content)
        print(i)
    with open('places_'+interest+'_'+cityName+'.json', 'w') as outfile:
        json.dump(ubersHistory, outfile)
    return ubersHistory
def ParsingAirbnb(cityName,roomsNumber,step,maxPrice):
    g = geocoder.google(cityName)
    AirbnbHistory={}
    cityLat=g.latlng[0]
    cityLng=g.latlng[1]
    minPrice=0
    urlAirbnb='https://api.airbnb.com/v2/search_results?'
    for i in range(100):
        valuesAirbnb ={'client_id':'3092nxybyb0otqw18e8nh5nty',
                 'currency':'USD',
                 'locale':'en-US',
                 'user_lat':cityLat,
                 'user_lng':cityLng,
                 'location':cityName,
                 'min_bedrooms':roomsNumber,
                 '_limit':'50',
                 'guests':'1',
                 '_format':'for_search_results_with_minimal_pricing',
                 'price_min':minPrice,  
                 'price_max':maxPrice,
                 'sort':'1'}
        dataAirbnb= urllib.urlencode(valuesAirbnb)
        r = requests.get(urlAirbnb,dataAirbnb)
        minPrice=maxPrice
        maxPrice+=i*step
        AirbnbHistory[str(i)]=json.loads(r.content)
        print(i)
    with open('places_Houses_'+cityName+'.json', 'w') as outfile:
        json.dump(AirbnbHistory, outfile)
    return AirbnbHistory
AirbnbHistory=ParsingAirbnb('Paris',1,5,20)   