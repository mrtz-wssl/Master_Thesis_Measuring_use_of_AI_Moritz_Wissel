import os
from bs4 import BeautifulSoup
import sys
import pdb
import os
import re
import mimetypes

#base_path = '/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3'
base_path = '/home/moritz/Documents/Thesis Execution/Master_Thesis_V3'

sys.path.append(os.path.join(base_path, 'Webscraping', 'download'))
#sys.path.append('/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/download')  # Change the paths to directory, if code is reused
sys.path.append(os.path.join(base_path, 'Webscraping', 'crawler'))
#sys.path.append('/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/crawler') # Change the paths to directory, if code is reused

from waybackmachine_crawler import waybackmachine_crawler
from data_reader import data_reader

# Making the file path work
os.chdir(os.path.join(base_path, 'Webscraping', 'utils'))
#os.chdir("/Users/moritzwissel/Documents/GitHub/Master_Thesis_V3/Webscraping/utils")

class website_text:

    def __init__(self, path, domain, year, incyear = None, skip_memory_error = False):
        mimetypes.init()
        domain = data_reader.clean_domain_url(domain)
        print('website_text | Domain: ' + str(domain))
        self.texts = self.load_domain(path, domain, year, incyear , skip_memory_error = skip_memory_error)
        print(self.texts)
        print('website_text | Init Finish Marker')
        


    def get_website_text(self):
        if self.texts is not None:
            return " ".join(self.texts)
        else:
            return ""

        
    def clean_page_text(self, text, skip_memory_error = False):
        #initial_text = text
        try:
            text= re.sub(r"[\s,:#][\.\-@]?[\d\w]+[\.\-@][\d\w\.\-@_]*"," ",text)
            text= re.sub(r"[\s,:][\.\-@][\d\w]+"," ",text)
            text= re.sub(r"\s\d[\d\w]+"," ",text)
            text= re.sub(r"[{}>\*/\';]"," ",text)
            text= re.sub(r"\s+"," ",text)
            text= re.sub(r"DOMContentLoaded.*_static"," ",text)

            #remove all these random unicode words
            #text = re.sub(r"(\W|^)\w*" + '\x00' + "\w*\W"," ",text)
            #text = re.sub(r"(\W|^)\w*" + '\x01' + "\w*\W"," ",text)
            #text= re.sub(r"(\W|^)\w*" + '\x03' + "\w*\W"," ",text)
            return text
        except MemoryError as e:
            if skip_memory_error:
                print("\t --> Memory Error in method clean_page_text.. Skipping")
                return ""
            else:
                raise e


    def is_html_page(self,text):
        #remove downloaded PDFs, this is rarely used, since most are deleted when the
        #algorithm filters through bad_mimes.
        if text[0:3]=="PDF" or text[1:4] == "PDF":
            return False

        if text[0:3] == "PNG" or text[1:4] == "PNG":
            return False

        #any page this long has something wrong for sure.  100K characters are 120 letter pages!
        if len(text) > 100000:
            return False
        
        return True


    
    def is_valid_website(self):
        text_len = len(self.get_website_text())
        print(f"Checking validity: Text length = {text_len}")

        # Add more conditions or print statements here based on your logic
        if text_len < 50:  
            print("Website not valid based on text length criteria")
            return False
        else:
            print("Website considered valid")
            return True

        
    def load_page(self, page_file_path, skip_memory_error = False, char_limit=1000000):
        print(f"Attempting to load page from path: {page_file_path}")
        try:
            bad_mimes = ['application/pdf','text/x-perl','image/jpeg','application/x-msdos-program',
                         'image/gif', 'text/vcard','application/msword','application/xml',
                         'video/x-ms-wmv', 'text/css','text/vnd.sun.j2me.app-descriptor']            
            
            (mime, x) = mimetypes.guess_type(page_file_path)

            if mime is not None:
                #remove all undesired types of data that is not text to include into NLP
                if mime in bad_mimes:
                    return ""
                if mime.split("/")[0] in ['application','video','image','audio']:
                    return ""
            
            if mime not in ['text/html','text/plain'] and mime is not None:
                #pdb.set_trace()
                pass

            print(f"Opening file: {page_file_path}")
            f = open(page_file_path, encoding='utf-8')  # Specify encoding
            html = f.read()
            soup = BeautifulSoup(html,"html.parser")
            text = soup.get_text(separator = ' ')

            #just a limit of 1 million characters to avoid memory errors
            text = text[0:char_limit]
            
            return self.clean_page_text(text)
        except (TypeError, UnboundLocalError):
            print("\t. --> There was one error, skipping this page")
            return ""
        except UnicodeDecodeError:
            print(f"Unicode decode error encountered for file {page_file_path}. Skipping.")
            return ""

        except MemoryError as e:
            if skip_memory_error:
                ("\t --> Memory Error.. Skipping")
                return ""
            else:
                raise e
    
    def load_domain(self, path, domain, year=None, incyear = None, force_download=False,skip_memory_error = False):
        print(f"Loading domain: {domain} from path: {path}")
        clean_domain = data_reader.clean_domain_url(domain)     # Potential issue: clean_domain is also run in __init__
        print('Domain cleaned to: ' + str(clean_domain))
        root_folder = "{0}/{1}".format(path,clean_domain).replace("//","/")
        print('Root folder: ' + str(root_folder))
        if year is None:
            file_folder = root_folder
            print('website_text | file_folder assigned!')
        else: 
            file_folder = "{0}/{1}/{2}".format(path,clean_domain, year).replace("//","/")

        if os.path.exists(root_folder) is False or os.path.exists(file_folder) is False or os.path.isdir(file_folder) is False:
            if force_download is True:
                #depends on whether it is startup download of public download
                pdb.set_trace()
                download_year = year if year is not None else incyear
                download_year = int(download_year)
                self.force_download(root_folder , domain, download_year)
            else:
                return None
            
        files = []
    
        for file_name in os.listdir(file_folder):
            if file_name.endswith('.html') or file_name.endswith('.txt'):  # Check file extension
                text = self.load_page(file_folder + "/" + file_name, skip_memory_error = skip_memory_error)
                if self.is_html_page(text):
                    text = re.sub(r"\s+"," ",text)
                    files.append(text)
        
        return files



    
    def force_download(self,path, domain, year):
        year_folder = year is not None

        crawler = waybackmachine_crawler(website = domain, output_folder = path , year_folder = year_folder)
        crawler.crawl_from_date(year, 12, 31)
