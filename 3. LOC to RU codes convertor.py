import pandas as pd
import numpy as np

locdata = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Data files\participant home locations.csv')

RUdata = pd.DataFrame(columns = ['uid', 'RUCA (from ZIP)', "RUCA (from state-county-tract FIPS)", "RUCA_class",
"RUCC", "RUCC_class", "NCHS", "NCHS_class", "OMB (from atlas)", "OMB (from FORHP)", "UIC", "UIC_class"])
RUdata['uid'] = locdata['uid']

RUCA1 = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Rural_urban codes\RUCA2010_zipcode.csv')
RUCA2 = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Rural_urban codes\RUCA2010_county_FIPS.csv')
RUCC = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Rural_urban codes\RUCC2013_county_FIPS.csv')
NCHS = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Rural_urban codes\NCHS2013_county_FIPS.csv')
atlas = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Comparison files\USDA_ERS_RuralAtlasData_county classifications.csv')
FORHP = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Rural_urban codes\HRSA_county_FIPS_ZIP.csv')
UIC = pd.read_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Rural_urban codes\UIC2013_county_FIPS.csv')


def findgeneralRUcode (RUfile, loc_col, RU_col, loc_code, end_col):
    '''
    This function converts participants' location codes loaded from locdata (e.g. ZIP,
    FIPS) into some desired rural-urban code.To do so, the program attempts to find
    the row in the rural-urban code file that contains the participant loc_code. If 
    successful, it extracts the rural-urban code in this row and places it in RUdata.
    The arguments required make this function generalizable to different files with
    data in different columns, but does require manual checking of these files.

    Arguments required are:
    RUfile (var) = variable name of the loaded file that contains data for the desired
    rural-urban code (e.g. a file containing RUCA codes corresponding to different 
    ZIP codes)

    loc_col (str) = column name in the loaded file that contains the loc_code that will be
    used

    RU_col (int) = index of the column in the loaded file that contains the rural-urban code

    loc_code (*) = the location code that will be used to find the desired rural-urban code
    (e.g. ZIP); it is specific to the rural-urban code file being used (i.e. some comparison 
    files will require ZIP, some FIPS, some the county name, etc) and must be inputted in 
    the format required for the specific file (*e.g. as a string, numpy integer, etc)
    
    end_col (int) = index of the column in RUdata where the rural-urban code should be placed
    
    '''

    if isinstance(loc_code, str) == True: ## if the location code is inputed a string, the program will search for substring matches within the loaded file
        try:
            row = RUfile[RUfile[loc_col].str.contains(loc_code)]  ## allows searching for substring if formatting prevents an exact match, e.g. where there are "" around ZIP codes in RUCA1 file
            RUdata.iloc[i, end_col] = row.iloc[0, RU_col]
        except IndexError: # accounts for error if row does not exist
            pass

    else: ## if the location code is inputed as an integer, float, etc, the program will search for exact matches within the loaded file
        try:
            row = RUfile[RUfile[loc_col] == loc_code]
            RUdata.iloc[i, end_col] = row.iloc[0, RU_col]
        except IndexError: # accounts for error if row does not exist
            pass

def findRUCAcode (end_col):
    '''
    This function is specific to the RUCA2 file, and converts participants' FIPS codes
    (10-11 digit version, i.e. at the census tract level) into RUCA codes. It was 
    extended from the basic findgeneralRUcode function due to the extra exceptions
    that occured with the RUCA2 file; for instance, the participants' FIPS codes provided
    by the FCC API in "2. address to loc extractor" did not always match with a FIPS code
    in the RUCA2 file. To provide RUCA codes or as many participants as possibe, this 
    function first estimates missing RUCA codes by using a 'rounded' FIPS and then,
    if still unsuccessful, asks the user to search for the participant's FIPS code using
    the participant address and the geolocator website that is actually correlated with 
    the RUCA2 file (in case this FIPS code is slightly different than the one found by 
    the FCC API) and reiterates the process.

    In other words, if the RUCA code corresponding to the participant FIPS code is 
    originally not found, or if there are several distinct RUCA codes for the 'rounded'
    FIPS, the program will direct the user to manually search address --> FIPS and the 
    program will try again with the new FIPS, first full and then rounded.

    Since this function is specific to the RUCA code file and participant data used in
    this project, only one argument is  required (end_col); however, this function may be used as
    base code for functions in similar projects.

    end_col (int) = index of the column in RUdata where the rural-urban code should be placed
    
    '''

    global FIPS1  ## addresses error "UnboundLocalError: local variable 'FIPS1' referenced before assignment"

    for iteration in range(2):
        try:
            row2 = RUCA2[RUCA2["State-County-Tract FIPS Code"] == np.int64(FIPS1)]
            RUdata.iloc[i, end_col] = row2.iloc[0, 4] 
            break
        
        except IndexError: # accounts for error if row does not exist
            try:
                row2 = RUCA2[RUCA2["State-County-Tract FIPS Code"].astype(str).str.contains(str(FIPS1)[:-1])] ## try with 'rounded' FIPS (last digit of census tract code is dropped)
                
                if (np.array(row2["Primary RUCA Code 2010"])[0] == np.array(row2["Primary RUCA Code 2010"])).all():
                    RUdata.iloc[i, end_col] = row2["Primary RUCA Code 2010"].mean()  ## if all codes for this larger area are the same, they are probably accurate
                    break

                else:
                    if iteration == 0:
                        FIPS1 = np.int64(input(f"Please search for {locdata.iloc[i, 3]} at http://www.ffiec.gov/Geocode/ and return the full FIPS code (add state, county, and tract codes together without any spaces or decimal points). "))
                        ## try once to search for FIPS using the provided website, in case the FIPS provided by the API was slightly different/inaccurate
                
            except IndexError: # accounts for error if row with rounded FIPS does not exist
                if iteration == 0:
                    FIPS1 = np.int64(input(f"Please search for {locdata.iloc[i, 3]} at http://www.ffiec.gov/Geocode/ and return the full FIPS code (add state, county, and tract codes together without any spaces or decimal points). ")) ## in the case where the row was not found, the code will skip the else block so we put the user prompt here

