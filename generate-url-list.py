from inputs import EXCEL_FILENAME

import pandas
from pandas import read_csv

excel_file = read_csv(EXCEL_FILENAME)
page_urls = excel_file.occurrenceid.str.strip()

with open("url-list.txt","w") as output_file:
	urls = page_urls.to_string(index=False)
	urls = urls.replace(" ","")
	output_file.write(urls)