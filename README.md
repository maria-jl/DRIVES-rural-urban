# DRIVES-rural-urban

## Objective
This repository includes work from my summer 2020 research project. The objective of this project is to investigate the impact of location of residence (urban/suburban/rural) on daily driving behaviour among older adults. This research will then be linked to emerging machine learning models to predict the presence of preclinical Alzheimer disease (AD) from naturalistic driving patterns captured by GPS data.

With this objective in mind, this project repository is divided into three main areas:

**rural urban coding (preprocessing)**

1. homelocationfinder (trip end lat/long --> home lat/long/address [v1] or intermediate addresses file --> complete home lat/long/address file [v2])  
2. address to LOC extractor (home lat/long/address --> various location info, e.g. ZIP, FIPS, city, county, etc)  
3. LOC to RU codes convertor (location info --> various RU codes, e.g. RUCA, RCC, UIC)  
4. RU codes to RU class convertor (various RU codes --> corresponding three-level classes, e.g. RUCA_class, & final codes "RUCA_ru" and "other_ru")

**driving correlations (preprocessing)**

5. rural urban_driving summary (driving data --> overall driving summaries for each participant, where each row has participant uid, overall RU code, and the values for various overall driving behaviours)
5. [a] skmob attribute finder (driving data --> skmob-obtained driving summaries, e.g. no. unique locations and radius of gyration)  
6. rural urban_driving correlations (rural urban_driving summary --> plots of possible RU/driving correlations)  

**driving correlations (machine learning)**  

