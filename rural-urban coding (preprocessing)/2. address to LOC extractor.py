import pandas as pd
import numpy as np
import string
import requests
import geopy
from geopy.geocoders import GeoNames

geo = GeoNames(username='maria.jl')
geo_nominatim = geopy.Nominatim(user_agent='1234')

loc_data = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Data files\participant home addresses.csv')

### adding empty columns to be filled with distinct location information
loc_data['ZIP'] = '' 
loc_data['city/census region'] = ''
loc_data['county'] = ''
loc_data['state'] = ''
loc_data['state (abbreviation)'] = ''
loc_data['FIPS (state-county-tract)'] = ''
loc_data[''] = ''
loc_data['neighbourhood (from GeoNames API)'] = ''
loc_data['ZIP (from Nominatim)'] = ''
loc_data['county (from Nominatim)'] = ''

def extract_state_zip ():
    '''
    This function takes the input of an address (global var) in the form of a list 
    such as ["street address", "town/city", "state ZIP", "country"] and extracts the
    state and ZIP code. For the addresses in this project, the function should 
    always provide state as an abbreviation.

    '''

    try:
        state_zip = address[-2]
        state_zip = address[-2].split(" ")

        if len(state_zip) == 1:  ## accounts for error when state_zip contains only state
            state_zip.append("N/A")

        return state_zip

    except:     # accounts for error when state_zip contains no state or ZIP
        state_zip = ["N/A", "N/A"]
        return state_zip

def extract_city ():
    '''
    This function takes the input of an address (global var) in the form of a list such  
    as ["street address", "town/city", "state ZIP", "country"] and extracts the 
    city/town. It accounts for the exceptions where address has 'xxxx+xx city' and 
    where city is not present in the address.

    '''

    try:
        a = address[-3].index("+") # accounts for when address has 'xxxx+xx city' form
        return address[-3][a+4:]

    except ValueError:       # address in normal form
        return address[-3]

    except IndexError: # if address does not actually include city
        return 'N/A'

def FCCinfo ():
    '''
    This function takes the input of latitude and longitude (global vars, as "lat" 
    and "long") and uses the FCC block API to find the corresponding 10-11 digit 
    FIPS code (corresponding to city, county, and census tract) and the county name,
    returned in a list as ["FIPS", "county name"].

    The library 'requests' must be imported previously.

    '''

    try:
        FCCloc = requests.get(f"https://geo.fcc.gov/api/census/block/find?format=json&latitude={lat}&longitude={long}&censusyear=2020")
        FCCloc = FCCloc.text.split('"')

        loc_info = []
        loc_info.append(FCCloc[FCCloc.index('FIPS') + 2][0:11])     ### to extract FIPS code
        loc_info.append(FCCloc[FCCloc.index('County') + 8])        ### to extract county

        return loc_info

    except requests.exceptions.ConnectionError:
        print("No response from fcc.gov (missing FIPS & county).")
        return ['N/A', 'N/A']

def GeoNamesinfo ():
    '''
    This function takes the input of latitude and longitude (global vars, as "lat" 
    and "long") and uses the GeoNames reverse geolocator library/API to find the
    corresponding neighborhood and state name. They are returned in a list as 
    [neighborhood, state, country].

    The GeoNames library from Geopy must be previously imported as "geo".

    NOTE: the geolocator (interestingly) also returns a latitude and longitude
    which seem to be slightly different from the latitude and longitude provided.

    '''

    try:    
        GN_loc = geo.reverse(query=(lat, long), exactly_one = False, timeout = 5) 
        neighborhood_state_country = str(GN_loc[0]).split(", ")
        return neighborhood_state_country

    except:
        print("GeoNames error (missing neighborhood, lat, lng).")
        return ["N/A", "N/A", "N/A"]

def Nominatiminfo ():
    '''
    This function takes the input of latitude and longitude (global vars, as "lat" 
    and "long") and uses the Geopy module/API Nominatim to find the corresponding
    county name and ZIP (in this project, used as a "check" against the extracted 
    ZIP and the FCC county name) and return them in a list as [ZIP, county].

    The Nominatim library from Geopy must be previously imported as "geo_nominatim".
    '''

    loc_info = []

    ### extract Nominatim ZIP as a check
    try:
        N_loc = geo_nominatim.reverse((lat, long))
        loc_info.append(N_loc.raw['address']['postcode'])

    except KeyError:    # accounts for error if no postcode is present in location information
        loc_info.append("N/A")


    ### extract Nominatim county as a check
    try:
        loc_info.append(N_loc.raw['address']['county']) 

    except KeyError:    # accounts for error if no county is present in location information
        loc_info.append("N/A")

    return loc_info


for i in range(len(loc_data)):      ### for each row, or participant,
    lat = loc_data.iloc[i, 1]       ## extract their home location (in lat, long)
    long = loc_data.iloc[i, 2]

    if lat == 0:                     ## if participant's home location was undetermined by skmob
        loc_data.iloc[i, 1:] = 'N/A'     # then make all location information = NaN
    else:
        address = loc_data.iloc[i, 3].split(", ")

        state_zip = extract_state_zip()
        neighborhood_state_county = GeoNamesinfo()
        ZIP_county = Nominatiminfo()
        FIPS_county = FCCinfo()

        loc_data.iloc[i, 4] = state_zip[1] # ZIP (from GoogleMaps address)
        loc_data.iloc[i, 5] = extract_city() # city (from GoogleMaps address)
        loc_data.iloc[i, 6] = FIPS_county[1] # county (from FCC, using lat/long)
        loc_data.iloc[i, 7] = neighborhood_state_county[1] # state (from GeoNames, using lat/long)
        loc_data.iloc[i, 8] = state_zip[0] # state abbreviation (from GoogleMaps address)
        loc_data.iloc[i, 9] = FIPS_county[0] # full FIPS code (from FCC, using lat/long)
        loc_data.iloc[i, 11] = neighborhood_state_county[0] # neighborhood (from GeoNames, using lat/long)
        loc_data.iloc[i, 12] = ZIP_county[0] # ZIP (from Nominatim, using lat/long)
        loc_data.iloc[i, 13] = ZIP_county[1] # county (from Nominatim, using lat/long)


## ensures all words in county name are capitalized, e.g. St. Louis city --> St. Louis City
for i in range(len(loc_data)):
    loc_data.iloc[i, 6] = string.capwords(loc_data.iloc[i, 6])


loc_data.to_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Data files\participant home locations.csv', index = False)
