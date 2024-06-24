
import nltk
import pandas as pd
from website_text import website_text
import pdb
import pickle
import numpy as np
import os
from langdetect import detect


# Making the file path work

base_path = '/home/moritz/Documents/Thesis Execution/Master_Thesis_V3'
#base_path = '/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3'

os.chdir(os.path.join(base_path, 'Webscraping' ,'utils'))
#os.chdir("/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/utils")

class website_text_dataset:
    # This class is created for a series of helper methods to study the whole website dataset
    # such as adding flags of whether something is valid.  The method 'prep' is supposed to be called
    # before any analysis is done, thus allowing all sorts of things to be added in the process.


    
    def prep(website_info, update_language = False):
        website_info['text'] = website_info.text.str.strip()

        
        if 'lang' not in website_info or update_language is True:
            print('\t Detecting language. This step takes a few minutes.')            
            website_info['lang'] = website_info.text.apply(website_text_dataset.detect_lang)
            print("\t Done")

        print("\t .Identify invalid websites")
        website_info = website_text_dataset.add_is_valid_website(website_info)
        print("\t .Done")
        
        print("\t .Identify duplicate websites")
        website_info['is_duplicate'] = website_info.duplicated(subset = ['website','type'])
        print("\t .Done")
        
        return website_info


    

    

    def get_valid_public_firms_index(website_info):
        public_index = np.all([website_info.type == "public_firm",                                
                                 website_info.is_valid_website == True,
                                 website_info.is_duplicate == False],
                                axis=0)

        return public_index


    
    
    def get_valid_startups_index(website_info):
        startups_index = np.all([website_info.type == "startup",
                                 website_info.snapshot_in_window == True,
                                 website_info.is_valid_website == True,
                                 website_info.is_duplicate == False],
                                axis=0)

        return startups_index


        
    
    def add_is_valid_website(website_info):
        website_info['is_valid_website'] = True
        domain_word_pos = website_info.text.str.lower().str.find('domain')
        bad_domain = np.all([domain_word_pos >= 0 , domain_word_pos < 100], axis=0)


        invalid_conditions=[bad_domain,                                   
                            website_info.text.str.contains('BuyDomains.com'),
                            website_info.text.str.contains('This Web page is parked for FREE'),
                            website_info.text.str.contains('Free business profile for provided by Network Solutions'),
                            website_info.text.str.contains('The Sponsored Listings displayed above are served automatically'),

                            website_info.text.str.contains('Apache'),
                            website_info.text.str.contains('website is for sale'),
                            website_info.text.str.contains('This Web site coming soon'),
                            website_info.text.str.contains('Welcome to the new website! Our site has been recently created'),
                            website_info.text.str.match('^Wayback Machine'),
                            website_info.text.str.match('Wayback Machine See what s new with book lending'),
                            website_info.text.str.match('^AVAILABLE NOT FOUND'),
                            website_info.text.str.match('^DefaultHomePage'),
                            website_info.text.str.match('^I?n?t?ernet Archive: Scheduled Mantenance'),
                            website_info.text.str.match('^The page cannot be found'),
                            website_info.text.str.match('^503'),
                            website_info.text.str.match('^5?0?3 Service Unavailable'),
                            website_info.text.str.lower().str.match('domain down'),
                            website_info.text.str.match('^Too Many Requests'),
                            website_info.text.str.match('^Your browser does not support'),
                            website_info.text.str.match('^New Server for COMPANYNAME'),
                            website_info.text.str.contains('this page is parked FREE'),
                            website_info.text.str.contains('domain name was recently registered'),
                            website_info.text.str.contains('placeholder for domain'),
                            website_info.text.str.contains('xtremedata.com  : Low cost'),
                            website_info.text.str.lower().str.contains('domain name registration'),
                            website_info.text.str.contains('Under Construction'),
                            website_info.text.str.contains('This Web site is currently under'),
                            website_info.text.str.contains('This domain name was recently'),
                            website_info.text.str.contains('This page is parked free'),
                            website_info.text.str.match('^Microsoft VBScript runtime error'),
                            website_info.text.str.match('^WebFusion'),
                            website_info.text.str.match('^Register domain names'),
                            website_info.text.str.match('^Moved This page has moved'),
                            website_info.text.str.match('^Coming Soon'),
                            website_info.text.str.contains('Site (is )?Temporarily Unavailable'),
                            website_info.text.str.match('^Under Construction'),
                            website_info.text.str.match('^cPanel'),
                            website_info.text.str.match('^Authorization Required'),
                            website_info.text.str.match('^Top Web Search Directory Top Web Searches'),
                            website_info.text.str.match('^Web Searches'),
                            website_info.text.str.match('^Web Hosting'),
                            website_info.text.str.match('^Search Directory Page Sponsored Listing'),
                            website_info.text.str.match('^coming soon'),
                            website_info.text.str.match('This site is the default web server site'),
                            website_info.text.str.match('DF-1.4 %���� 0 obj< '),
                            website_info.text.str.match('This page uses frames, but your brow'),
                            website_info.text.str.match('U N D E R C O N S T R U C T I O N'),
                            website_info.text.str.match('We recommend you upgrade your browser to one of below free alternatives'),
                            website_info.text.str.match('enable JavaScript'),
                            website_info.text.str.lower().str.match('under construction'),
                            website_info.text.str.match('Page cannot be Please contact your service provider for more'),

                            website_info.text.str.match('^A WordPress Site'),
                            website_info.text.str.match('^Related Searches: Related Searches'),
                            website_info.text.str.match('^Welcome to IIS'),

                            ### Language
                            website_info.lang != 'en']
        
        #Some conditions by range of value in "find" method
        a= website_info.text.str.find("Go Daddy")
        invalid_conditions.append(np.logical_and(a>= 0 , a<200))
        
        a =  website_info.text.str.find("Wayback Machine")
        invalid_conditions.append(np.logical_and(a>= 0 , a<200))
        
        a =  website_info.text.str.find('This website is for sale')
        invalid_conditions.append(np.logical_and(a>= 0 , a<50))
        
        a =  website_info.text.str.find('Adobe Flash Player Download')
        invalid_conditions.append(np.logical_and(a>= 0 , a<30))
        
        website_info.at[np.any(invalid_conditions, axis=0),'is_valid_website'] = False
        
        return website_info


    

    def get_self_index(website_info, i, firmtype="startup"):
        self_index  = np.all([website_info.website == website_info.website[i],
                          website_info.type == firmtype],
                         axis=0)
        return self_index
        
    def get_latest_snapshots(path=os.path.join(base_path, "tfidf", "closest_snapshots_list.csv")):
    #def get_latest_snapshots(path="/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/tfidf/closest_snapshots_list.csv"):
        if os.path.exists(path):            
            print("Using closest snapshots from path {0}".format(path))
            return pd.read_csv(path)
        else:
            print("Could not find a closest snapshot file at {0}".format(path))
            return None
            

    lang_counter = 0
    def detect_lang(text):
        return detect(text)

        
    def setup_website_text_df( website_df, truncate_text_chars=5000):
        #
        #  this is the main method that converts a dataframe of firms into a 
        #  website dataset that can be used to study the similarity across firms.
        #
        
        websites = []        
        website_list= []
        website_info = {}  # Initialize the variable


        print("Loading all websites. Total: {0}".format(website_df.shape[0]), flush=True)
        counter  = 0
        counter_good = 0

        # Getting Snapshot DF, then formatting and extracting the year
        closest_snapshots = website_text_dataset.get_latest_snapshots()
        closest_snapshots['closest_snapshot_time'] = closest_snapshots['closest_snapshot_time'].astype(str)
        # Replace 'nan' with a placeholder or handle them
        closest_snapshots['snapshot_year'] = pd.to_numeric(closest_snapshots.closest_snapshot_time.str.slice(0,4), errors='coerce').fillna(0).astype(int) #Changed 'closest_snapshot_year' to "snapshot_year"

        #closest_snapshots['snapshot_year'] = closest_snapshots.closest_snapshot_time.str.slice(0,4).astype(int)
        print('web_txt_df | Extracted Years: ' + str(closest_snapshots['snapshot_year']))
        
        # Determining, whether the closest snapshot is close enough (<2 years) to the founding year


        ######## PRODUCES EMPTY COLUMN 
        closest_snapshots['snapshot_in_window'] = np.absolute(closest_snapshots.founding_year - closest_snapshots.snapshot_year) <= 2
        print('web_txt_df | Snapshots in Window: ' + str(closest_snapshots['snapshot_in_window']))


        # Performing the following operations for each row in the website_df, that gets passed to the setup_website_text_df method
        for index , row in website_df.iterrows():
            counter += 1
            
            # Creating a new dataframe
            doc = website_text(row['path'], row['website'], row['year'], row['incyear'])
            print(doc)

            # Creating a dictionary that saves the necessary website infos
            website_info = {'website': row['website'], 'text_len': 0, 'source': row['source'], 'type': row['type'], 'snapshot_in_window': None}
            print('web_txt_df | Pre-If Marker: website_info:   '+ str(website_info))

            # Checking whether the website-infos are existent and that the content of the website is valid
            if doc is not None and doc.is_valid_website():

                # getting the website text and checking length, then saving contents
                text = doc.get_website_text()
                website_info['text_len'] = len(text)

                # Shortening the text to a limit of caharcters
                website_info['text'] = text[:truncate_text_chars] if truncate_text_chars is not None else text
                
                # Re-Creating the website_info dictionary - Possible source of problems 
                website_info = {}
                website_info['website'] = row['website']
                website_info['text_len'] = len(doc.get_website_text())
                website_info['source'] = row['source']

                text = doc.get_website_text()
                print('web_text_df | text check: ' + str(text))

                # If the text is longer than its set limit, shortening to the limit of characters
                if truncate_text_chars is not None:
                    text = text[1:truncate_text_chars] if len(text) > truncate_text_chars else text

                # Saving the text to the website_info dataframe    
                website_info['text'] = text            
                website_info['type'] = row['type']

                # Getting the closest snapshot for the website from the corersponding object
                close_snap = closest_snapshots[closest_snapshots.website == website_info['website']]
                print('web_text_datase| Closest Snap: ' + str(close_snap))

                # Check if snapshot_in_window is valid for the current row
                if not row.get('snapshot_in_window', False):
                    print(f"Assigning False to website {row['website']} as it has no valid snapshot in window.")
                    row['snapshot_in_window'] = False

                
                

                # If there is a closest snap available, adding the snapshot to the dictionary and formatting it 
                if close_snap is not None and close_snap.shape[0] >= 1:
                    website_info['closest_snapshot'] = close_snap.closest_snapshot.iloc[0]
                    website_info['closest_snapshot_time'] = close_snap.closest_snapshot_time.iloc[0]
                    website_info['snapshot_in_window'] = close_snap.snapshot_in_window.iloc[0]
                    print('web_text_df | IF = True; creating snapshot_in_window column!')
                #else:
                    #website_info['closest_snapshot'] = False
                    

                # After adding everything, the dictionary for the company is appended to the website_list
                website_list.append(website_info)
            else:
                print(f"Website at index {index} is not valid or None.")

            # Debugging Conditions
            if 'snapshot_in_window' not in website_info:
                print(f"Missing 'snapshot_in_window' in website_info at index {index}")
            
            if (counter % 30) == 0:
                print("\t.. {0} ({1})".format(counter, counter_good), flush=True)

            if doc is not None and doc.is_valid_website():
                # Existing code to populate website_info
                print(f"website_info at index {index}: {website_info}")  # Debugging line
                #website_list.append(website_info)
            else:
                print(f"Doc not valid or None at index {index}")
        
        # For-Loop completed!    
        # Trying to extract the data from the website_list prematurely
        website_info_df = pd.DataFrame(website_list)
        
        if 'snapshot_in_window' not in website_info_df.columns:
            print("Column 'snapshot_in_window' not found in the DataFrame. Creating with default value.")
            website_info_df['snapshot_in_window'] = False  # or any default value you prefer
        else:
            website_info_df["snapshot_in_window"] = website_info_df["snapshot_in_window"].astype(float)




        return (website_info_df, websites)
        print("\t Done", flush=True)
        
