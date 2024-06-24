

import sys
import pdb
import os
import argparse

base_path = '/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3'
#base_path = '/home/moritz/Documents/Thesis Execution/Master_Thesis_V3'

#sys.path.append(os.path.abspath('/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/download'))
sys.path.append(os.path.join(base_path, 'Webscraping', 'download'))
#sys.path.append(os.path.abspath('/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/text_analysis'))
sys.path.append(os.path.join(base_path, 'Webscraping', 'text_analysis'))
from data_reader import data_reader
from website_text_dataset import website_text_dataset
from langdetect import detect




# Running a for loop that creates a seperate dataframe for each year
for year in range(2018, 2023):

    print("Reading data for year {0}".format(year))
    
    # Getting and formatting the company dataframe
    cb_startups = data_reader.read_crunchbase()
    print('Main | Companies added successfully!')
    cb_startups['incyear'] = cb_startups.founding_year
    cb_startups = cb_startups[cb_startups.incyear == year]
    cb_startups['year'] = None
    #cb_startups['path'] = "/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/out" # hardcoded path
    cb_startups['path'] = f"{base_path}/out"


    cb_startups = cb_startups[['website','year','path','incyear']]
    cb_startups["type"] = "startup"
    cb_startups['source'] = "crunchbase"
    print(cb_startups.info())

    # Saving the dataframe to a copy
    all_websites = cb_startups.copy()

    print("Loading text")
    
    ########## RETURNS EMPTY DATAFRAME
    (website_info, websites) = website_text_dataset.setup_website_text_df(all_websites, truncate_text_chars=5000)
    csv_path = os.path.join(base_path, 'Data', 'data_output', f'website_info_{year}.csv')
    #csv_path = "/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Data/data_output/website_info_{0}.csv".format(year)
    print(website_info.info())

    print("text loaded")
    print("replacing nas")
    print(website_info.info())

    website_info["snapshot_in_window"] = website_info.snapshot_in_window.astype(float)
    print("storing file to {0}".format(csv_path))


    try:
    # Print DataFrame just before writing to file
        print("DataFrame to be written to CSV:", website_info)

        # Write DataFrame to CSV
        website_info.to_csv(csv_path, index=False, mode='w+')
        print("File written successfully")

    except Exception as e:
        print("Error while writing file:", e)

