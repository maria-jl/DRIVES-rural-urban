import pandas as pd
import numpy as np

RUdata = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Data files\participant _ruralurbancodes.csv')
RUdata[""] = ''
RUdata["RUCA_ru"] = ''
RUdata["other_ru"] = ''

def convertRUcodetoRUclass(col, max_metro, max_micro, max_rural):
    '''
    This function converts any numerical rural-urban code to a 3-level classification
    (metro, micro, rural) according to the classifications defined in this project.
    It requires the rural-urban code data for participants to be uploaded as RUdata,
    in the format where one column has the rural-urban code for each participant
    and the next column on the right has an empty column for the metro/micro/rural
    classification.

    Arguments required are:
    col = column in RUdata where specific rural-urban code is found
    max_metro = the upper limit for which the specific code should be converted to metro (e.g. 3)
    max_micro = the upper limit for which the specific code should be converted to micro (e.g. 6)
    max_rural = the upper limit for which the specific code should be converted to rural (e.g. 10)
    
    '''

    if RUdata.iloc[i, col] <= max_metro:
        RUdata.iloc[i, col+1] = 'Metro'
    elif RUdata.iloc[i, col] <= max_micro:
        RUdata.iloc[i, col+1] = 'Micro'
    elif RUdata.iloc[i, col] <= max_rural:
        RUdata.iloc[i, col+1] = 'Rural'

def convertTRIclasstoRUclass(TRIcol, RUcol):
    '''
    This function converts the 3-level classification codes (metro, micro, rural)
    defined in this project into the final binary classification (urban, rural)
    where for this project, metro = urban and micro, rural, nonmetro, etc = rural.
    It requires the rural-urban code data for participants to be uploaded as RUdata,
    in the format where one column has the rural-urban code for each participant
    and the next column on the right has an empty column for the metro/micro/rural
    classification.

    Arguments required are:
    TRIcol = column in RUdata where 3-level class for desired rural-urban code is found (e.g. "RUCC_class")
    RUcol = column in RUdata where final binary classification will be placed (for this project, "RUCA_ru" and "other_ru")
    '''

    if RUdata.iloc[i, TRIcol] == 'Metro':
        RUdata.iloc[i, RUcol] = 'Urban' 
    elif RUdata.iloc[i, TRIcol] == 'Micro' or RUdata.iloc[i, TRIcol] == 'Rural':
        RUdata.iloc[i, RUcol] = 'Rural'

for i in range(len(RUdata)):
    convertRUcodetoRUclass(col = 2, max_metro = 3, max_micro = 6, max_rural = 10)  ## RUCA conversion (argument names are included for readability)
    convertRUcodetoRUclass(col = 4, max_metro = 3, max_micro = 7, max_rural = 9)  ## RUCC conversion
    convertRUcodetoRUclass(col = 6, max_metro = 4, max_micro = 5, max_rural = 6)  ## NCHS conversion
    convertRUcodetoRUclass(col = 10, max_metro = 2, max_micro = 8, max_rural = 12)  ## UIC conversion

    ## NOTE: OMB codes exist between NCHS and UIC columns, but already have a 3-level classification format

    convertTRIclasstoRUclass(TRIcol = 3, RUcol = 13)  ### converts RUCA class into rural/urban class ("RUCA_ru")
    convertTRIclasstoRUclass(TRIcol = 5, RUcol = 14)  ### converts RUCC class into rural/urban class ("other_ru");

    ### NOTE: for the sake of this project, "other_ru" should represent the classification for ALL
    ## codes other than RUCA since they seem to agree when condensed down to the binary classification;
    # however a manual check should be done if using this function on other datasets


RUdata.to_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Data files\participant _ruralurbancodes.csv', index = False)