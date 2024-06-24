# Master_Thesis_Measuring_use_of_AI_Moritz_Wissel
 
## Table of Contents
- [Introduction](#introduction)
- [Files](#Files)

DISCLAIMER: Only the Jupyter Notebooks are relevant to understand the thesis. All other files are needed for the code to run correctly.


## Introduction
This thesis explores the effectiveness of AI-related keywords on early-stage startup websites as indicators of underlying quality, addressing the information asymmetry between venture capitalists (VCs) and startups. With strong signals often absent in early- stage startups, weak signals, such as website content, become crucial. The study examines signals of strength, quantity, and timing, particularly focusing on AI-related terms due to the significant increase in AI startups and funding in recent years. Utilizing a representative sample of US-based startups, I scraped websites for AI-related keywords to analyze their signaling effectiveness. Performing a logistic regression analysis, I found that AI-related keywords are an effective weak signal for startup quality and thus increase funding likelihood. I also found that the number of keywords does not influence funding success and that the signaling effect of keywords is higher for older startups. By investigating the role of AI-related keywords in signaling startup quality, this thesis contributes to a deeper understanding of effective signals in the venture capital domain.



## Files
- analysis.ipynb: Contains all analyses of the master thesis, including descriptive statistics, the logistic regression models, and graphs
- analysis setup.ipynb: Combines the collected data, examines its validity and prepares it for an in-depth analysis.
- keywords.ipnb: Runs the keyword analysis and optimizes the search algorithm 
- crunchbase.ipynb: Creates the company data sample and prepares it for the scraping process

- Working Docs: Include all files that I used to perform manual checks 
- Webscraping: Contains the web scraper
- tfidf: Supplementary file of the webscraper that contains the list of closes snapshots for the scraper
- Plots: Contains all exported plots
- Exports: Contains all exported files, used to transfer data and tables from the analysis to the Thesis
- Documentation: Work in progress files used during the analysis process
- Data: Contains all crunchbase data related to the web scraper and the analysis