7. rural urban_driving MODELS (rural urban_driving correlations --> machine learning models that attempt to predict an individual's class (rural, urban) from their overall driving patterns)


**NOTE:** Most of these Python files flow directly from one another (e.g. the address file generated in step <1> is directly used in step <2>, without any processing in between). However, a few steps required manual processing: namely, the choice of version of homelocationfinder in <2>, the manual creation of the "overall RU code" column in 'participant _ruralurbancodes.csv' based on "RUCA_ru" and "other_ru" columns, and the addition of skmob driving summaries from 'ruralurban_skmob summary.csv' to 'ruralurban_driving summary.csv' prior to visualizations in <6>.

## Data

The data used in this project was obtained from the DRIVES study at Washington University. It is comprised mostly of data obtained from GPS loggers in participant cars, thus including information collected every 30s while driving (e.g. vehicle speed, vehicle acceleration, vehicle latitude and longitude), as well as trip information (e.g. whether the trip was during the day or the night). Two datasets were combined for use in this project, due to the low number of participants that were found to be classified as rural: the 'main' dataset with participants mostly from the Greater St. Louis area in Missouri and Illinois (STL, n = 246), and a second dataset with participants from North Carolina (NC, n = 36). Since each dataset is structured slightly differently, with somewhat different driving information, they are used both together and seperately in this project. For the final stages of the project (e.g. machine learning models), only the main dataset was used; this decision was made to ensure consistency because some different driving/rurality trends were observed between the NC and STL datsets at step <6>, and because we cannot be sure that all driving metrics were obtained or even defined in the same way for both datasets.


## Rural-urban classifications

In this project, a number of different ways of classifying areas as rural or urban were investigated. Five methods were selected for their ease of use (i.e. accessibility of public classification data in the form of Excel/CSV files and/or APIs) as well as potential to be useful in distinguishing rural and urban areas when considering rurality as an influence on driving behaviours.

Rural-urban classifications (US) investigated in this project include:

**OMB (Office of Management and Budget)**

*codes:*  
Metro area – Urban core of 50,000 or more people  
Micro area  – Urban core of 10,000-49,9999 people  
Rural area – Counties outside of metro or micro areas  

*notes:*  
OMB classification is known to underrepresent rural areas. The data file used classified areas using a basic FIPS code (i.e. at the county level).


**NCHS (National Center for Health Statistics)**

*codes:*  
Large central metro – Counties in MSAs (metropolitan statistical areas) of 1 million or more population that: 1. Contain the entire population of the largest principal city of the MSA, or 2. Have their entire population contained in the largest principal city of the MSA, or 3. Contain at least 250,000 inhabitants of any principal city of the MSA.  
Large fringe metro – Counties in MSAs of 1 million or more population that did not qualify as large central metro counties.  
Medium metro – Counties in MSAs of populations of 250,000 to 999,999.  
Small metro – Counties in MSAs of populations less than 250,000.  
Micropolitan – Counties in micropolitan statistical areas.  
Noncore = Nonmetropolitan counties that did not qualify as micropolitan.  

*classification:*  
In order to collapse these codes into useable categories, we further defined NCHS codes in this way:  
1-4 = "metro"  
5 = "micro"  
6 = "rural"  

*notes:*  
This classification was developed for health stastistical purposes so it may be particularly useful for this project; however, previous studies usually used it for research that assessed health outcomes based on access to services such as hospitals. As such, we must consider the distinction between social behaviours and health outcomes when considering how level of rurality may affect driving patterns (i.e. rather than trying to predict health outcomes based on rural/urban access to health services, we are trying to predict driving behaviours based on rural/urban location of residence). The data file used classified areas using a basic FIPS code (i.e. at the county level).


**UIC (Urban Influence Codes)**

*codes:*  
1 – In large metro area of 1+ million residents  
2 – In small metro area of less than 1 million residents  
3 – Micropolitan adjacent to large metro  
4 – Non-core adjacent to large metro  
5 – Micropolitan adjacent to small metro  
6 – Non-core adjacent to small metro with own town  
7 – Non-core adjacent to small metro with no town  
8 – Micropolitan not adjacent to a metro area  
9 – Non-core adjacent to micro with own town  
10 – Non-core adjacent to micro with no town  
11 – Non-core not adjacent to metro or micro with own town  
12 – Non-core not adjacent to metro or micro with no town  

*classification:*  
In order to collapse these codes into useable categories, we further defined UIC codes in this way:  
1-2 = "metro"  
3-8 = "micro"  
9-12 = "rural"  

*notes:*  
This classification is intended to distinguish metropolitan counties by population size of their metro area, and nonmetropolitan counties by size of the largest city or town and proximity to metro and micropolitan areas. The data file used classified areas using a basic FIPS code (i.e. at the county level).

**RUCC (Rural-Urban Continuum Codes)**

*codes:*  
1 – Counties in metro areas of 1 million population or more  
2 – Counties in metro areas of 250,000 to 1 million population  
3 – Counties in metro areas of fewer than 250,000 population  
4 – Urban population of 20,000 or more, adjacent to a metro area  
5 – Urban population of 20,000 or more, not adjacent to a metro area  
6 – Urban population of 2,500 to 19,999, adjacent to a metro area  
7 – Urban population of 2,500 to 19,999, not adjacent to a metro area  
8 – Completely rural or less than 2,500 urban population, adjacent to a metro area  
9 – Completely rural or less than 2,500 urban population, not adjacent to a metro area  
88 – Unknown-Alaska/Hawaii State/not official USDA Rural-Urban Continuum code  
99 – Unknown/not official USDA Rural-Urban Continuum code  

*classification:*  
In order to collapse these codes into useable categories, we further defined RUCC codes in this way:  
1-3 = "metro"  
4-7 = "micro"  
8-9 = "rural"  

*notes:*  
This classification is intended to distinguish metropolitan counties by the population size of their metro area, and nonmetropolitan counties by degree of urbanization and adjacency to a metro area. The data file used classified areas using a basic FIPS code (i.e. at the county level).


**RUCA (Rural-Urban Commuting Codes)**

*codes:*  
1	– Metropolitan area core: primary flow within an urbanized area (UA)  
2	– Metropolitan area high commuting: primary flow 30% or more to a UA  
3	– Metropolitan area low commuting: primary flow 10% to 30% to a UA  
4	– Micropolitan area core: primary flow within an urban cluster of 10,000 to 49,999 (large UC)  
5	– Micropolitan high commuting: primary flow 30% or more to a large UC  
6	– Micropolitan low commuting: primary flow 10% to 30% to a large UC  
7	– Small town core: primary flow within an urban cluster of 2,500 to 9,999 (small UC)  
8	– Small town high commuting: primary flow 30% or more to a small UC  
9	– Small town low commuting: primary flow 10% to 30% to a small UC  
10 – Rural areas: primary flow to a tract outside a UA or UC  
99 – Not coded: Census tract has zero population and no rural-urban identifier information  

*classification:*  
In order to collapse these codes into useable categories, we further defined RUCA codes in this way:    
1-3 = "metro"  
4-6 = "micro"  
7-10 = "rural"  

*notes:*  
This classification takes into account measures of population density, urbanization, and daily commuting. Since it classifies areas at the census tract level, it is more precise in addition to considering commuting flows rather than just population or adjacency to urban areas. The data files used classified areas using ZIP code and a state-county-tract FIPS code (i.e. at the census tract level), respectively. For any areas that were classified differently between the two comparison files, the file using the state-county-tract FIPS code was used since it is more precise.


***Overall Classifications***  

In this project, like many other research studies, I defined metro and micro classification as "urban", with everything else being "rural." From the classifications for each code type, I then developed three overarching rural-urban classifications:

*RUCA_ru (9R)* --- based on RUCA (from state-county-tract FIPS) classifications: rural (RUCA_class = micro or rural) or urban (RUCA_class = metro)

*other_ru (5R)* --- based on all codes other than RUCA (RUCC, NCHS, OMB, UIC) as we found that all these codes agreed based on the definition of rurality and urbanicity as: rural (classes = micro, rural, nonmetro, or neither) or urban (classes = metro)

*overall (8R)* --- As the ultimate classification chosen for this project, a binary code of rural or urban was assigned to each participant based on firstly RUCA_ru and secondly other_ru (since RUCA codes are based on smaller/more precise locations as well as encompass a perhaps wider and more encompassing definition of rurality and urbanicity). In other words, for most participants where RUCA_ru and other_ru did not match, RUCA_ru was chosen as the code; except for one case where the RUCA code was one point away from being categorized into the opposite class, in which case the other_ru was chosen as the code. 

**NOTE:** R represents the number of participants classified as rural, within the main/STL dataset of 246 participants with driving data.
