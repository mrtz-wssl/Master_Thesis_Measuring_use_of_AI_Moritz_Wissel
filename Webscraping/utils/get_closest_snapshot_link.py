import argparse
import traceback
import re
import time
import pandas as pd
import pdb
import sys
import os

base_path = '/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3'
#base_path = '/home/moritz/Documents/Thesis Execution/Master_Thesis_V3'

os.chdir(os.path.join(base_path, 'Webscraping', 'utils'))
#os.chdir("/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/utils")

sys.path.append(os.path.abspath('../crawler'))
sys.path.append(os.path.abspath('../text_analysis'))
from waybackmachine_crawler import waybackmachine_crawler
import requests
from data_reader import data_reader

from json.decoder import JSONDecodeError
import time
 

###############################################
##
##   Run: python3 get_closest_snapshot_link.py
##   This script goes to the Wayback Machine to get the closest website link
##    for all websitse in Crunchbase.
##
##
##
##
##
##


websites = data_reader.read_crunchbase()
websites[['closest_snapshot']] = ""
websites[['closest_snapshot_time']] = ""


for index, company in websites.iterrows():
    crawler = waybackmachine_crawler(company['website'])
    year = company['founding_year'] + 1

    try:
        closest_snapshot = crawler.list_closest_snapshot(year,1,1)
        time.sleep(3)
    except JSONDecodeError:
        print("\n\n*********JSONDecodeError************")
        closest_snapshot = "Error or No Data"

    if closest_snapshot is not None and closest_snapshot != "Error or No Data":
        websites.at[index,'closest_snapshot']=str(closest_snapshot)
        websites.at[index,'closest_snapshot_time']=closest_snapshot.get('timestamp', 'No Timestamp')
    else:
        websites.at[index,'closest_snapshot']="None"
        #websites.at[index,'closest_snapshot_time']="None"
    
    print("\t\t---->  {0} of {1}".format(index, websites.shape[0]))


    #store every 100 sites
    if (index%100) == 0:
        websites.to_csv("../../tfidf/closest_snapshots_list.csv")
    time.sleep(4)

# The result is exported and gets importet in the data_reader script    
#websites.to_csv("../../tfidf/closest_snapshots_list.csv")
#websites.to_csv("../../Data/websites.csv")