def findOMBcode1 (end_col):
    '''
    This function is specific to the rural-urban atlas file, and converts participants'
    FIPS codes (4-5 digit version, i.e. at the county level) into OMB codes (metro, 
    nonmetro, micro). It is a modification of the findgeneralRUcode function that
    accounts for the fact that this file uses three binary or 'dummy variable' columns
    for each OMB classification rather than a single column containing all three 
    classifications.

    Since it was the only such file used in this project, it is specific to the atlas
    file and only requires one argument (end_col); however, it could be easily 
    generalized for other files or rural-urban codes.

    end_col (int) = index of the column in RUdata where the rural-urban code should be placed
    '''

    try:
        row5 = atlas[atlas["FIPStxt"] == np.int64(FIPS2)]

        if row5.iloc[0, 7] == np.float64(1):             # adds OMB (corresponding to basic FIPS) #
            RUdata.iloc[i, end_col] = 'Metro'
        elif row5.iloc[0, 8] == np.float64(1): 
            RUdata.iloc[i, end_col] = 'Nonmetro'
        elif row5.iloc[0, 9] == np.float64(1):
            RUdata.iloc[i, end_col] = 'Micro'
    except IndexError: # accounts for error if row does not exist
        pass

def findOMBcode2 (end_col):
    '''
    This function is specific to the FORHP file (containing OMB classification data
    obtained from HRSA and FORHP), and also provides OMB codes (metro, micro, neither)
    as a check against the first OMB codes, as I found that the coding is slightly
    different between files (e.g. a participant location classified as nonmetro by the 
    atlas file may be classified as micro or neither by the FORHP file).

    It works almost identically to the findOMBcode1 function, except that it uses both
    ZIP and basic FIPS code from a participant, since ZIP was found to be insufficient
    to uniquely find a row within the FORHP file (thus leading to errors in accurately
    providing OMB code). This file could be easily generalized to find rural-urban codes
    where doing so requires more than one location code from the participant.

    end_col (int) = index of the column in RUdata where the rural-urban code should be placed
    
    '''
    
    try:
        row6 = FORHP[(FORHP["ZIP_CODE"] == np.int64(ZIP)) & (FORHP["STCountyFIPS"] == np.int64(FIPS2))]
        RUdata.iloc[i, end_col] = row6.iloc[0, 3]
    except IndexError: # accounts for error if row does not exist
        pass

for i in range(len(locdata)):

    ## this part of the code extracts and processes the participant's location 
    # information (e.g. ZIP, FIPS) from locdata for use:
    
    try:
        uid = locdata.iloc[i, 0]
        ZIP = int(locdata.iloc[i, 4])  ## need to convert to int to drop .0
        FIPS1 = locdata.iloc[i, 9]

        if len(str(locdata.iloc[i, 9])) >= 11:
            FIPS2 = str(FIPS1)[0:5]             ## need to first convert to str to extract first 4-5 numbers
        else:         
            FIPS2 = str(FIPS1)[0:4]             ## accounts for the (invisible) leading zero
    
        ### FIPS1 = full 10-11 digit FIPS code, i.e. encompassing state, county, and census tract codes
        ### FIPS2 = basic' 4-5 digit FIPS code, i.e. encompassing state and county codes

    except ValueError:   # accounts for location value = NaN
        continue

    
    ## this part of the code uses the extracted location information (e.g. ZIP, FIPS) 
    # for each participant and adds the corresponding rural-urban codes to RUdata:

    findgeneralRUcode(RUCA1, "''ZIP_CODE''", 3, str(ZIP), 1)    ## adds RUCA (corresponding to ZIP) into col 1
    findRUCAcode (2)                                            ## adds RUCA (corresponding to full FIPS) into col 2
    findgeneralRUcode(RUCC, "FIPS", 4, np.int64(FIPS2), 4)      ## adds RUCC (corresponding to basic FIPS) into col 4
    findgeneralRUcode(NCHS, "FIPS code", 6, np.int64(FIPS2), 6) ## adds NCHS (corresponding to basic FIPS) into col 6
    findgeneralRUcode(UIC, "FIPS", 4, np.int64(FIPS2), 10)      ## adds UIC (corresponding to basic FIPS) into col 10
    findOMBcode1(8)                                             ## adds OMB from atlas file (corresponding to basic FIPS) into col 8
    findOMBcode2(9)                                             ## adds OMB from FORHPS file (corresponding to ZIP and basic FIPS) into col 9

RUdata.to_csv(r'C:\Users\maria\OneDrive\Documents\RESEARCH\Data files\participant _ruralurbancodes.csv', index = False)