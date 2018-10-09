########## INPUTS/TOGGLES ##########

EXCEL_FILENAME = "Brazil-Test-01.csv" # name of csv in project folder's root
DOWNLOAD_IMAGES = True # toggle whether or not to save images (must be True or False) capitalization matters 
UPDATE_CSV = True # toggle whether or not to update csv (must be True or False) capitalization matters
DELETE_FAILURES = True # toggle whether or not to remove csv rows that failed to be scraped (must be True or False) capitalization matters

SCRAPE_MODE = "csv" # set where the scraped webpages originate from
# if you ran the script once and noticed missing images/csv entries, 
# you can change this to "failures" and run the script again
# this will attempt to scrape the urls that failed to in the previous run

