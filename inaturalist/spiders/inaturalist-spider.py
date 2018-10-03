########## HEADERS ##########

import sys
from os.path import dirname as up 

path_to_project_folder = up(up(up(__file__)))
sys.path.append(path_to_project_folder)

from inputs import EXCEL_FILENAME # user defined

import urllib
from urllib import URLopener # used to download images

import pandas 
from pandas import DataFrame, read_csv # used to extract column data from excel file

import scrapy # used to create web crawlers
from scrapy import Spider

import selenium # used to load web pages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

########## CONSTANTS ##########

chromedriver_options = webdriver.ChromeOptions()
chromedriver_options.add_argument("headless")

excel_file = read_csv(EXCEL_FILENAME) # obtain contents of csv file
species_names = excel_file.Name.tolist() # obtain Name column
page_urls = excel_file.occurrenceid.tolist() # obtain occurrenceid column

observation_numbers = [] # list of all unique numbers at the end of "inturalist.org/observations/"
for url in page_urls: # build the list of observation numbers using occurrenceid column
	observation_numbers.append(url.split("/")[-1])

observation_name_dict = dict(zip(observation_numbers, species_names)) # create dictionary, key=obvservation number, value=a Name

########## SPIDER ##########

class InaturalistSpider(Spider):
	name = "inaturalist" # name of spider

	with open("url-list.txt","rt") as url_file:
		start_urls = [url.strip() for url in url_file.readlines()] # fetch all urls from url-list.txt

	def __init__(self):
		self.driver = webdriver.Chrome(chrome_options=chromedriver_options) # PhantonJS is used as a headless web-browser

	def parse(self, response):
		self.driver.get(response.url) # load an observation page in selenium
		
		image_elements = WebDriverWait(self.driver,10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, "//div[@class='image-gallery-image']/img"))) # scrape images of species
		image_urls = [] # list of urls, scraped from image elements
		for image_element in image_elements: # build image_urls
			image_url = image_element.get_attribute("src") # extract src attribtue from image element (the image url)
			image_urls.append(image_url) # add extracted url to image_urls
		
		image = URLopener() # create a blank URLopener object to later download image(s) 
		species_name = observation_name_dict[str(response.url).strip().split("/")[-1]] # look up species name in our dictionary by using observation number as key
		number_of_images = len(image_urls) # calculate total number of images for an observation
		
		if number_of_images > 1: # if there are multiple images for one observation page
			for index in range(number_of_images): # loop over all images
				indexed_species_name = species_name + '-0' + str(index+1) # create string that looks like "species_name-0x" where x is >= 1
				image.retrieve(image_urls[index].replace("large","original"), "images/" + indexed_species_name + ".jpeg") # download the image, save it as "species_name-0x.jpeg"

				dataframe = DataFrame({'Name' : [indexed_species_name], 'occurrenceid' : [response.url]}, columns=['Name','occurrenceid']) # create a new row to add to csv containing "species_name-0x" and url
				excel_file = dataframe.to_csv(EXCEL_FILENAME, header=None, mode='a', index=False) # add the new row to original csv file

		elif number_of_images == 1: # if there is only one image for one observation
			image.retrieve(str(image_urls[0]).replace("large","original"), "images/" + species_name + ".jpeg") # download the image, save it as "species_name.jpeg"
		
		return