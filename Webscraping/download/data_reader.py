import pandas as pd
import pdb
import os, re
import numpy as np
from urllib.parse import urlparse

# Making the file path work

base_path = '/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3'
#base_path = '/home/moritz/Documents/Thesis Execution/Master_Thesis_V3'

os.chdir(os.path.join(base_path, 'Webscraping', 'utils'))
#os.chdir("/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/utils")


class data_reader:


    def clean_domain_url(website):
        if not website.startswith(('http://', 'https://')):
            website = 'http://' + website  # Add scheme for urlparse
        parsed_url = urlparse(website)
        domain = parsed_url.netloc
        domain = domain.replace("www.", "").replace("home.", "")

        print('Data Reader | Domain: ' + str(domain))
        return domain


    # Open
    #def add_closest_snapshot(companies, closest_snapshot_path="/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/tfidf/closest_snapshots_list.csv"):
    def add_closest_snapshot(companies, closest_snapshot_path=os.path.join(base_path, "tfidf", "closest_snapshots_list.csv")):

        if not os.path.exists(closest_snapshot_path):
            return companies

        # Reading the CSV with the closest snapshots
        snaps = pd.read_csv(closest_snapshot_path)
        
        # Selecting only relevant columns
        snaps = snaps[['org_uuid','closest_snapshot','closest_snapshot_time']]
        snaps['closest_snapshot_time'] = snaps['closest_snapshot_time'].astype(str)
        #snaps['closest_snapshot_year'] = pd.to_numeric(snaps.closest_snapshot_time.str.slice(stop=4), errors='coerce', downcast='integer').fillna(2000)
        snaps['closest_snapshot_year'] = pd.to_numeric(snaps.closest_snapshot_time.str.slice(stop=4), errors='coerce', downcast='integer')
        print(snaps['closest_snapshot_year'])
        companies =  companies.merge(snaps, how='left', on='org_uuid')
        companies['snapshot_in_window'] = np.absolute(companies.closest_snapshot_year - companies.founding_year) <= 2
        #companies.to_excel('/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/out/return_companies_add_closest_snapshot.xlsx')
        companies.to_excel(os.path.join(base_path, 'out', 'return_companies_add_closest_snapshot.xlsx'))
        
        print(companies.info())
        return companies

    # Open
    def read_crunchbase():
        #companies = pd.read_csv('/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Data/Crunchbase/websites.csv')
        companies = pd.read_csv(os.path.join(base_path, 'Data', 'Crunchbase', 'websites.csv'))
        companies = companies.rename(columns = {'Website':'website'})
        print('Data Reader, Nr. of Duplicates: ' + str(companies.duplicated()))
        print(companies.info())

        if not "closest_snapshot_time" in companies.columns:
            print('Adding Closest Snapshot')
            companies = data_reader.add_closest_snapshot(companies)
            print('Closest Snapshots Added!')
            print(companies.info())

        return companies

    # Open
    def read_preqin():
        companies = pd.read_stata("../../Data/Preqin/all_deals.minimal.dta")
        return companies

    # Adapted
    def read_public_companies(regex = None):
        #companies = pd.read_csv("/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Data/Crunchbase/websites.csv")
        companies = pd.read_csv(os.path.join('Data', 'Crunchbase', 'websites.csv'))
        companies = companies.rename(columns = {'Website':'website'})

        if regex is None:
            return companies
        else:
            return companies[companies.website.str.contains(regex)]



    def find_missing_public(year):
        public_firms = data_reader.read_public_companies()
        public_firms = public_firms[public_firms.ipoyear <= int(year)]
        public_firms['year'] = year
        public_firms['in_data'] = False
        
        path = "../../out_public/"
        for i in public_firms.index:        
            domain = public_firms.loc[i,'website']
            domain = data_reader.clean_domain_url(domain)

            file_folder = "{0}/{1}/{2}".format(path,domain, year)            
            if   os.path.exists(file_folder):
                public_firms.loc[i,'in_data'] = True
    
        missing_firms =  public_firms[~public_firms.in_data]
        
        print ("Finished checking for missing public firms in year" +year)
        print ("Report on Missing. \n \t. {0} Total public websites.\n\t. {1} downloaded.\n\t. {2} missing.".format(public_firms.shape[0], public_firms.shape[0] - missing_firms.shape[0], missing_firms.shape[0]))

        return missing_firms
