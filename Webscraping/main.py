import subprocess
import time

# How to operate:
# 0. Save previous Batch to its designated folder
# 1. Commit previous Batch to Github 
# 2. Select new batches from crunchbase.ipynb and SAVE the dataframe
# 3. Reset crunchbase_current_compnay.txt file to 0 if you start new
# 4. Delete previous list of closest snapshots
# 5. Run the file


def run_script(script_path): 
    try:
        subprocess.run(['python', script_path], check = True)
        print(f"Script {script_path} executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error occured in script {script_path}: {e}")
        return False
    return True

# Don't forget to reset the crunchbase_current_company.txt when you reset the scraper

scripts = [
    
    'Webscraping/utils/get_closest_snapshot_link.py', 
    'Webscraping/download/download_all_crunchbase.py', 
    'Webscraping/utils/store_all_website_text.py']

for script in scripts: 
    success = False
    while not success: 
        success = run_script(script)
        if not success: 
            print(f"Retrying {script} after error...")
            break