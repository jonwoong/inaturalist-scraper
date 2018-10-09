# inaturalist-scraper
Web Scraping of inaturalist.org using ScraPy and Selenium

## Dependencies
Python 2.7  
ScraPy  
Selenium  
ChromeDriver  

## How to Use
1. Place csv file in root project folder.
2. Change `EXCEL_FILENAME` in `inputs.py` to the file name of your csv.  
Column A must be Names  
Column B must be observation pages  
3. Make the script executable by running `$ chmod +x scrape.sh`
4. Run script with `$ ./scrape.sh`
