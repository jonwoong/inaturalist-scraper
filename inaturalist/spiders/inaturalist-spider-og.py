import urllib
from urllib import URLopener # used to download images

import pandas 
from pandas import DataFrame, read_csv # used to extract column data from excel file

import scrapy # used to create web crawlers
from scrapy.http import HtmlResponse
from scrapy.item import Item, Field

import selenium # used to load web pages
from selenium import webdriver

class InaturalistSpider(scrapy.Spider):
	#name = "inaturalist" # name of spider

	with open("url-list.txt","rt") as url_file:
		start_urls = [url.strip() for url in url_file.readlines()] # fetch all urls from url-list.txt

	def __init__(self, *args, **kwargs):
		super(InaturalistSpider, self).__init__(*args, **kwargs) # read in command-line arguments

		self.driver = webdriver.PhantomJS() # PhantonJS is used as a headless web-browser
		self.excel_file = read_csv(self.input_filename) # obtain contents of csv file
		self.species_names = self.excel_file.Name.tolist() # obtain Name column
		self.page_urls = self.excel_file.occurrenceid.tolist() # obtain occurrenceid column

		self.observation_numbers = [] # list of all unique numbers at the end of "inturalist.org/observations/"
		for url in self.page_urls: # build the list of observation numbers using occurrenceid column
			self.observation_numbers.append(url.split("/")[-1])

		self.observation_name_dict = dict(zip(self.observation_numbers, self.species_names)) # create dictionary, key=obvservation number, value=a Name

	def parse(self, response):
		self.driver.get(response.url) # load an observation page in selenium
		rendered_html = self.driver.find_element_by_tag_name('html').get_attribute('innerHTML') # scrape HTML contents of observation page after javascript is done loading
		response = HtmlResponse(url=response.url, body=rendered_html, encoding="utf-8") # convert HTML contents into an HtmlResponse object
		image_urls = response.xpath('//div[@class="image-gallery-image"]/img/@src').extract() # scrape all high-res image urls on observation page
		
		image = URLopener() # create a blank URLopener object to later download image(s) 
		species_name = self.observation_name_dict[str(response.url).strip().split("/")[-1]] # look up species name in our dictionary by using observation number as key
		number_of_images = len(image_urls) # calculate total number of images for an observation
		
		if number_of_images > 1: # if there are multiple images for one observation page
			for index in range(number_of_images): # loop over all images
				indexed_species_name = species_name + '-0' + str(index+1) # create string that looks like "species_name-0x" where x is >= 1
				image.retrieve(image_urls[index], indexed_species_name + ".jpeg") # download the image, save it as "species_name-0x.jpeg"

				dataframe = DataFrame({'Name' : [indexed_species_name], 'occurrenceid' : [response.url]}, columns=['Name','occurrenceid']) # create a new row to add to csv containing "species_name-0x" and url
				self.excel_file = dataframe.to_csv(self.input_filename, header=None, mode='a', index=False) # add the new row to original csv file

		elif number_of_images == 1: # if there is only one image for one observation
			image.retrieve(str(image_urls[0]),species_name + ".jpeg") # download the image, save it as "species_name.jpeg"
		
		yield # stop this spider instance
		
		
		


