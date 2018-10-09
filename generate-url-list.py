from inputs import *

import pandas
from pandas import read_csv


if __name__ == '__main__':
	if SCRAPE_MODE == "csv":
		excel_file = read_csv(EXCEL_FILENAME)
		page_urls = excel_file.occurrenceid.str.strip()

		with open("url-list.txt",'w') as output_file:
			urls = page_urls.to_string(index=False)
			urls = urls.replace(" ","")
			output_file.write(urls)

	elif SCRAPE_MODE == "failures":
		with open("exception-url-list.txt","r") as exception_file:
			with open("url-list.txt","w") as output_file:
				exception_urls = exception_file.readlines()
				for exception_url in exception_urls:
					output_file.write(exception_url)